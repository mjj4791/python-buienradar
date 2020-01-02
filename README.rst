Python buienradar library
=========================

Library and CLI tools for interacting with buienradar xml/api.

- https://data.buienradar.nl/2.0/feed/json

and precipitation forecase from:

- https://gpsgadget.buienradar.nl/data/raintext?lat=<latitude>&lon=<longitude>

Old XMI-based APIs used before http://xml.buienradar.nl.

Requirements
------------

- Python 3.4 (or higher)


Description
-----------

This package is created as a library for the Home assistant buienradar component implementation. A CLI has been created mainly for debugging purposes but may be extended in the future for more real-world application if needed.

Installation
------------

.. code-block:: bash

    $ pip install buienradar

Usage
-----

.. code-block:: bash

    $ python -m buienradar -h
    Command line interface for buienradar library.

    Usage:
      buienradar [-v | -vv] [options]
      buienradar (-h | --help)
      buienradar --version

     Options:
      -h --help                 Show this screen.
      -v                        Increase verbosity.
      -vv                       Increase verbosity more.
      --version                 Show version.
      --longitude=<longitude>   Longitude to use [default: 5.119734]
      --latitude=<latitude>     Latitude to use [default: 52.091579]
      --timeframe=<timeframe>   Minutes to look ahead for
                                precipitation (5..120) [default: 60]
      --usexml                  Use the (old) XML API; will use JSON API otherwise.

    $ python -m buienradar
    {'distance': 4.235064, 'success': True, 'msg': None, 'data': {'condition': {'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/cc.png', 'condition': 'cloudy', 'exact': 'Heavily clouded', 'condcode': 'c', 'detailed': 'cloudy', 'exact_nl': 'Zwaar bewolkt'}, 'barometerfcname': 'Rain', 'barometerfc': 3, 'windgust': 12.2, 'attribution': 'Data provided by buienradar.nl', 'measured': datetime.datetime(2019, 3, 3, 20, 10, tzinfo=<DstTzInfo 'Europe/Amsterdam' CET+1:00:00 STD>), 'humidity': 80, 'rainlasthour': 0.1, 'temperature': 11.8, 'stationname': 'De Bilt (6260)', 'winddirection': 'Z', 'precipitation_forecast': {'timeframe': 60, 'average': 0, 'total': 0.0}, 'precipitation': 0.0, 'rainlast24hour': 3.9, 'forecast': [{'maxtemp': 9.0, 'condition': {'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/f.png', 'condition': 'rainy', 'exact': 'Alternatingly cloudy with some light rain', 'condcode': 'f', 'detailed': 'partlycloudy-light-rain', 'exact_nl': 'Afwisselend bewolkt met (mogelijk) wat lichte regen'}, 'rainchance': 70, 'temperature': 9.0, 'snow': 0, 'rain': 4.0, 'min_rain': 4.0, 'max_rain': 4.0, 'windforce': 7, 'sunchance': 40, 'datetime': datetime.datetime(2019, 3, 4, 0, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CET+1:00:00 STD>), 'winddirection': 'zw', 'mintemp': 8.0}, {'maxtemp': 0.0, 'condition': {'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/q.png', 'condition': 'rainy', 'exact': 'Heavily clouded with rain', 'condcode': 'q', 'detailed': 'rainy', 'exact_nl': 'Zwaar bewolkt en regen'}, 'rainchance': 70, 'temperature': 0.0, 'snow': 0, 'rain': 4.0, 'min_rain': 1.0, 'max_rain': 4.0, 'windforce': 4, 'sunchance': 10, 'datetime': datetime.datetime(2019, 3, 5, 0, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CET+1:00:00 STD>), 'winddirection': 'zw', 'mintemp': 4.0}, {'maxtemp': 0.0, 'condition': {'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/q.png', 'condition': 'rainy', 'exact': 'Heavily clouded with rain', 'condcode': 'q', 'detailed': 'rainy', 'exact_nl': 'Zwaar bewolkt en regen'}, 'rainchance': 90, 'temperature': 0.0, 'snow': 0, 'rain': 9.0, 'min_rain': 5.0, 'max_rain': 9.0, 'windforce': 4, 'sunchance': 10, 'datetime': datetime.datetime(2019, 3, 6, 0, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CET+1:00:00 STD>), 'winddirection': 'z', 'mintemp': 0.0}, {'maxtemp': 0.0, 'condition': {'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/f.png', 'condition': 'rainy', 'exact': 'Alternatingly cloudy with some light rain', 'condcode': 'f', 'detailed': 'partlycloudy-light-rain', 'exact_nl': 'Afwisselend bewolkt met (mogelijk) wat lichte regen'}, 'rainchance': 70, 'temperature': 0.0, 'snow': 0, 'rain': 5.0, 'min_rain': 2.0, 'max_rain': 5.0, 'windforce': 5, 'sunchance': 30, 'datetime': datetime.datetime(2019, 3, 7, 0, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CET+1:00:00 STD>), 'winddirection': 'zw', 'mintemp': 0.0}, {'maxtemp': 0.0, 'condition': {'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/f.png', 'condition': 'rainy', 'exact': 'Alternatingly cloudy with some light rain', 'condcode': 'f', 'detailed': 'partlycloudy-light-rain', 'exact_nl': 'Afwisselend bewolkt met (mogelijk) wat lichte regen'}, 'rainchance': 40, 'temperature': 0.0, 'snow': 0, 'rain': 2.0, 'min_rain': 0.0, 'max_rain': 2.0, 'windforce': 4, 'sunchance': 30, 'datetime': datetime.datetime(2019, 3, 8, 0, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CET+1:00:00 STD>), 'winddirection': 'w', 'mintemp': 0.0}], 'irradiance': 0, 'visibility': 22600, 'pressure': 997.2, 'groundtemperature': 11.3, 'feeltemperature': 9.2, 'windspeed': 7.2, 'windforce': 4, 'windazimuth': 187}}

    $ python -m buienradar -v
    INFO:__main__:Start...
    INFO:buienradar.buienradar:Getting buienradar JSON data for latitude=52.091579, longitude=5.119734
    INFO:buienradar.buienradar_json:Getting buienradar json data for latitude=52.091579, longitude=5.119734
    INFO:buienradar.buienradar_json:Retrieving  weather data (https://data.buienradar.nl/2.0/feed/json)...
    INFO:requests.packages.urllib3.connectionpool:Starting new HTTPS connection (1): data.buienradar.nl
    INFO:buienradar.buienradar_json:Retrieving  weather data (https://gpsgadget.buienradar.nl/data/raintext?lat=52.09&lon=5.12)...
    INFO:requests.packages.urllib3.connectionpool:Starting new HTTPS connection (1): gpsgadget.buienradar.nl
    INFO:buienradar.buienradar_json:Parse ws data: latitude: 52.091579, longitude: 5.119734
    INFO:__main__:result: {'data': {'temperature': 11.8, 'winddirection': 'Z', 'forecast': [{'temperature': 9.0, 'snow': 0, 'winddirection': 'zw', 'min_rain': 4.0, 'datetime': datetime.datetime(2019, 3, 4, 0, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CET+1:00:00 STD>), 'maxtemp': 9.0, 'max_rain': 4.0, 'rain': 4.0, 'condition': {'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/f.png', 'detailed': 'partlycloudy-light-rain', 'condition': 'rainy', 'exact_nl': 'Afwisselend bewolkt met (mogelijk) wat lichte regen', 'exact': 'Alternatingly cloudy with some light rain', 'condcode': 'f'}, 'windforce': 7, 'mintemp': 8.0, 'rainchance': 70, 'sunchance': 40}, {'temperature': 0.0, 'snow': 0, 'winddirection': 'zw', 'min_rain': 1.0, 'datetime': datetime.datetime(2019, 3, 5, 0, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CET+1:00:00 STD>), 'maxtemp': 0.0, 'max_rain': 4.0, 'rain': 4.0, 'condition': {'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/q.png', 'detailed': 'rainy', 'condition': 'rainy', 'exact_nl': 'Zwaar bewolkt en regen', 'exact': 'Heavily clouded with rain', 'condcode': 'q'}, 'windforce': 4, 'mintemp': 4.0, 'rainchance': 70, 'sunchance': 10}, {'temperature': 0.0, 'snow': 0, 'winddirection': 'z', 'min_rain': 5.0, 'datetime': datetime.datetime(2019, 3, 6, 0, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CET+1:00:00 STD>), 'maxtemp': 0.0, 'max_rain': 9.0, 'rain': 9.0, 'condition': {'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/q.png', 'detailed': 'rainy', 'condition': 'rainy', 'exact_nl': 'Zwaar bewolkt en regen', 'exact': 'Heavily clouded with rain', 'condcode': 'q'}, 'windforce': 4, 'mintemp': 0.0, 'rainchance': 90, 'sunchance': 10}, {'temperature': 0.0, 'snow': 0, 'winddirection': 'zw', 'min_rain': 2.0, 'datetime': datetime.datetime(2019, 3, 7, 0, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CET+1:00:00 STD>), 'maxtemp': 0.0, 'max_rain': 5.0, 'rain': 5.0, 'condition': {'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/f.png', 'detailed': 'partlycloudy-light-rain', 'condition': 'rainy', 'exact_nl': 'Afwisselend bewolkt met (mogelijk) wat lichte regen', 'exact': 'Alternatingly cloudy with some light rain', 'condcode': 'f'}, 'windforce': 5, 'mintemp': 0.0, 'rainchance': 70, 'sunchance': 30}, {'temperature': 0.0, 'snow': 0, 'winddirection': 'w', 'min_rain': 0.0, 'datetime': datetime.datetime(2019, 3, 8, 0, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CET+1:00:00 STD>), 'maxtemp': 0.0, 'max_rain': 2.0, 'rain': 2.0, 'condition': {'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/f.png', 'detailed': 'partlycloudy-light-rain', 'condition': 'rainy', 'exact_nl': 'Afwisselend bewolkt met (mogelijk) wat lichte regen', 'exact': 'Alternatingly cloudy with some light rain', 'condcode': 'f'}, 'windforce': 4, 'mintemp': 0.0, 'rainchance': 40, 'sunchance': 30}], 'feeltemperature': 9.2, 'precipitation': 0.0, 'visibility': 22600, 'windspeed': 7.2, 'humidity': 80, 'precipitation_forecast': {'timeframe': 60, 'total': 0.0, 'average': 0}, 'condition': {'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/cc.png', 'detailed': 'cloudy', 'condition': 'cloudy', 'exact_nl': 'Zwaar bewolkt', 'exact': 'Heavily clouded', 'condcode': 'c'}, 'rainlast24hour': 3.9, 'windazimuth': 187, 'irradiance': 0, 'barometerfcname': 'Rain', 'stationname': 'De Bilt (6260)', 'attribution': 'Data provided by buienradar.nl', 'barometerfc': 3, 'windgust': 12.2, 'measured': datetime.datetime(2019, 3, 3, 20, 10, tzinfo=<DstTzInfo 'Europe/Amsterdam' CET+1:00:00 STD>), 'rainlasthour': 0.1, 'pressure': 997.2, 'groundtemperature': 11.3, 'windforce': 4}, 'success': True, 'distance': 4.235064, 'msg': None}

    $ python -m buienradar -v --longitude=5.10 --latitude=52.1 --timeframe=45
    INFO:__main__:Start...
    INFO:buienradar.buienradar:Getting buienradar JSON data for latitude=52.1, longitude=5.1
    INFO:buienradar.buienradar_json:Getting buienradar json data for latitude=52.1, longitude=5.1
    INFO:buienradar.buienradar_json:Retrieving  weather data (https://data.buienradar.nl/2.0/feed/json)...
    INFO:requests.packages.urllib3.connectionpool:Starting new HTTPS connection (1): data.buienradar.nl
    INFO:buienradar.buienradar_json:Retrieving  weather data (https://gpsgadget.buienradar.nl/data/raintext?lat=52.1&lon=5.1)...
    INFO:requests.packages.urllib3.connectionpool:Starting new HTTPS connection (1): gpsgadget.buienradar.nl
    INFO:buienradar.buienradar_json:Parse ws data: latitude: 52.1, longitude: 5.1
    INFO:__main__:result: {'data': {'rainlast24hour': 3.9, 'rainlasthour': 0.1, 'visibility': 22600, 'barometerfcname': 'Rain', 'measured': datetime.datetime(2019, 3, 3, 20, 10, tzinfo=<DstTzInfo 'Europe/Amsterdam' CET+1:00:00 STD>), 'windazimuth': 187, 'winddirection': 'Z', 'windforce': 4, 'humidity': 80, 'barometerfc': 3, 'temperature': 11.8, 'windgust': 12.2, 'pressure': 997.2, 'precipitation': 0.0, 'precipitation_forecast': {'timeframe': 45, 'total': 0.0, 'average': 0.0}, 'attribution': 'Data provided by buienradar.nl', 'irradiance': 0, 'feeltemperature': 9.2, 'groundtemperature': 11.3, 'condition': {'condcode': 'c', 'exact': 'Heavily clouded', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/cc.png', 'detailed': 'cloudy', 'condition': 'cloudy', 'exact_nl': 'Zwaar bewolkt'}, 'stationname': 'De Bilt (6260)', 'windspeed': 7.2, 'forecast': [{'temperature': 9.0, 'winddirection': 'zw', 'snow': 0, 'maxtemp': 9.0, 'max_rain': 4.0, 'rainchance': 70, 'windforce': 7, 'datetime': datetime.datetime(2019, 3, 4, 0, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CET+1:00:00 STD>), 'mintemp': 8.0, 'condition': {'condcode': 'f', 'exact': 'Alternatingly cloudy with some light rain', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/f.png', 'detailed': 'partlycloudy-light-rain', 'condition': 'rainy', 'exact_nl': 'Afwisselend bewolkt met (mogelijk) wat lichte regen'}, 'sunchance': 40, 'rain': 4.0, 'min_rain': 4.0}, {'temperature': 0.0, 'winddirection': 'zw', 'snow': 0, 'maxtemp': 0.0, 'max_rain': 4.0, 'rainchance': 70, 'windforce': 4, 'datetime': datetime.datetime(2019, 3, 5, 0, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CET+1:00:00 STD>), 'mintemp': 4.0, 'condition': {'condcode': 'q', 'exact': 'Heavily clouded with rain', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/q.png', 'detailed': 'rainy', 'condition': 'rainy', 'exact_nl': 'Zwaar bewolkt en regen'}, 'sunchance': 10, 'rain': 4.0, 'min_rain': 1.0}, {'temperature': 0.0, 'winddirection': 'z', 'snow': 0, 'maxtemp': 0.0, 'max_rain': 9.0, 'rainchance': 90, 'windforce': 4, 'datetime': datetime.datetime(2019, 3, 6, 0, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CET+1:00:00 STD>), 'mintemp': 0.0, 'condition': {'condcode': 'q', 'exact': 'Heavily clouded with rain', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/q.png', 'detailed': 'rainy', 'condition': 'rainy', 'exact_nl': 'Zwaar bewolkt en regen'}, 'sunchance': 10, 'rain': 9.0, 'min_rain': 5.0}, {'temperature': 0.0, 'winddirection': 'zw', 'snow': 0, 'maxtemp': 0.0, 'max_rain': 5.0, 'rainchance': 70, 'windforce': 5, 'datetime': datetime.datetime(2019, 3, 7, 0, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CET+1:00:00 STD>), 'mintemp': 0.0, 'condition': {'condcode': 'f', 'exact': 'Alternatingly cloudy with some light rain', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/f.png', 'detailed': 'partlycloudy-light-rain', 'condition': 'rainy', 'exact_nl': 'Afwisselend bewolkt met (mogelijk) wat lichte regen'}, 'sunchance': 30, 'rain': 5.0, 'min_rain': 2.0}, {'temperature': 0.0, 'winddirection': 'w', 'snow': 0, 'maxtemp': 0.0, 'max_rain': 2.0, 'rainchance': 40, 'windforce': 4, 'datetime': datetime.datetime(2019, 3, 8, 0, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CET+1:00:00 STD>), 'mintemp': 0.0, 'condition': {'condcode': 'f', 'exact': 'Alternatingly cloudy with some light rain', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/f.png', 'detailed': 'partlycloudy-light-rain', 'condition': 'rainy', 'exact_nl': 'Afwisselend bewolkt met (mogelijk) wat lichte regen'}, 'sunchance': 30, 'rain': 2.0, 'min_rain': 0.0}]}, 'distance': 5.48199, 'msg': None, 'success': True}


Example python code:

.. code-block:: python

    from buienradar.buienradar import (get_data, parse_data)
    from buienradar.constants import (CONTENT, RAINCONTENT, SUCCESS)

    # minutes to look ahead for precipitation forecast
    # (5..120)
    timeframe = 45

    # gps-coordinates for the weather data
    latitude = 52.1
    longitude = 5.10

    result = get_data(latitude=latitude,
                      longitude=longitude,
                      )

    if result.get(SUCCESS):
        data = result[CONTENT]
        raindata = result[RAINCONTENT]

        result = parse_data(data, raindata, latitude, longitude, timeframe)

    print(result)

Example of returned data:

.. code-block:: python

    {
        'msg': None,
        'success': True,
        'distance': 5.48199
        'data': {
            'attribution': 'Data provided by buienradar.nl',
            'barometerfc': 4,
            'barometerfcname': 'Cloudy',
            'condition': {
                'exact_nl': 'Zwaar bewolkt en regen',
                'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/q.png',
                'condition': 'rainy',
                'detailed': 'rainy',
                'condcode': 'q',
                'exact': 'Heavily clouded with rain',
                'night': True
            },
            'feeltemperature': 8.8,
            'groundtemperature': 11.3,
            'humidity': 91,
            'irradiance': 67,
            'measured': datetime.datetime(2019, 3, 3, 12, 40, tzinfo=<DstTzInfo 'Europe/Amsterdam' CET+1:00:00 STD>),
            'precipitation': 0.1,
            'precipitation_forecast': {
                'average': 0.8,
                'total': 0.6,
                'timeframe': 45
            },
            'pressure': 1003.7,
            'rainlast24hour': 2.8,
            'rainlasthour': 0.2,
            'stationname': 'De Bilt (6260)',
            'temperature': 11.5,
            'visibility': 10800
            'windazimuth': 215,
            'winddirection': 'ZW',
            'windforce': 4,
            'windgust': 12.9,
            'windspeed': 7.4,
            'forecast': [
                {
                'condition': {
                    'condition': 'rainy',
                    'condcode': 'f',
                    'detailed': 'partlycloudy-light-rain',
                    'exact': 'Alternatingly cloudy with some light rain',
                    'night': False},
                    'exact_nl': 'Afwisselend bewolkt met (mogelijk) wat lichte regen',
                    'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/f.png',
                    'sunchance': 40,
                    'temperature': 9.0
                },
                'datetime': datetime.datetime(2019, 3, 4, 0, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CET+1:00:00 STD>),
                'max_rain': 4.0,
                'maxtemp': 9.0,
                'min_rain': 4.0,
                'mintemp': 8.0,
                'rain': 4.0,
                'rainchance': 70,
                'snow': 0,
                'winddirection': 'zw',
                'windforce': 7,
                , {} ...
            ]
        },
    }



Use the constants defined in the buienradar component to get the data from the returned dictionary:

- DISTANCE: Distance between the given GPS coordinates and the selected weather-station (m)
- MESSAGE: Error message with more info regarding what went wrong
- SUCCESS: Boolean indicating if data was retrieved ok
- *STATUS_CODE: Sometimes present in data, if a http-get was not successful*
- *HEADERS: Sometimes present in data, if a http-get was not successful*
- CONTENT: get the weather data returned from get_data request
- RAINCONTENT: get the rain forcast data returned from get_data request
- DATA: weather data for the selected weather-station

    - ATTRIBUTION: attribution to buienradar.nl
    - BAROMETERFC: a numerical value for the barometric forecast (only when using json API (default))
    - BAROMETERFCNAME: s textual value for the barometric forecast (only when using json API (default))

        - 0: no pressure data available
        - 1: Thunderstorms
        - 2: Stormy
        - 3: Rain
        - 4: Cloudy
        - 5: Unstable
        - 6: Stable
        - 7: Very dry

    - CONDITION: The current condition
        - CONDCODE: unique condition code (a-z)
        - CONDITION: condition

            - clear
            - cloudy
            - fog
            - rainy
            - snowy
            - lightning

        - DETAILED: more detailed condition

            - clear
            - partlycloudy
            - cloudy
            - partlycloudy-fog
            - partlycloudy-light-rain
            - partlycloudy-rain
            - light-rain
            - rainy
            - snowy-rainy
            - partlycloudy-light-snow
            - partlycloudy-snow
            - light-snow
            - snowy
            - partlycloudy-lightning
            - lightning

        - EXACT: the exact condition as reported (translated to english)
        - EXACTNL: the exact condition as reported
        - IMAGE: A symbol (url) for the current weather
        - NIGHTTIME: indicator if the condition is a daytime or nighttime condition

    - FEELTEMPERATURE: The feeltemperature (json only)
    - GROUNDTEMP: the current ground temperature (in C)
    - HUMIDITY: the relative humidity (%)
    - IRRADIANCE:  sun intensity in Watt per square meter (W/m2)
    - MEASURED: the time the data was retrieved
    - PRECIPITATION: the amount of precipitation/rain in mm/h
    - PRECIPITATION_FORECAST: information on forecasted precipitation

        - AVERAGE: the average expected precipitation (mm/h)
        - TOTAL: the total expected precipitation (mm)
        - TIMEFRAME: the time-frame for the forecasted precipitation (min)
    - PRESSURE: the sea-level air pressure in hPa
    - RAINLAST24HOUR: rainfall last 24 hours (json only)
    - RAINLASTHOUR: rain fall in the lat houd (json only)
    - STATIONNAME: the name of the selected meteo-station
    - TEMPERATURE: the current temperature (in C)
    - VISIBILITY:  visibility in meters (m)
    - WINDAZIMUTH: where the wind is coming from: N (North), Z (south), NO (North-East), etc.
    - WINDDIRECTION: where the wind is coming from in degrees, with true north at 0° and progressing clockwise
    - WINDFORCE: the wind speed/force in Bft
    - WINDGUST: the wind-speed of wind gusts (m/s)
    - WINDSPEED: the wind speed in m/s

    - FORECAST: array of forcasted days

        - CONDITION: the expected condition (see condition above)
        - DATETIME: date for the forcasted data
        - MAX_RAIN: the maximum expected rain (in mm)
        - MAX_TEMP: the maximum temperature (in C)
        - MIN_RAIN: the minimum expected rainfall (in mm)
        - MIN_TEMP: the minimum temperature (in C)
        - RAIN: the expected rain in (mm)
        - RAIN_CHANCE: the chance for rain (%)
        - SUN_CHANCE: the chance for sun (%)
        - SNOW: the expected snowfall (in cm) (NOTE: will always be 0 when using json API!)
        - TEMPERATURE: the temperature (in C)
        - WINDFORCE: the wind speed/force in Bft
