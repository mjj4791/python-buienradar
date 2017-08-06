"""Buienradar library to get parsed weather data from buienradar.nl."""
import logging
from datetime import datetime, timedelta

import pytz
import requests
import xmltodict
from vincenty import vincenty

SUCCESS = 'success'
STATUS_CODE = 'status_code'
HEADERS = 'headers'
CONTENT = 'content'
RAINCONTENT = 'raincontent'
MESSAGE = 'msg'
DATA = 'data'

ATTRIBUTION_INFO = "Data provided by buienradar.nl"

# key names as user in returned result
ATTRIBUTION = "attribution"
CONDCODE = 'condcode'
CONDITION = 'condition'
DATETIME = 'datetime'
DETAILED = 'detailed'
EXACT = 'exact'
EXACTNL = 'exact_nl'
DISTANCE = 'distance'
FORECAST = 'forecast'
GROUNDTEMP = 'groundtemperature'
HUMIDITY = 'humidity'
IMAGE = 'image'
IRRADIANCE = 'irradiance'
MEASURED = 'measured'
PRECIPITATION = 'precipitation'
PRECIPITATION_FORECAST = 'precipitation_forecast'
PRESSURE = 'pressure'
STATIONNAME = 'stationname'
TEMPERATURE = 'temperature'
VISIBILITY = 'visibility'
WINDAZIMUTH = 'windazimuth'
WINDDIRECTION = 'winddirection'
WINDFORCE = 'windforce'
WINDGUST = 'windgust'
WINDSPEED = 'windspeed'

# keys in forcasted data:
MAX_TEMP = 'maxtemp'
MIN_TEMP = 'mintemp'
RAIN = 'rain'
RAIN_CHANCE = 'rainchance'
SUN_CHANCE = 'sunchance'
SNOW = 'snow'

# keys in forcasted precipitation data:
AVERAGE = 'average'
TIMEFRAME = 'timeframe'
TOTAL = 'total'

# key names in buienradar xml:
__BRROOT = 'buienradarnl'
__BRWEERGEGEVENS = 'weergegevens'
__BRACTUEELWEER = 'actueel_weer'
__BRWEERSTATIONS = 'weerstations'
__BRWEERSTATION = 'weerstation'
__BRLAT = 'lat'
__BRLON = 'lon'
__BRSTATIONCODE = 'stationcode'
__BRSTATIONNAAM = 'stationnaam'
__BRSNEEUWCMS = 'sneeuwcms'
__BRTEXT = '#text'
__BRZIN = '@zin'
__BRID = '@ID'
__BRICOON = 'icoon'
__BRVERWACHTING = 'verwachting_meerdaags'
__BRDAYFC = "dag-plus%d"
__BRMINTEMP = 'mintemp'
__BRMAXTEMP = 'maxtemp'
__BRKANSZON = 'kanszon'
__BRKANSREGEN = 'kansregen'
__BRMAXMMREGEN = 'maxmmregen'
__BRMINMMREGEN = 'minmmregen'
__BRWINDKRACHT = 'windkracht'

# buienradat date format: '07/26/2017 15:50:00'
__DATE_FORMAT = '%m/%d/%Y %H:%M:%S'
__TIMEZONE = 'Europe/Amsterdam'


def __to_int(val):
    """Convert val into an integer value."""
    try:
        return int(val)
    except (ValueError, TypeError):
        return 0


def __to_float(val, digits):
    """Convert val into float with digits decimal."""
    try:
        return round(float(val), digits)
    except (ValueError, TypeError):
        return float(0)


def __to_float2(val):
    """Convert val into float with 2 decimals."""
    return __to_float(val, 2)


def __to_float1(val):
    """Convert val into float with 1 decimal."""
    return __to_float(val, 1)


def __to_localdatetime(val):
    """Convert val into a local datetime for tz Europe/Amsterdam."""
    try:
        dt = datetime.strptime(val, __DATE_FORMAT)
        dt = pytz.timezone(__TIMEZONE).localize(dt)
        return dt
    except (ValueError, TypeError):
        return None


