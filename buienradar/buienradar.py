"""
Buienradar library to get parsed weather data from buienradar.nl.
"""
import asyncio
import logging
from datetime import datetime, timedelta

import aiohttp
import async_timeout
import xmltodict
from vincenty import vincenty

SUCCESS = 'success'
STATUS_CODE = 'status_code'
HEADERS = 'headers'
CONTENT = 'content'
MESSAGE = 'msg'
DATA = 'data'

ATTRIBUTION_INFO = "Data provided by buienradar.nl"

# key names as user in returned result
ATTRIBUTION = "attribution"
DATETIME = 'datetime'
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
SYMBOL = 'symbol'
TEMPERATURE = 'temperature'
VISIBILITY = 'visibility'
WINDAZIMUTH = 'windazimuth'
WINDDIRECTION = 'winddirection'
WINDFORCE = 'windforce'
WINDGUST = 'windgust'
WINDSPEED = 'windspeed'

# keys in forcasted data:
MAX_TEMP = 'max_temp'
MIN_TEMP = 'min_temp'
RAIN = 'rain'
RAIN_CHANCE = 'rain_chance'
SUN_CHANCE = 'sun_chance'

# keys in forcasted precipitation data:
AVERAGE = 'average'
TIMEFRAME = 'timeframe'
TOTAL = 'total'

# key names in buienradar xml:
BRROOT = 'buienradarnl'
BRWEERGEGEVENS = 'weergegevens'
BRACTUEELWEER = 'actueel_weer'
BRWEERSTATIONS = 'weerstations'
BRWEERSTATION = 'weerstation'
BRLAT = 'lat'
BRLON = 'lon'
BRSTATIONCODE = 'stationcode'
BRSTATIONNAAM = 'stationnaam'
BRTEXT = '#text'
BRZIN = '@zin'
BRVERWACHTING = 'verwachting_meerdaags'
BRDAYFC = "dag-plus%d"
BRMINTEMP = 'mintemp'
BRMAXTEMP = 'maxtemp'
BRKANSZON = 'kanszon'
BRKANSREGEN = 'kansregen'
BRMAXMMREGEN = 'maxmmregen'
BRMINMMREGEN = 'minmmregen'
BRWINDKRACHT = 'windkracht'

# Sensor types are defined like so:
# SENSOR_TYPES = { 'key': 'key in buienradar xml', }
SENSOR_TYPES = {
    HUMIDITY: 'luchtvochtigheid',
    GROUNDTEMP: 'temperatuur10cm',
    IRRADIANCE: 'zonintensiteitWM2',
    MEASURED: 'datum',
    PRECIPITATION: 'regenMMPU',
    PRESSURE: 'luchtdruk',
    STATIONNAME: 'stationnaam',
    SYMBOL: 'icoonactueel',
    TEMPERATURE: 'temperatuurGC',
    VISIBILITY: 'zichtmeters',
    WINDSPEED: 'windsnelheidMS',
    WINDFORCE: 'windsnelheidBF',
    WINDDIRECTION: 'windrichtingGR',
    WINDAZIMUTH: 'windrichting',
    WINDGUST: 'windstotenMS',
}

log = logging.getLogger(__name__)


@asyncio.coroutine
def async_get_data(latitude=52.091579, longitude=5.119734, timeframe=3600):
    """Get buienradar xml data and return results."""
    result = yield from __async_get_ws_data(latitude, longitude)

    if result[SUCCESS]:
        # load forecasted precipitation:
        fc_data = yield from __async_get_precipfc_data(latitude,
                                                       longitude,
                                                       timeframe)
        result[DATA][PRECIPITATION_FORECAST] = fc_data
    return result


def get_data(latitude=52.091579, longitude=5.119734, timeframe=3600):
    """Get buienradar xml data and return results."""
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(async_get_data(
                                                    latitude,
                                                    longitude,
                                                    timeframe,
                                                   )
                                     )
    return result


@asyncio.coroutine
def __async_get_url(url):
    """Load data from url and return result."""
    log.info("Retrieving xml weather data (%s)...", url)
    resp = None
    with async_timeout.timeout(10):
        try:
            resp = yield from aiohttp.request('GET', url)
            return resp
        except (asyncio.TimeoutError, asyncio.CancelledError,
                aiohttp.ClientError) as err:
            return None
        finally:
            if resp is not None:
                yield from resp.release()


