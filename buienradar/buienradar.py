"""
Buienradar library to get parsed weather data from buienradar.nl.
"""
import logging
from datetime import datetime, timedelta

import requests
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
PRECIPITATION = 'precipitation'
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
BRMINTEMP = 'maxtemp'
BRMAXTEMP = 'maxtempmax'

# Sensor types are defined like so:
# SENSOR_TYPES = { 'key': 'key in buienradar xml', }
SENSOR_TYPES = {
    STATIONNAME: 'stationnaam',
    SYMBOL: 'icoonactueel',
    HUMIDITY: 'luchtvochtigheid',
    TEMPERATURE: 'temperatuurGC',
    GROUNDTEMP: 'temperatuur10cm',
    WINDSPEED: 'windsnelheidMS',
    WINDFORCE: 'windsnelheidBF',
    WINDDIRECTION: 'windrichtingGR',
    WINDAZIMUTH: 'windrichting',
    PRESSURE: 'luchtdruk',
    VISIBILITY: 'zichtmeters',
    WINDGUST: 'windstotenMS',
    PRECIPITATION: 'regenMMPU',
    IRRADIANCE: 'zonintensiteitWM2',
}

log = logging.getLogger(__name__)


def __get_data(url):
    """Load data from url and return result."""
    log.info("Retrieving xml weather data (%s)...", url)
    return requests.get(url)


def get_data():
    """Get buienradar xml data and return results."""
    result = {SUCCESS: False, MESSAGE: None}

    try:
        r = __get_data('https://xml.buienradar.nl/')

        if (200 == r.status_code):
            result[SUCCESS] = (200 == r.status_code)
            result[STATUS_CODE] = r.status_code
            result[HEADERS] = r.headers
            result[CONTENT] = r.content
        else:
            r = __get_data('https://api.buienradar.nl/')

            result[SUCCESS] = (200 == r.status_code)
            result[STATUS_CODE] = r.status_code
            result[HEADERS] = r.headers
            result[CONTENT] = r.content
    except requests.RequestException as ose:
        result[MESSAGE] = 'Error getting xml data. %s' % ose
        log.error(result[MESSAGE])

    return result


def parse_data(content, latitude=52.091579, longitude=5.119734):
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
            fcdatetime = fcdatetime.replace(hour=0, minute=0, second=0, microsecond=0)

            fcdata = {TEMPERATURE: __get_temp(tmpsect),
                      DATETIME: fcdatetime}
            result[DATA][FORECAST].append(fcdata)
    return result


def __get_temp(section):
    """Get the forecasted temp from xml section."""
    try:
        return (float(section[BRMINTEMP]) +
                float(section[BRMAXTEMP])) / 2
    except (ValueError, TypeError, KeyError):
        return None


def __get_ws_distance(wstation, latitude, longitude):
    """
    Get the distance to the weatherstation from wstation section of xml.

    wstation: weerstation section of buienradar xml (dict)
    latitude: our latitude
    longitude: our longitude
    """
    if wstation:
        try:
            wslat = float(wstation[BRLAT])
            wslon = float(wstation[BRLON])

            dist = vincenty((latitude, longitude), (wslat, wslon))
            log.debug("calc distance: %s (latitude: %s, longitude: %s, wslat: %s, wslon: %s)",
                  dist, latitude, longitude, wslat, wslon)
            return dist
        except (ValueError, TypeError, KeyError):
            # value does not exist, or is not a float
            return None
    else:
        return None


def __select_nearest_ws(xmldata, latitude, longitude):
    """Select the nearest weatherstation."""
    log.debug("__select_nearest_ws: latitude: %s, longitude: %s", latitude, longitude)
    dist = 0
    dist2 = 0
    loc_data = None

    try:
        ws_xml = xmldata[BRWEERGEGEVENS][BRACTUEELWEER][BRWEERSTATIONS][BRWEERSTATION]
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