# Sensor types are defined like so:
# SENSOR_TYPES = { 'key': ['key in buienradar xml', conversion function], }
SENSOR_TYPES = {
    HUMIDITY: ['luchtvochtigheid', __to_int],
    GROUNDTEMP: ['temperatuur10cm', __to_float1],
    IRRADIANCE: ['zonintensiteitWM2', __to_int],
    MEASURED: ['datum', __to_localdatetime],
    PRECIPITATION: ['regenMMPU', __to_float1],
    PRESSURE: ['luchtdruk', __to_float2],
    STATIONNAME: ['stationnaam', None],
    CONDITION: ['icoonactueel', None],
    TEMPERATURE: ['temperatuurGC', __to_float1],
    VISIBILITY: ['zichtmeters', __to_int],
    WINDSPEED: ['windsnelheidMS', __to_float2],
    WINDFORCE: ['windsnelheidBF', __to_int],
    WINDDIRECTION: ['windrichting', None],
    WINDAZIMUTH: ['windrichtingGR', __to_int],
    WINDGUST: ['windstotenMS', __to_float2],
}

# Condition codes are defined like so:
# __BRCONDITIONS = { 'code': 'conditon', 'detailed', 'exact', 'exact_nl'}
__BRCONDITIONS = {
    'a': ['clear', 'clear', 'Almost fully clear (sunny/clear)',
          'Vrijwel onbewolkt (zonnig/helder)'],
    'b': ['cloudy', 'partlycloudy', 'Mix of clear and medium or low clouds',
          'Mix van opklaringen en middelbare of lage bewolking'],
    'j': ['cloudy', 'partlycloudy', 'Mix of clear and high clouds',
          'Mix van opklaringen en hoge bewolking'],
    'o': ['cloudy', 'partlycloudy', 'Partly cloudy',
          'Half bewolkt'],
    'r': ['cloudy', 'partlycloudy', '?? Partly cloudy ??',
          '?? Partly cloudy ??'],
    'c': ['cloudy', 'cloudy', 'Heavily clouded',
          'Zwaar bewolkt'],
    'p': ['cloudy', 'cloudy', '?? Cloudy ??',
          '?? Cloudy ??'],
    'd': ['fog', 'partlycloudy-fog',
          'Alternating cloudy with local fog(banks)',
          'Afwisselend bewolkt met lokaal mist(banken)'],
    'n': ['fog', 'fog', 'Clear and local mist or fog',
          'Opklaring en lokaal nevel of mist'],
    'f': ['rainy', 'partlycloudy-light-rain',
          'Alternatingly cloudy with some light rain',
          'Afwisselend bewolkt met (mogelijk) wat lichte regen'],
    'h': ['rainy', 'partlycloudy-rain', '?? partlycloudy-rain ??',
          '?? partlycloudy-rain ??'],
    'k': ['rainy', 'partlycloudy-light-rain', '??partlycloudy-light-rain ??',
          '??partlycloudy-light-rain ??'],
    'l': ['rainy', 'rainy', '?? rainy ??',
          '?? rainy ??'],
    'q': ['rainy', 'rainy', 'Heavily clouded with rain',
          'Zwaar bewolkt en regen'],
    'w': ['rainy', 'snowy-rainy',
          'Heavily clouded with rain and winter precipitation',
          'Zwaar bewolkt met regen en winterse neerslag'],
    'm': ['rainy', 'light-rain', 'Heavily clouded with some light rain',
          'Zwaar bewolkt met wat lichte regen'],
    'u': ['snowy', 'partlycloudy-light-snow', 'Cloudy with light snow',
          'Afwisselend bewolkt met lichte sneeuwval'],
    'i': ['snowy', 'partlycloudy-snow', '?? partlycloudy-snow ??',
          '?? partlycloudy-snow ??'],
    'v': ['snowy', 'light-snow', 'Heavily clouded with light snowfall',
          'Zwaar bewolkt met lichte sneeuwval'],
    't': ['snowy', 'snowy', 'Heavy snowfall',
          'Zware sneeuwval'],
    'g': ['lightning', 'partlycloudy-lightning',
          'Clear with (possibly) some heavy lightning',
          'Opklaringen en kans op enkele pittige (onweers)buien'],
    's': ['lightning', 'lightning',
          'Cloudy with (possibly) some heavy (thunderstorms) showers',
          'Bewolkt en kans op enkele pittige (onweers)buien'],
    # 'e': ['N/A', 'N/A', 'N/A', 'N/A'],
    # 'x': ['N/A', 'N/A', 'N/A', 'N/A'],
    # 'y': ['N/A', 'N/A', 'N/A', 'N/A'],
    # 'z': ['N/A', 'N/A', 'N/A', 'N/A'],
}