@asyncio.coroutine
def __async_get_ws_data(latitude=52.091579, longitude=5.119734):
    """Get buienradar xml data and return results."""
    result = {SUCCESS: False, MESSAGE: None}
    r = None

    url = 'https://xml.buienradar.nl/'
    r = yield from __async_get_url(url)

    if (r is not None and 200 == r.status):
        result[SUCCESS] = (200 == r.status)
        result[STATUS_CODE] = r.status
        result[HEADERS] = r.headers
        result[CONTENT] = yield from r.text()
    else:
        url = 'https://api.buienradar.nl/'
        r = yield from __async_get_url(url)

        result[SUCCESS] = (200 == r.status)
        result[STATUS_CODE] = r.status
        result[HEADERS] = r.headers
        result[CONTENT] = yield from r.text()

    if result[SUCCESS]:
        result = __parse_data(result[CONTENT])

    return result


def __parse_precipfc_data(data, timeframe):
    """Parse the forecasted precipitation data."""
    result = {AVERAGE: None, TOTAL: None, TIMEFRAME: None}
    forecast = {}

    for line in data.splitlines():
        (val, key) = line.split("|")
        # See buienradar documentation for this api, attribution
        # https://www.buienradar.nl/overbuienradar/gratis-weerdata
        #
        # Op basis van de door u gewenste coördinaten (latitude en longitude)
        # kunt u de neerslag tot twee uur vooruit ophalen in tekstvorm. De
        # data wordt iedere 5 minuten geüpdatet. Op deze pagina kunt u de
        # neerslag in tekst vinden. De waarde 0 geeft geen neerslag aan (droog)
        # de waarde 255 geeft zware neerslag aan. Gebruik de volgende formule
        # voor het omrekenen naar de neerslagintensiteit in de eenheid
        # millimeter per uur (mm/u):
        #
        # Neerslagintensiteit = 10^((waarde-109)/32)
        #
        # Ter controle: een waarde van 77 is gelijk aan een neerslagintensiteit van 0,1 mm/u.
        mmu = 10**((int(val) - 109)/32)
        forecast[(key)] = mmu

        totalrain = 0
        numberoflines = 0
        for key, value in forecast.items():
            tdelta = datetime.strptime(key, '%H:%M') - datetime.now()
            if tdelta.days < 0:
                tdelta = timedelta(days=0, seconds=tdelta.seconds,
                                   microseconds=tdelta.microseconds)
            if tdelta.seconds > 0 and tdelta.seconds <= timeframe:
                totalrain = totalrain + float(value)
                numberoflines = numberoflines + 1

        if numberoflines > 0:
            result[AVERAGE] = round((totalrain / numberoflines), 2)
        result[TOTAL] = round(totalrain/12, 2)
        result[TIMEFRAME] = timeframe

    return result


@asyncio.coroutine
def __async_get_precipfc_data(latitude, longitude, timeframe):
    """Get buienradar forecasted precipitation."""
    format = "http://gadgets.buienradar.nl/data/raintext/?lat=%s&lon=%s"
    url = format % (latitude, longitude)
    r = yield from __async_get_url(url)
    if (r is not None and 200 == r.status):
        data = yield from r.text()

        return __parse_precipfc_data(data, timeframe)

    return None


def __parse_data(content, latitude=52.091579, longitude=5.119734):
    """Parse the buienradar xml data."""
    log.debug("parse: latitude: %s, longitude: %s", latitude, longitude)
    result = {SUCCESS: False, MESSAGE: None, DATA: None}

    # convert the xml data into a dictionary:
    try:
        xmldata = xmltodict.parse(content)[BRROOT]
    except (xmltodict.expat.ExpatError, KeyError) as err:
        result[MESSAGE] = "Unable to parse content as xml."
        log.exception(result[MESSAGE])
        return result

    # select the nearest weather station
    loc_data = __select_nearest_ws(xmldata, latitude, longitude)
    # process current weather data from selected weatherstation
    if loc_data:
        # add distance to weatherstation
        result[DISTANCE] = __get_ws_distance(loc_data, latitude, longitude)

        result = __parse_loc_data(loc_data, result)
        log.debug("Extracted weather-data: %s", result[DATA])

        # extract weather forecast
        try:
            fc_data = xmldata[BRWEERGEGEVENS][BRVERWACHTING]
        except (xmltodict.expat.ExpatError, KeyError) as err:
            result[MESSAGE] = 'Unable to extract forecast data.'
            log.exception(result[MESSAGE])
            return result

        if fc_data:
            result = __parse_fc_data(fc_data, result)
    else:
        result[MESSAGE] = 'No location selected.'

    return result


