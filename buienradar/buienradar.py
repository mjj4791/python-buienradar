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
ROOT = 'buienradarnl'
WEERGEGEVENS = 'weergegevens'
ACTUEELWEER = 'actueel_weer'
WEERSTATIONS = 'weerstations'
WEERSTATION = 'weerstation'
LAT = 'lat'
LON = 'lon'
STATIONCODE = 'stationcode'
STATIONNAME = 'stationnaam'
TEXT = '#text'
ZIN = '@zin'
VERWACHTING = 'verwachting_meerdaags'
DAYFC = "dag-plus%d"
MINTEMP = 'maxtemp'
MAXTEMP = 'maxtempmax'

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


def get_data():
    """Get buienradar xml data and return results."""
    result = {SUCCESS: False, MESSAGE: None}

    log.info("Retrieving xml weather data...")
    try:
        r = requests.get("https://xml.buienradar.nl/")

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
    result = {SUCCESS: False, MESSAGE: None, DATA: None, FORECAST: []}

    # convert the xml data into a dictionary:
    try:
        xmldata = xmltodict.parse(content)[ROOT]
    except (xmltodict.expat.ExpatError, IndexError) as err:
        result[MESSAGE] = "Unable to parse content as xml."
        log.exception(result[MESSAGE])
        return result

    # select the nearest weather station
    loc_data = __select_nearest_ws(xmldata, latitude, longitude)
    # process current weather data from selected weatherstation
    if loc_data:
        result = __parse_loc_data(loc_data, result)
        log.debug("Extracted weather-data: %s", result[DATA])
    else:
        result[MESSAGE] = 'No location selected.'

    # extract weather forecast
    try:
        fc_data = xmldata[WEERGEGEVENS][VERWACHTING]
    except (xmltodict.expat.ExpatError, IndexError) as err:
        result[MESSAGE] = "Unable to extract forecast data."
        log.exception(result[MESSAGE])
        return result

    if fc_data:
        result = __parse_fc_data(fc_data, result)

    return result


def __parse_loc_data(loc_data, result):
    """Parse the xml data from selected weatherstation."""
    result[DATA] = {ATTRIBUTION: ATTRIBUTION_INFO}
    for key, value in SENSOR_TYPES.items():
        result[DATA][key] = None
        try:
            sens_data = loc_data[value]
            if key == SYMBOL:
                # update weather symbol & status text
                result[DATA][key] = sens_data[ZIN]
                result[DATA][IMAGE] = sens_data[TEXT]
            else:
                if key == STATIONNAME:
                    result[DATA][key] = sens_data[TEXT]
                else:
                    # update all other data
                    result[DATA][key] = sens_data
        except KeyError:
            log.warning("Data element with key='%s' "
                        "not loaded from br data!", key)
    result[SUCCESS] = True
    return result


def __parse_fc_data(fc_data, result):
    """Parse the forecast data from the xml section."""
    for daycnt in range(1, 6):
        daysection = DAYFC % daycnt
        if daysection in fc_data:
            tmpsect = fc_data[daysection]
            fcdatetime = datetime.today()
            # add daycnt days
            fcdatetime += timedelta(days=daycnt)
            fcdatetime = fcdatetime.replace(hour=0, minute=0, second=0, microsecond=0)

            fcdata = {TEMPERATURE: __get_temp(tmpsect),
                      DATETIME: fcdatetime}
            result[FORECAST].append(fcdata)
    return result


def __get_temp(section):
    """Get the forecasted temp from xml section."""
    try:
        return (float(section[MINTEMP]) +
                float(section[MAXTEMP])) / 2
    except (ValueError, TypeError, KeyError):
        return None


def __select_nearest_ws(xmldata, latitude, longitude):
    """Select the nearest weatherstation."""
    log.debug("__select_nearest_ws: latitude: %s, longitude: %s", latitude, longitude)
    dist = 0
    dist2 = 0
    loc_data = None

    try:
        ws_xml = xmldata[WEERGEGEVENS][ACTUEELWEER][WEERSTATIONS][WEERSTATION]
    except KeyError:
        log.warning("Missing section in Buienradar xmldata (%s)."
                    "Can happen 00:00-01:00 CE(S)T",
                    WEERSTATION)
        return None

    for wstation in ws_xml:
        wslat = float(wstation[LAT])
        wslon = float(wstation[LON])

        dist2 = vincenty((latitude, longitude), (wslat, wslon))
        log.debug("calc distance: %s: %s (latitude: %s, longitude: %s, wslat: %s, wslon: %s)",
                  wstation[STATIONNAME][TEXT],
                  dist2, latitude, longitude, wslat, wslon)
        if ((loc_data is None) or (dist2 < dist)):
            dist = dist2
            loc_data = wstation

    if loc_data is None:
        log.warning("No weatherstation selected; aborting...")
        return None
    else:
        log.debug("Selected station: code='%s', "
                  "name='%s', lat='%s', lon='%s'.",
                  loc_data[STATIONCODE],
                  loc_data[STATIONNAME][TEXT],
                  loc_data[LAT],
                  loc_data[LON])
        return loc_data
