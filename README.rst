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
    {'data': {'irradiance': 0, 'symbol': 'Zwaar bewolkt', 'measured': datetime.datetime(2017, 7, 26, 22, 20, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'groundtemperature': 18.1, 'winddirection': 'ZW', 'windgust': 6.8, 'humidity': 91, 'forecast': [{'min_temp': 16.0, 'rain': 0.0, 'datetime': datetime.datetime(2017, 7, 27, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'temperature': 21.0, 'rain_chance': 24, 'windforce': 3, 'sun_chance': 0, 'max_temp': 21.0}, {'min_temp': 14.0, 'rain': 1.6, 'datetime': datetime.datetime(2017, 7, 28, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'temperature': 21.0, 'rain_chance': 56, 'windforce': 4, 'sun_chance': 0, 'max_temp': 21.0}, {'min_temp': 15.0, 'rain': 4.1, 'datetime': datetime.datetime(2017, 7, 29, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'temperature': 21.0, 'rain_chance': 52, 'windforce': 4, 'sun_chance': 0, 'max_temp': 21.0}, {'min_temp': 16.0, 'rain': 3.4, 'datetime': datetime.datetime(2017, 7, 30, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'temperature': 22.0, 'rain_chance': 49, 'windforce': 3, 'sun_chance': 29, 'max_temp': 22.0}, {'min_temp': 13.0, 'rain': 0.0, 'datetime': datetime.datetime(2017, 7, 31, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'temperature': 24.0, 'rain_chance': 20, 'windforce': 3, 'sun_chance': 0, 'max_temp': 24.0}], 'precipitation': 0.0, 'pressure': 1007.21, 'attribution': 'Data provided by buienradar.nl', 'stationname': 'De Bilt (6260)', 'windspeed': 3.63, 'temperature': 18.1, 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/cc.png', 'windforce': 3, 'visibility': 6110, 'precipitation_forecast': {'average': 0.0, 'total': 0.0, 'timeframe': 60}, 'windazimuth': 229}, 'msg': None, 'distance': 4.235064, 'success': True}

    $ python -m buienradar -v
    INFO:__main__:Start...
    INFO:buienradar.buienradar:Getting buienradar data for latitude=52.091579, longitude=5.119734
    INFO:buienradar.buienradar:Retrieving xml weather data (https://xml.buienradar.nl/)...
    INFO:buienradar.buienradar:Retrieving xml weather data (http://gadgets.buienradar.nl/data/raintext/?lat=52.091579&lon=5.119734)...
    INFO:buienradar.buienradar:Parse ws data: latitude: 52.091579, longitude: 5.119734
    INFO:__main__:result: {'data': {'irradiance': 0, 'precipitation': 0.0, 'visibility': 6110, 'humidity': 91, 'measured': datetime.datetime(2017, 7, 26, 22, 20, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'symbol': 'Zwaar bewolkt', 'groundtemperature': 18.1, 'forecast': [{'sun_chance': 0, 'windforce': 3, 'min_temp': 16.0, 'temperature': 21.0, 'rain': 0.0, 'datetime': datetime.datetime(2017, 7, 27, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'max_temp': 21.0, 'rain_chance': 24}, {'sun_chance': 0, 'windforce': 4, 'min_temp': 14.0, 'temperature': 21.0, 'rain': 1.6, 'datetime': datetime.datetime(2017, 7, 28, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'max_temp': 21.0, 'rain_chance': 56}, {'sun_chance': 0, 'windforce': 4, 'min_temp': 15.0, 'temperature': 21.0, 'rain': 4.1, 'datetime': datetime.datetime(2017, 7, 29, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'max_temp': 21.0, 'rain_chance': 52}, {'sun_chance': 29, 'windforce': 3, 'min_temp': 16.0, 'temperature': 22.0, 'rain': 3.4, 'datetime': datetime.datetime(2017, 7, 30, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'max_temp': 22.0, 'rain_chance': 49}, {'sun_chance': 0, 'windforce': 3, 'min_temp': 13.0, 'temperature': 24.0, 'rain': 0.0, 'datetime': datetime.datetime(2017, 7, 31, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'max_temp': 24.0, 'rain_chance': 20}], 'temperature': 18.1, 'windforce': 3, 'windazimuth': 229, 'windgust': 6.8, 'precipitation_forecast': {'total': 0.0, 'timeframe': 60, 'average': 0.0}, 'windspeed': 3.63, 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/cc.png', 'winddirection': 'ZW', 'pressure': 1007.21, 'attribution': 'Data provided by buienradar.nl', 'stationname': 'De Bilt (6260)'}, 'distance': 4.235064, 'msg': None, 'success': True}
    {'data': {'irradiance': 0, 'precipitation': 0.0, 'visibility': 6110, 'humidity': 91, 'measured': datetime.datetime(2017, 7, 26, 22, 20, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'symbol': 'Zwaar bewolkt', 'groundtemperature': 18.1, 'forecast': [{'sun_chance': 0, 'windforce': 3, 'min_temp': 16.0, 'temperature': 21.0, 'rain': 0.0, 'datetime': datetime.datetime(2017, 7, 27, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'max_temp': 21.0, 'rain_chance': 24}, {'sun_chance': 0, 'windforce': 4, 'min_temp': 14.0, 'temperature': 21.0, 'rain': 1.6, 'datetime': datetime.datetime(2017, 7, 28, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'max_temp': 21.0, 'rain_chance': 56}, {'sun_chance': 0, 'windforce': 4, 'min_temp': 15.0, 'temperature': 21.0, 'rain': 4.1, 'datetime': datetime.datetime(2017, 7, 29, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'max_temp': 21.0, 'rain_chance': 52}, {'sun_chance': 29, 'windforce': 3, 'min_temp': 16.0, 'temperature': 22.0, 'rain': 3.4, 'datetime': datetime.datetime(2017, 7, 30, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'max_temp': 22.0, 'rain_chance': 49}, {'sun_chance': 0, 'windforce': 3, 'min_temp': 13.0, 'temperature': 24.0, 'rain': 0.0, 'datetime': datetime.datetime(2017, 7, 31, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'max_temp': 24.0, 'rain_chance': 20}], 'temperature': 18.1, 'windforce': 3, 'windazimuth': 229, 'windgust': 6.8, 'precipitation_forecast': {'total': 0.0, 'timeframe': 60, 'average': 0.0}, 'windspeed': 3.63, 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/cc.png', 'winddirection': 'ZW', 'pressure': 1007.21, 'attribution': 'Data provided by buienradar.nl', 'stationname': 'De Bilt (6260)'}, 'distance': 4.235064, 'msg': None, 'success': True}

    $ python -m buienradar -v --longitude=5.10 --latitude=52.1 --timeframe=45
    INFO:__main__:Start...
    INFO:buienradar.buienradar:Getting buienradar data for latitude=52.1, longitude=5.1
    INFO:buienradar.buienradar:Retrieving xml weather data (https://xml.buienradar.nl/)...
    INFO:buienradar.buienradar:Retrieving xml weather data (http://gadgets.buienradar.nl/data/raintext/?lat=52.1&lon=5.1)...
    INFO:buienradar.buienradar:Parse ws data: latitude: 52.1, longitude: 5.1
    INFO:__main__:result: {'distance': 5.48199, 'data': {'attribution': 'Data provided by buienradar.nl', 'windspeed': 4.0, 'humidity': 90, 'precipitation': 0.0, 'pressure': 1007.21, 'stationname': 'De Bilt (6260)', 'groundtemperature': 18.0, 'temperature': 18.2, 'visibility': 10300, 'irradiance': 0, 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/cc.png', 'windforce': 3, 'forecast': [{'rain_chance': 24, 'min_temp': 16.0, 'temperature': 21.0, 'sun_chance': 0, 'datetime': datetime.datetime(2017, 7, 27, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'max_temp': 21.0, 'rain': 0.0, 'windforce': 3}, {'rain_chance': 56, 'min_temp': 14.0, 'temperature': 21.0, 'sun_chance': 0, 'datetime': datetime.datetime(2017, 7, 28, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'max_temp': 21.0, 'rain': 1.6, 'windforce': 4}, {'rain_chance': 52, 'min_temp': 15.0, 'temperature': 21.0, 'sun_chance': 0, 'datetime': datetime.datetime(2017, 7, 29, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'max_temp': 21.0, 'rain': 4.1, 'windforce': 4}, {'rain_chance': 49, 'min_temp': 16.0, 'temperature': 22.0, 'sun_chance': 29, 'datetime': datetime.datetime(2017, 7, 30, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'max_temp': 22.0, 'rain': 3.4, 'windforce': 3}, {'rain_chance': 20, 'min_temp': 13.0, 'temperature': 24.0, 'sun_chance': 0, 'datetime': datetime.datetime(2017, 7, 31, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'max_temp': 24.0, 'rain': 0.0, 'windforce': 3}], 'windgust': 7.4, 'measured': datetime.datetime(2017, 7, 26, 22, 30, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'winddirection': 'ZW', 'symbol': 'Zwaar bewolkt', 'windazimuth': 219, 'precipitation_forecast': {'total': 0.0, 'average': 0.0, 'timeframe': 45}}, 'success': True, 'msg': None}
    {'distance': 5.48199, 'data': {'attribution': 'Data provided by buienradar.nl', 'windspeed': 4.0, 'humidity': 90, 'precipitation': 0.0, 'pressure': 1007.21, 'stationname': 'De Bilt (6260)', 'groundtemperature': 18.0, 'temperature': 18.2, 'visibility': 10300, 'irradiance': 0, 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/cc.png', 'windforce': 3, 'forecast': [{'rain_chance': 24, 'min_temp': 16.0, 'temperature': 21.0, 'sun_chance': 0, 'datetime': datetime.datetime(2017, 7, 27, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'max_temp': 21.0, 'rain': 0.0, 'windforce': 3}, {'rain_chance': 56, 'min_temp': 14.0, 'temperature': 21.0, 'sun_chance': 0, 'datetime': datetime.datetime(2017, 7, 28, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'max_temp': 21.0, 'rain': 1.6, 'windforce': 4}, {'rain_chance': 52, 'min_temp': 15.0, 'temperature': 21.0, 'sun_chance': 0, 'datetime': datetime.datetime(2017, 7, 29, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'max_temp': 21.0, 'rain': 4.1, 'windforce': 4}, {'rain_chance': 49, 'min_temp': 16.0, 'temperature': 22.0, 'sun_chance': 29, 'datetime': datetime.datetime(2017, 7, 30, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'max_temp': 22.0, 'rain': 3.4, 'windforce': 3}, {'rain_chance': 20, 'min_temp': 13.0, 'temperature': 24.0, 'sun_chance': 0, 'datetime': datetime.datetime(2017, 7, 31, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'max_temp': 24.0, 'rain': 0.0, 'windforce': 3}], 'windgust': 7.4, 'measured': datetime.datetime(2017, 7, 26, 22, 30, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'winddirection': 'ZW', 'symbol': 'Zwaar bewolkt', 'windazimuth': 219, 'precipitation_forecast': {'total': 0.0, 'average': 0.0, 'timeframe': 45}}, 'success': True, 'msg': None}


Example python code:

.. code-block:: python

    from buienradar.buienradar import (get_data, parse_data,
                                       CONTENT, RAINCONTENT, SUCCESS)

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
        'distance': 5.48199, 
        'data': {
            'attribution': 'Data provided by buienradar.nl', 
            'windspeed': 4.0, 
            'humidity': 90, 
            'precipitation': 0.0, 
            'pressure': 1007.21, 
            'stationname': 'De Bilt (6260)', 
            'groundtemperature': 18.0, 
            'temperature': 18.2, 
            'visibility': 10300, 
            'irradiance': 0, 
            'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/cc.png', 
            'windforce': 3, 
            'forecast': [
                {'rain_chance': 24, 
                'min_temp': 16.0, 
                'temperature': 21.0, 
                'sun_chance': 0, 
                'datetime': datetime.datetime(2017, 7, 27, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 
                'max_temp': 21.0, 
                'rain': 0.0, 
                'windforce': 3}, 
                ...
                ], 
            'windgust': 7.4, 
            'measured': datetime.datetime(2017, 7, 26, 22, 30, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 
            'winddirection': 'ZW', 
            'symbol': 'Zwaar bewolkt', 
            'windazimuth': 219, 
            'precipitation_forecast': {
                'total': 0.0, 
                'average': 0.0, 
                'timeframe': 45}
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