def __parse_loc_data(loc_data, result):
    """Parse the xml data from selected weatherstation."""
    result[DATA] = {ATTRIBUTION: ATTRIBUTION_INFO, FORECAST: []}

    for key, value in SENSOR_TYPES.items():
        result[DATA][key] = None
        try:
            sens_data = loc_data[value]
            if key == SYMBOL:
                # update weather symbol & status text
                result[DATA][key] = sens_data[BRZIN]
                result[DATA][IMAGE] = sens_data[BRTEXT]
            else:
                if key == STATIONNAME:
                    result[DATA][key] = sens_data[BRTEXT]
                    result[DATA][key] += " (%s)" % loc_data[BRSTATIONCODE]
                else:
                    # update all other data
                    result[DATA][key] = sens_data
        except KeyError:
            if result[MESSAGE] is None:
                result[MESSAGE] = "Missing key(s) in br data: "
            result[MESSAGE] += "%s " % value
            log.warning("Data element with key='%s' "
                        "not loaded from br data!", key)
    result[SUCCESS] = True
    return result


def __parse_fc_data(fc_data, result):
    """Parse the forecast data from the xml section."""
    for daycnt in range(1, 6):
        daysection = BRDAYFC % daycnt
        if daysection in fc_data:
            tmpsect = fc_data[daysection]
            fcdatetime = datetime.today()
            # add daycnt days
            fcdatetime += timedelta(days=daycnt)
            fcdatetime = fcdatetime.replace(hour=0, minute=0,
                                            second=0, microsecond=0)

            fcdata = {
                      TEMPERATURE: __get_float(tmpsect, BRMAXTEMP),
                      MIN_TEMP: __get_float(tmpsect, BRMINTEMP),
                      MAX_TEMP: __get_float(tmpsect, BRMAXTEMP),
                      SUN_CHANCE: __get_int(tmpsect, BRKANSZON),
                      RAIN_CHANCE: __get_int(tmpsect, BRKANSREGEN),
                      RAIN: __get_float(tmpsect, BRMAXMMREGEN),
                      WINDFORCE: __get_int(tmpsect, BRWINDKRACHT),
                      DATETIME: fcdatetime
                     }
            result[DATA][FORECAST].append(fcdata)
    return result


def __get_float(section, name):
    """Get the forecasted float from xml section."""
    try:
        return float(section[name])
    except (ValueError, TypeError, KeyError):
        return None


def __get_int(section, name):
    """Get the forecasted int from xml section."""
    try:
        return int(section[name])
    except (ValueError, TypeError, KeyError):
        return None


def __get_ws_distance(wstation, latitude, longitude):
    """Get the distance to the weatherstation from wstation section of xml.

    wstation: weerstation section of buienradar xml (dict)
    latitude: our latitude
    longitude: our longitude
    """
    if wstation:
        try:
            wslat = float(wstation[BRLAT])
            wslon = float(wstation[BRLON])

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
        ws_xml = xmldata[BRWEERGEGEVENS][BRACTUEELWEER]
        ws_xml = ws_xml[BRWEERSTATIONS][BRWEERSTATION]
    except (KeyError, TypeError):
        log.warning("Missing section in Buienradar xmldata (%s)."
                    "Can happen 00:00-01:00 CE(S)T",
                    BRWEERSTATION)
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
                      loc_data[BRSTATIONCODE],
                      loc_data[BRSTATIONNAAM][BRTEXT],
                      loc_data[BRLAT],
                      loc_data[BRLON])
        except KeyError:
            log.debug("Selected weatherstation")
        return loc_data
