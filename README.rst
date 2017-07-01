Python buienradar library
=========================

Library and CLI tools for interacting with buienradar xml/api.

- http://xml.buienradar.nl
- http://api.buienradar.nl

and precipitation forecase from: 

- https://gpsgadget.buienradar.nl/data/raintext?lat=<latitude>&lon=<longitude>


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

    $ python -m buienradar
    {'distance': 4.235064, 'data': {'winddirection': '120', 'irradiance': '-', 'attribution': 'Data provided by buienradar.nl', 'groundtemperature': '18.1', 'symbol': 'Vrijwel onbewolkt (zonnig/helder)', 'windforce': '1', 'stationname': 'De Bilt (6260)', 'precipitation_forecast': {'total': 0.0, 'timeframe': 60, 'average': 0.0}, 'pressure': '1014.51', 'forecast': [{'datetime': datetime.datetime(2017, 6, 22, 0, 0), 'temperature': 29.0, 'min_temp': 20.0, 'windforce': 4, 'sun_chance': 68, 'max_temp': 29.0, 'rain_chance': 47, 'rain': 1.6}, {'datetime': datetime.datetime(2017, 6, 23, 0, 0), 'temperature': 24.0, 'min_temp': 15.0, 'windforce': 4, 'sun_chance': 63, 'max_temp': 24.0, 'rain_chance': 3, 'rain': None}, {'datetime': datetime.datetime(2017, 6, 24, 0, 0), 'temperature': 20.0, 'min_temp': 17.0, 'windforce': 4, 'sun_chance': None, 'max_temp': 20.0, 'rain_chance': 38, 'rain': 0.7}, {'datetime': datetime.datetime(2017, 6, 25, 0, 0), 'temperature': 19.0, 'min_temp': 14.0, 'windforce': 3, 'sun_chance': None, 'max_temp': 19.0, 'rain_chance': 25, 'rain': None}, {'datetime': datetime.datetime(2017, 6, 26, 0, 0), 'temperature': 21.0, 'min_temp': 12.0, 'windforce': 3, 'sun_chance': 94, 'max_temp': 21.0, 'rain_chance': 11, 'rain': None}], 'windspeed': '1.34', 'precipitation': '-', 'temperature': '21.0', 'measured': '06/21/2017 22:30:00', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/aa.png', 'visibility': '32000', 'humidity': '81', 'windazimuth': 'OZO', 'windgust': '1.9'}, 'success': True, 'msg': None}

    $ python -m buienradar -v
    INFO:__main__:Start...
    INFO:buienradar.buienradar:Getting buienradar data for latitude=52.091579, longitude=5.119734
    INFO:buienradar.buienradar:Retrieving xml weather data (https://xml.buienradar.nl/)...
    INFO:buienradar.buienradar:Retrieving xml weather data (http://gadgets.buienradar.nl/data/raintext/?lat=52.091579&lon=5.119734)...
    INFO:__main__:result: {'success': True, 'distance': 4.235064, 'msg': None, 'data': {'windspeed': '1.01', 'irradiance': '-', 'temperature': '20.7', 'pressure': '1014.51', 'winddirection': '111', 'humidity': '82', 'windgust': '1.9', 'visibility': '31500', 'forecast': [{'min_temp': 20.0, 'rain_chance': 47, 'sun_chance': 42, 'temperature': 29.0, 'rain': 1.6, 'windforce': 4, 'datetime': datetime.datetime(2017, 6, 22, 0, 0), 'max_temp': 29.0}, {'min_temp': 15.0, 'rain_chance': 3, 'sun_chance': None, 'temperature': 24.0, 'rain': None, 'windforce': 4, 'datetime': datetime.datetime(2017, 6, 23, 0, 0), 'max_temp': 24.0}, {'min_temp': 17.0, 'rain_chance': 38, 'sun_chance': None, 'temperature': 20.0, 'rain': 0.7, 'windforce': 4, 'datetime': datetime.datetime(2017, 6, 24, 0, 0), 'max_temp': 20.0}, {'min_temp': 14.0, 'rain_chance': 25, 'sun_chance': None, 'temperature': 19.0, 'rain': None, 'windforce': 3, 'datetime': datetime.datetime(2017, 6, 25, 0, 0), 'max_temp': 19.0}, {'min_temp': 12.0, 'rain_chance': 11, 'sun_chance': 21, 'temperature': 21.0, 'rain': None, 'windforce': 3, 'datetime': datetime.datetime(2017, 6, 26, 0, 0), 'max_temp': 21.0}], 'precipitation': '-', 'attribution': 'Data provided by buienradar.nl', 'windforce': '1', 'stationname': 'De Bilt (6260)', 'groundtemperature': '18.1', 'precipitation_forecast': {'total': 0.0, 'average': 0.0, 'timeframe': 60}, 'windazimuth': 'OZO', 'symbol': 'Vrijwel onbewolkt (zonnig/helder)', 'measured': '06/21/2017 22:40:00', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/aa.png'}}

    $ python -m buienradar -v --longitude=5.10 --latitude=52.1 --timeframe=45
    INFO:__main__:Start...
    INFO:buienradar.buienradar:Getting buienradar data for latitude=52.1, longitude=5.1
    INFO:buienradar.buienradar:Retrieving xml weather data (https://xml.buienradar.nl/)...
    INFO:buienradar.buienradar:Retrieving xml weather data (http://gadgets.buienradar.nl/data/raintext/?lat=52.1&lon=5.1)...
    INFO:__main__:result: {'msg': None, 'distance': 5.48199, 'success': True, 'data': {'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/aa.png', 'symbol': 'Vrijwel onbewolkt (zonnig/helder)', 'temperature': '20.7', 'humidity': '82', 'windazimuth': 'OZO', 'attribution': 'Data provided by buienradar.nl', 'visibility': '31500', 'groundtemperature': '18.1', 'precipitation_forecast': {'average': 0.0, 'timeframe': 45, 'total': 0.0}, 'precipitation': '-', 'windforce': '1', 'pressure': '1014.51', 'windgust': '1.9', 'irradiance': '-', 'forecast': [{'max_temp': 29.0, 'rain': 1.6, 'rain_chance': 47, 'sun_chance': 42, 'temperature': 29.0, 'min_temp': 20.0, 'windforce': 4, 'datetime': datetime.datetime(2017, 6, 22, 0, 0)}, {'max_temp': 24.0, 'rain': None, 'rain_chance': 3, 'sun_chance': None, 'temperature': 24.0, 'min_temp': 15.0, 'windforce': 4, 'datetime': datetime.datetime(2017, 6, 23, 0, 0)}, {'max_temp': 20.0, 'rain': 0.7, 'rain_chance': 38, 'sun_chance': None, 'temperature': 20.0, 'min_temp': 17.0, 'windforce': 4, 'datetime': datetime.datetime(2017, 6, 24, 0, 0)}, {'max_temp': 19.0, 'rain': None, 'rain_chance': 25, 'sun_chance': None, 'temperature': 19.0, 'min_temp': 14.0, 'windforce': 3, 'datetime': datetime.datetime(2017, 6, 25, 0, 0)}, {'max_temp': 21.0, 'rain': None, 'rain_chance': 11, 'sun_chance': 21, 'temperature': 21.0, 'min_temp': 12.0, 'windforce': 3, 'datetime': datetime.datetime(2017, 6, 26, 0, 0)}], 'measured': '06/21/2017 22:40:00', 'stationname': 'De Bilt (6260)', 'winddirection': '111', 'windspeed': '1.01'}}


Example python code:

.. code-block:: python

    from buienradar.buienradar import (get_data, parse_data,
                                       CONTENT, RAINCONTENT, SUCCESS)

    # minutes to look ahead for precipitation forecast
    # (5..120)
    timeframe = 60

    # gps-coordinates for the weather data
    latitude = 51.50
    longitude = 6.20

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
        'distance': 4.235064,
        'data': {
            'winddirection': OZO,
            'irradiance': 0,
            'attribution': 'Data provided by buienradar.nl',
            'groundtemperature': 18.1,
            'symbol': 'Vrijwel onbewolkt (zonnig/helder)',
            'windforce': 1,
            'stationname': 'De Bilt (6260)',
            'precipitation_forecast': {
                'total': 0.0,
                'timeframe': 60,
                'average': 0.0
            },
            'pressure': 1014.51,
            'forecast': [
                {'datetime': datetime.datetime(2017, 6, 22, 0, 0),
                'temperature': 29.0,
                'min_temp': 20.0,
                'windforce': 4,
                'sun_chance': 68,
                'max_temp': 29.0,
                'rain_chance': 47,
                'rain': 1.6
                },
            ...
            ],
            'windspeed': 1.34,
            'precipitation': 0.0,
            'temperature': 21.0,
            'measured': '06/21/2017 22:30:00',
            'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/aa.png',
            'visibility': 32000,
            'humidity': 81,
            'windazimuth': 120,
            'windgust': 1.9
        },
        'success': True,
        'msg': None
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

  - MEASURED: the time the data was retrieved
  - IRRADIANCE:  sun intensity in Watt per square meter (W/m2)
  - SYMBOL: a text describing for the current weather.
  - FORECAST: array of forcasted days
  
    - RAIN: the expected rain in mm/h
    - DATETIME: date for the forcasted data
    - WINDFORCE: the wind speed/force in Bft
    - MIN_TEMP: the minimum temperature (in C)
    - SUN_CHANCE: the chance for sun (%)
    - MAX_TEMP: the maximum temperature (in C)
    - RAIN_CHANCE: the chance for rain (%)
    - TEMPERATURE: the temperature (in C)
- VISIBILITY:  visibility in meters (m)
- WINDGUST: the wind-speed of wind gusts (m/s)
- TEMPERATURE: the current temperature (in C)
- PRESSURE: the sea-level air pressure in hPa
- GROUNDTEMP: the current ground temperature (in C)
- STATIONNAME: the name of the selected meteo-station
- ATTRIBUTION: attribution to buienradar.nl
- IMAGE: A symbol for the current weather
- HUMIDITY: the relative humidity (%)
- WINDAZIMUTH: where the wind is coming from: N (North), Z (south), NO (North-East), etc.
- WINDSPEED: the wind speed in m/s
- WINDDIRECTION: where the wind is coming from in degrees, with true north at 0° and progressing clockwise
- WINDFORCE: the wind speed/force in Bft
- PRECIPITATION: the amount of precipitation/rain in mm/h
- PRECIPITATION_FORECAST: information on forecasted precipitation

  - AVERAGE: the average expected precipitation mm/h)
  - TOTAL: the total expected precipitation (mm)
  - TIMEFRAME: the time-frame for the forecasted precipitation (s)