log = logging.getLogger(__name__)


def get_data(latitude=52.091579, longitude=5.119734):
    """Get buienradar xml data and return results."""
    final_result = {SUCCESS: False, MESSAGE: None,
                    CONTENT: None, RAINCONTENT: None}

    log.info("Getting buienradar data for latitude=%s, longitude=%s",
             latitude, longitude)
    result = __get_ws_data()

    if result[SUCCESS]:
        # store xml data:
        final_result[CONTENT] = result[CONTENT]
        final_result[SUCCESS] = True
    else:
        msg = "Status: %d, Msg: %s" % (result[STATUS_CODE], result[MESSAGE])
        log.warning(msg)
        final_result[MESSAGE] = msg

    # load forecasted precipitation:
    result = __get_precipfc_data(latitude,
                                 longitude)
    if result[SUCCESS]:
        final_result[RAINCONTENT] = result[CONTENT]
    else:
        msg = "Status: %d, Msg: %s" % (result[STATUS_CODE], result[MESSAGE])
        log.warning(msg)
        final_result[MESSAGE] = msg

    return final_result


def parse_data(content, raincontent, latitude=52.091579,
               longitude=5.119734, timeframe=60):
    """Parse the raw data and return as data dictionary."""
    result = {SUCCESS: False, MESSAGE: None, DATA: None}

    if timeframe < 5 or timeframe > 120:
        raise ValueError("Timeframe must be >=5 and <=120.")

    if content is not None:
        result = __parse_ws_data(content, latitude, longitude)

        if result[SUCCESS] and raincontent is not None:
            data = __parse_precipfc_data(raincontent, timeframe)
            result[DATA][PRECIPITATION_FORECAST] = data

    log.debug("Extracted weather-data: %s", result[DATA])
    return result


def condition_from_code(condcode):
    """Get the condition name from the condition code."""
    if condcode in __BRCONDITIONS:
        cond_data = __BRCONDITIONS[condcode]

        return {CONDCODE: condcode,
                CONDITION: cond_data[0],
                DETAILED: cond_data[1],
                EXACT: cond_data[2],
                EXACTNL: cond_data[3],
                }
    return None


def __get_url(url):
    """Load data from url and return result."""
    log.info("Retrieving xml weather data (%s)...", url)
    result = {SUCCESS: False, MESSAGE: None}
    try:
        r = requests.get(url)
        result[STATUS_CODE] = r.status_code
        result[HEADERS] = r.headers
        result[CONTENT] = r.text
        if (200 == r.status_code):
            result[SUCCESS] = True
        else:
            result[MESSAGE] = "Got http statuscode: %d." % (r.status_code)
        return result
    except requests.RequestException as ose:
        result[MESSAGE] = 'Error getting url data. %s' % ose
        log.error(result[MESSAGE])

    return result


def __get_ws_data():
    """Get buienradar xml data and return results."""
    url = 'https://xml.buienradar.nl/'

    result = __get_url(url)
    if result[SUCCESS]:
        return result

    # try secondary url:
    url = 'https://api.buienradar.nl/'
    result = __get_url(url)

    return result


def __get_precipfc_data(latitude, longitude):
    """Get buienradar forecasted precipitation."""
    url = 'http://gadgets.buienradar.nl/data/raintext/?lat={}&lon={}'
    # rounding coordinates prevents unnecessary redirects/calls
    url = url.format(
        round(latitude, 2),
        round(longitude, 2)
        )
    result = __get_url(url)
    return result


