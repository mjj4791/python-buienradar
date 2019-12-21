"""Constants to be imported elsewhere."""
# sections in returned structure
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
BAROMETERFC = 'barometerfc'               # new (json only!)
BAROMETERFCNAME = 'barometerfcname'       # new (json only!)
BAROMETERFCNAMENL = 'barometerfcnamenl'   # new (json only!)
CONDCODE = 'condcode'
CONDITION = 'condition'
DATETIME = 'datetime'
DETAILED = 'detailed'
EXACT = 'exact'
EXACTNL = 'exact_nl'
DISTANCE = 'distance'
FEELTEMPERATURE = 'feeltemperature'       # new (json only!)
FORECAST = 'forecast'
GROUNDTEMP = 'groundtemperature'
HUMIDITY = 'humidity'
IMAGE = 'image'
IRRADIANCE = 'irradiance'
MEASURED = 'measured'
NIGHTTIME = 'night'
PRECIPITATION = 'precipitation'
PRECIPITATION_FORECAST = 'precipitation_forecast'
PRESSURE = 'pressure'
RAINLAST24HOUR = 'rainlast24hour'        # new (json only!)
RAINLASTHOUR = 'rainlasthour'            # new (json only!)
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
SNOW = 'snow'                           # depricated; no longer in json API!
MIN_RAIN = 'minrain'                    # new in json API
MAX_RAIN = 'maxrain'                    # new in json API

# keys in forecasted precipitation data:
AVERAGE = 'average'
TIMEFRAME = 'timeframe'
TOTAL = 'total'

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
