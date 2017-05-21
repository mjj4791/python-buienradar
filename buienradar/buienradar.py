"""

"""
import requests
import logging
import xmltodict
from vincenty import vincenty

SUCCESS='success'
STATUS_CODE='status_code'
HEADERS='headers'
CONTENT='content'
MESSAGE='msg'
DATA='data'

CONF_ATTRIBUTION = "Data provided by buienradar.nl"
CONF_DATETIME = 'datetime'
CONF_STATIONNAME = 'stationname'
CONF_SYMBOL = 'symbol'
CONF_IMAGE = 'image'
CONF_HUMIDITY = 'humidity'
CONF_TEMPERATURE = 'temperature'
CONF_GROUNDTEMP = 'groundtemperature'
CONF_WINDSPEED = 'windspeed'
CONF_WINDFORCE = 'windforce'
CONF_WINDDIRECTION = 'winddirection'
CONF_WINDAZIMUTH = 'windazimuth'
CONF_PRESSURE = 'pressure'
CONF_VISIBILITY = 'visibility'
CONF_WINDGUST = 'windgust'
CONF_PRECIPITATION = 'precipitation'
CONF_IRRADIANCE = 'irradiance'
CONF_FORECAST = 'forecast'


# key names in buienradar xml:
CONF_BR_ROOT = 'buienradarnl'
CONF_BR_WEERGEGEVENS = 'weergegevens'
CONF_BR_ACTUEELWEER = 'actueel_weer'
CONF_BR_WEERSTATIONS = 'weerstations'
CONF_BR_WEERSTATION = 'weerstation'
CONF_BR_LAT = 'lat'
CONF_BR_LON = 'lon'
CONF_BR_STATIONCODE = 'stationcode'
CONF_BR_STATIONNAME = 'stationnaam'
CONF_BR_TEXT = '#text'
CONF_BR_ZIN = '@zin'
CONF_BR_FORECAST = 'verwachting_meerdaags'
CONF_BR_DAYFC = "dag-plus%d"
CONF_BR_MINTEMP = 'maxtemp'
CONF_BR_MAXTEMP = 'maxtempmax'

# Sensor types are defined like so:
# SENSOR_TYPES = { 'key': ['Display name',
#                          'unit of measurement',
#                          'key in buienradar xml'],}
SENSOR_TYPES = {
    CONF_STATIONNAME: 'stationnaam',
    CONF_SYMBOL: 'icoonactueel',
    CONF_HUMIDITY: 'luchtvochtigheid',
    CONF_TEMPERATURE: 'temperatuurGC',
    CONF_GROUNDTEMP: 'temperatuur10cm',
    CONF_WINDSPEED: 'windsnelheidMS',
    CONF_WINDFORCE: 'windsnelheidBF',
    CONF_WINDDIRECTION: 'windrichtingGR',
    CONF_WINDAZIMUTH: 'windrichting',
    CONF_PRESSURE: 'luchtdruk',
    CONF_VISIBILITY: 'zichtmeters',
    CONF_WINDGUST: 'windstotenMS',
    CONF_PRECIPITATION: 'regenMMPU',
    CONF_IRRADIANCE: 'zonintensiteitWM2',
}

log = logging.getLogger(__name__)
    

def get():
    """Get buienradar xml data and return results."""
    result={SUCCESS: False, MESSAGE: None}
    
    log.info("Retrieving xml weather data...")
    try:
        r = requests.get("https://xml.buienradar.nl/")
    
        result[SUCCESS] = (200==r.status_code)
        result[STATUS_CODE] = r.status_code
        result[HEADERS] = r.headers
        result[CONTENT] = r.content
    except requests.RequestException as ose:
        result[MESSAGE] = 'Error getting xml data. %s' % ose
        log.error(result[MESSAGE])
        
    return result


def parse(content=None, latitude=52.091579, longitude=5.119734):
    """Parse the buienradar xml data."""
    log.debug("parse: latitude: %s, longitude: %s", latitude, longitude)
    result={SUCCESS: False, MESSAGE: None, DATA: None}
    
    try:
        xmldata = xmltodict.parse(content)[CONF_BR_ROOT]
    except (ExpatError, IndexError) as err:
        result[MESSAGE]="Unable to parse content as xml."
        log.exception(result[MESSAGE])
        return result
    
    loc_data=__select_nearest_ws(xmldata, latitude, longitude)
    
    if loc_data:
        result[DATA] = {}
        for key, value in SENSOR_TYPES.items():
            result[DATA][key] = None
            try:
                sens_data = loc_data[value]
                if key == CONF_SYMBOL:
                    # update weather symbol & status text
                    result[DATA][key] = sens_data[CONF_BR_ZIN]
                    result[DATA][CONF_IMAGE] = sens_data[CONF_BR_TEXT]
                else:
                    if key == CONF_STATIONNAME:
                        result[DATA][key] = sens_data[CONF_BR_TEXT]
                    else:
                        # update all other data
                        result[DATA][key] = sens_data
            except KeyError:
                log.warning("Data element with key='%s' "
                            "not loaded from br data!", key)
        result[SUCCESS]=True
        log.debug("BR cached data: %s", result[DATA])
    else:
        result[MESSAGE]='No location selected.'
    
    return result

def __select_nearest_ws(xmldata, latitude, longitude):
    """Select the nearest weatherstation."""
    log.debug("__select_nearest_ws: latitude: %s, longitude: %s", latitude, longitude)
    dist = 0
    dist2 = 0
    loc_data = None

    xmldata_tmp = xmldata
    
    try:
        ws_xml=xmldata[CONF_BR_WEERGEGEVENS][CONF_BR_ACTUEELWEER][CONF_BR_WEERSTATIONS][CONF_BR_WEERSTATION]
    except:
        log.warning("Missing section in Buienradar xmldata (%s)."
                        "Can happen 00:00-01:00 CE(S)T",
                        CONF_BR_WEERSTATION)
        return None
        
    for wstation in ws_xml:
        wslat = float(wstation[CONF_BR_LAT])
        wslon = float(wstation[CONF_BR_LON])

        dist2 = vincenty((latitude, longitude), (wslat,wslon))
        log.debug("calc distance: %s: %s (latitude: %s, longitude: %s, wslat: %s, wslon: %s)", wstation[CONF_BR_STATIONNAME][CONF_BR_TEXT], dist2, latitude, longitude, wslat, wslon)
        if ((loc_data is None) or (dist2 < dist)):
            dist = dist2
            loc_data = wstation

    if loc_data is None:
        log.warning("No weatherstation selected; aborting...")
        return None
    else:
        log.debug("Selected station: code='%s', "
                      "name='%s', lat='%s', lon='%s'.",
                      loc_data[CONF_BR_STATIONCODE],
                      loc_data[CONF_BR_STATIONNAME][CONF_BR_TEXT],
                      loc_data[CONF_BR_LAT],
                      loc_data[CONF_BR_LON])
        return loc_data