def __parse_ws_data(content, latitude=52.091579, longitude=5.119734):
    """Parse the buienradar xml and rain data."""
    log.info("Parse ws data: latitude: %s, longitude: %s", latitude, longitude)
    result = {SUCCESS: False, MESSAGE: None, DATA: None}

    # convert the xml data into a dictionary:
    try:
        xmldata = xmltodict.parse(content)[__BRROOT]
    except (xmltodict.expat.ExpatError, KeyError) as err:
        result[MESSAGE] = "Unable to parse content as xml."
        log.exception(result[MESSAGE])
        return result

    # select the nearest weather station
    loc_data = __select_nearest_ws(xmldata, latitude, longitude)
    # process current weather data from selected weatherstation
    if not loc_data:
        result[MESSAGE] = 'No location selected.'
        return result

    if not __is_valid(loc_data):
        result[MESSAGE] = 'Location data is invalid.'
        return result

    # add distance to weatherstation
    log.debug("Raw location data: %s", loc_data)
    result[DISTANCE] = __get_ws_distance(loc_data, latitude, longitude)
    result = __parse_loc_data(loc_data, result)

    # extract weather forecast
    try:
        fc_data = xmldata[__BRWEERGEGEVENS][__BRVERWACHTING]
    except (xmltodict.expat.ExpatError, KeyError) as err:
        result[MESSAGE] = 'Unable to extract forecast data.'
        log.exception(result[MESSAGE])
        return result

    if fc_data:
        # result = __parse_fc_data(fc_data, result)
        log.debug("Raw forecast data: %s", fc_data)
        result[DATA][FORECAST] = __parse_fc_data(fc_data)

    return result


def __parse_precipfc_data(data, timeframe):
    """Parse the forecasted precipitation data."""
    result = {AVERAGE: None, TOTAL: None, TIMEFRAME: None}

    log.debug("Precipitation data: %s", data)
    lines = data.splitlines()
    index = 1
    totalrain = 0
    numberoflines = 0
    nrlines = min(len(lines), round(float(timeframe)/5) + 1)
    # looping through lines of forecasted precipitation data and
    # not using the time data (HH:MM) int the data. This is to allow for
    # correct data in case we are running in a different timezone.
    while index < nrlines:
        line = lines[index]
        log.debug("__parse_precipfc_data: line: %s", line)
        (val, key) = line.split("|")
        # See buienradar documentation for this api, attribution
        # https://www.buienradar.nl/overbuienradar/gratis-weerdata
        #
        # Op basis van de door u gewenste coordinaten (latitude en longitude)
        # kunt u de neerslag tot twee uur vooruit ophalen in tekstvorm. De
        # data wordt iedere 5 minuten geupdatet. Op deze pagina kunt u de
        # neerslag in tekst vinden. De waarde 0 geeft geen neerslag aan (droog)
        # de waarde 255 geeft zware neerslag aan. Gebruik de volgende formule
        # voor het omrekenen naar de neerslagintensiteit in de eenheid
        # millimeter per uur (mm/u):
        #
        # Neerslagintensiteit = 10^((waarde-109)/32)
        #
        # Ter controle: een waarde van 77 is gelijk aan een neerslagintensiteit
        # van 0,1 mm/u.
        mmu = 10**(float((int(val) - 109))/32)
        totalrain = totalrain + float(mmu)
        numberoflines = numberoflines + 1
        index += 1

    if numberoflines > 0:
        result[AVERAGE] = round((totalrain / numberoflines), 2)
    else:
        result[AVERAGE] = 0
    result[TOTAL] = round(totalrain/12, 2)
    result[TIMEFRAME] = timeframe

    return result


def __is_valid(loc_data):
    """Determine if this can be valid data (not all 0's)."""
    for key, [value, func] in SENSOR_TYPES.items():
        if (key != CONDITION and key != STATIONNAME and key != MEASURED):
            if (func is not None):
                sens_data = loc_data.get(value)
                if func(sens_data) != 0:
                    return True


def __parse_loc_data(loc_data, result):
    """Parse the xml data from selected weatherstation."""
    result[DATA] = {ATTRIBUTION: ATTRIBUTION_INFO,
                    FORECAST: [],
                    PRECIPITATION_FORECAST: None}

    for key, [value, func] in SENSOR_TYPES.items():
        result[DATA][key] = None
        try:
            sens_data = loc_data[value]
            if key == CONDITION:
                # update weather symbol & status text
                code = sens_data[__BRID][:1]
                result[DATA][CONDITION] = condition_from_code(code)
                result[DATA][CONDITION][IMAGE] = sens_data[__BRTEXT]
            else:
                if key == STATIONNAME:
                    name = sens_data[__BRTEXT].replace("Meetstation", "")
                    name = name.strip()
                    name += " (%s)" % loc_data[__BRSTATIONCODE]
                    result[DATA][key] = name
                else:
                    # update all other data
                    if func is not None:
                        result[DATA][key] = func(sens_data)
                    else:
                        result[DATA][key] = sens_data
        except KeyError:
            if result[MESSAGE] is None:
                result[MESSAGE] = "Missing key(s) in br data: "
            result[MESSAGE] += "%s " % value
            log.warning("Data element with key='%s' "
                        "not loaded from br data!", key)
    result[SUCCESS] = True
    return result


def __parse_fc_data(fc_data):
    """Parse the forecast data from the xml section."""
    fc = []
    for daycnt in range(1, 6):
        daysection = __BRDAYFC % daycnt
        if daysection in fc_data:
            tmpsect = fc_data[daysection]
            fcdatetime = datetime.now(pytz.timezone(__TIMEZONE))
            fcdatetime = fcdatetime.replace(hour=12,
                                            minute=0,
                                            second=0,
                                            microsecond=0)
            # add daycnt days
            fcdatetime = fcdatetime + timedelta(days=daycnt)
            code = tmpsect.get(__BRICOON, []).get(__BRID)
            fcdata = {
                      CONDITION: condition_from_code(code),
                      TEMPERATURE: __get_float(tmpsect, __BRMAXTEMP),
                      MIN_TEMP: __get_float(tmpsect, __BRMINTEMP),
                      MAX_TEMP: __get_float(tmpsect, __BRMAXTEMP),
                      SUN_CHANCE: __get_int(tmpsect, __BRKANSZON),
                      RAIN_CHANCE: __get_int(tmpsect, __BRKANSREGEN),
                      RAIN: __get_float(tmpsect, __BRMAXMMREGEN),
                      SNOW: __get_float(tmpsect, __BRSNEEUWCMS),
                      WINDFORCE: __get_int(tmpsect, __BRWINDKRACHT),
                      DATETIME: fcdatetime,
                     }
            fcdata[CONDITION][IMAGE] = tmpsect.get(__BRICOON, []).get(__BRTEXT)

            fc.append(fcdata)
    return fc


def __get_float(section, name):
    """Get the forecasted float from xml section."""
    try:
        return float(section[name])
    except (ValueError, TypeError, KeyError):
        return float(0)


def __get_int(section, name):
    """Get the forecasted int from xml section."""
    try:
        return int(section[name])
    except (ValueError, TypeError, KeyError):
        return 0


def __get_ws_distance(wstation, latitude, longitude):
    """Get the distance to the weatherstation from wstation section of xml.

    wstation: weerstation section of buienradar xml (dict)
    latitude: our latitude
    longitude: our longitude
    """
    if wstation:
        try:
            wslat = float(wstation[__BRLAT])
            wslon = float(wstation[__BRLON])

            dist = vincenty((latitude, longitude), (wslat, wslon))
            log.debug("calc distance: %s (latitude: %s, longitude: "
                      "%s, wslat: %s, wslon: %s)", dist, latitude,
                      longitude, wslat, wslon)
            return dist
        except (ValueError, TypeError, KeyError):
            # value does not exist, or is not a float
            return None
    else:
        return None


def __select_nearest_ws(xmldata, latitude, longitude):
    """Select the nearest weatherstation."""
    log.debug("__select_nearest_ws: latitude: %s, longitude: %s",
              latitude, longitude)
    dist = 0
    dist2 = 0
    loc_data = None

    try:
        ws_xml = xmldata[__BRWEERGEGEVENS][__BRACTUEELWEER]
        ws_xml = ws_xml[__BRWEERSTATIONS][__BRWEERSTATION]
    except (KeyError, TypeError):
        log.warning("Missing section in Buienradar xmldata (%s)."
                    "Can happen 00:00-01:00 CE(S)T",
                    __BRWEERSTATION)
        return None

    for wstation in ws_xml:
        dist2 = __get_ws_distance(wstation, latitude, longitude)

        if dist2 is not None:
            if ((loc_data is None) or (dist2 < dist)):
                dist = dist2
                loc_data = wstation

    if loc_data is None:
        log.warning("No weatherstation selected; aborting...")
        return None
    else:
        try:
            log.debug("Selected weatherstation: code='%s', "
                      "name='%s', lat='%s', lon='%s'.",
                      loc_data[__BRSTATIONCODE],
                      loc_data[__BRSTATIONNAAM][__BRTEXT],
                      loc_data[__BRLAT],
                      loc_data[__BRLON])
        except KeyError:
            log.debug("Selected weatherstation")
        return loc_data
