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
      --timeframe=<timeframe>   Seconds to look ahead for
                                precipitation [default: 3600]

    $ python -m buienradar


    $ python -m buienradar -v
    INFO:__main__:Start...
    INFO:buienradar.buienradar:Retrieving xml weather data (https://xml.buienradar.nl/)...
    INFO:buienradar.buienradar:Retrieving xml weather data (http://gadgets.buienradar.nl/data/raintext/?lat=52.091579&lon=5.119734)...
    INFO:__main__:Retrieved data:
    {'data': {'windspeed': '2.97', 'windazimuth': 'Z', 'pressure': '1006.81', 'visibility': '47000', 'attribution': 'Data provided by buienradar.nl', 'temperature': '20.0', 'windforce': '2', 'irradiance': '45', 'humidity': '46', 'precipitation_forecast': {'total': 0.0, 'average': 0.0, 'timeframe': 3600}, 'precipitation': '-', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/a.png', 'stationname': 'Meetstation De Bilt (6260)', 'windgust': '5.4', 'groundtemperature': '18.9', 'winddirection': '187', 'measured': '06/05/2017 20:50:00', 'forecast': [{'rain': 11.7, 'datetime': datetime.datetime(2017, 6, 6, 0, 0), 'temperature': 16.0, 'max_temp': 16.0, 'min_temp': 12.0, 'sun_chance': None, 'windforce': 5, 'rain_chance': 86}, {'rain': 2.1, 'datetime': datetime.datetime(2017, 6, 7, 0, 0), 'temperature': 17.0, 'max_temp': 17.0, 'min_temp': 12.0, 'sun_chance': None, 'windforce': 5, 'rain_chance': 47}, {'rain': None, 'datetime': datetime.datetime(2017, 6, 8, 0, 0), 'temperature': 23.0, 'max_temp': 23.0, 'min_temp': 13.0, 'sun_chance': None, 'windforce': 4, 'rain_chance': 13}, {'rain': 2.4, 'datetime': datetime.datetime(2017, 6, 9, 0, 0), 'temperature': 24.0, 'max_temp': 24.0, 'min_temp': 16.0, 'sun_chance': 32, 'windforce': 3, 'rain_chance': 52}, {'rain': 0.8, 'datetime': datetime.datetime(2017, 6, 10, 0, 0), 'temperature': 22.0, 'max_temp': 22.0, 'min_temp': 14.0, 'sun_chance': None, 'windforce': 4, 'rain_chance': 47}], 'symbol': 'Vrijwel onbewolkt (zonnig/helder)'}, 'msg': None, 'success': True, 'distance': 4.235064}


    $ python -m buienradar -v --longitude=5.10 --latitude=52.1 --timeframe=1800
    INFO:__main__:Start...
    INFO:buienradar.buienradar:Retrieving xml weather data (https://xml.buienradar.nl/)...
    INFO:buienradar.buienradar:Retrieving xml weather data (http://gadgets.buienradar.nl/data/raintext/?lat=52.1&lon=5.1)...
    INFO:__main__:Retrieved data:
    {'data': {'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/a.png', 'windspeed': '2.97', 'stationname': 'Meetstation De Bilt (6260)', 'irradiance': '45', 'temperature': '20.0', 'precipitation_forecast': {'average': 0.0, 'timeframe': 1800, 'total': 0.0}, 'pressure': '1006.81', 'visibility': '47000', 'windforce': '2', 'humidity': '46', 'windazimuth': 'Z', 'symbol': 'Vrijwel onbewolkt (zonnig/helder)', 'groundtemperature': '18.9', 'measured': '06/05/2017 20:50:00', 'precipitation': '-', 'winddirection': '187', 'windgust': '5.4', 'forecast': [{'rain': 11.7, 'temperature': 16.0, 'datetime': datetime.datetime(2017, 6, 6, 0, 0), 'max_temp': 16.0, 'min_temp': 12.0, 'rain_chance': 86, 'sun_chance': None, 'windforce': 5}, {'rain': 2.1, 'temperature': 17.0, 'datetime': datetime.datetime(2017, 6, 7, 0, 0), 'max_temp': 17.0, 'min_temp': 12.0, 'rain_chance': 47, 'sun_chance': None, 'windforce': 5}, {'rain': None, 'temperature': 23.0, 'datetime': datetime.datetime(2017, 6, 8, 0, 0), 'max_temp': 23.0, 'min_temp': 13.0, 'rain_chance': 13, 'sun_chance': None, 'windforce': 4}, {'rain': 2.4, 'temperature': 24.0, 'datetime': datetime.datetime(2017, 6, 9, 0, 0), 'max_temp': 24.0, 'min_temp': 16.0, 'rain_chance': 52, 'sun_chance': 32, 'windforce': 3}, {'rain': 0.8, 'temperature': 22.0, 'datetime': datetime.datetime(2017, 6, 10, 0, 0), 'max_temp': 22.0, 'min_temp': 14.0, 'rain_chance': 47, 'sun_chance': None, 'windforce': 4}], 'attribution': 'Data provided by buienradar.nl'}, 'success': True, 'distance': 4.235064, 'msg': None}


Example python code:

.. code-block:: python

    from buienradar.buienradar import (get_data, DATA, MESSAGE,
                                       SUCCESS, TEMPERATURE)
    
    result = get_data(latitude=<your latitude>,
                      longitude=<your longitude>,
                      timeframe=<yourtimeframe>,
                     )
        if result.get(SUCCESS):
            print(result.get(DATA))
            print("Current temperature: %s" % result.get(DATA).get(TEMPERATURE))
        else:
            print("Unable to retrieve data from Buienradar. (Msg: %s)",
                  result.get(MESSAGE))


Example of returned data:

.. code-block:: python

    {
        'distance': 4.235064, 
        'msg': None, 
        'success': True
        'data': {
                 'precipitation_forecast': {
                                   'total': 0.0,
                                   'timeframe': 3600,
                                   'average': 0.0
                                  },
                 'measured': '06/05/2017 17:00:00',
                 'irradiance': '596',
                 'symbol': 'Vrijwel onbewolkt (zonnig/helder)',
                 'forecast': [
                              {'rain': 11.7,
                               'datetime': datetime.datetime(2017, 6, 6, 0, 0),
                               'windforce': 5,
                               'min_temp': 12.0,
                               'sun_chance': None,
                               'max_temp': 16.0,
                               'rain_chance': 86,
                               'temperature': 16.0
                              },
                              ...
                             ],
                 'visibility': '40900',
                 'windgust': '9.8',
                 'temperature': '21.6',
                 'pressure': '1009.62',
                 'groundtemperature': '23.6',
                 'stationname': 'Meetstation De Bilt (6260)',
                 'attribution': 'Data provided by buienradar.nl',
                 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/a.png',
                 'humidity': '42',
                 'windazimuth': 'ZZW',
                 'windspeed': '5.36',
                 'winddirection': '200',
                 'windforce': '3',
                 'precipitation': '-'
        },
    }

Use the constants defined in the buienradar component to get the data from the returned dictionary:

- DISTANCE: Distance between the given GPS coordinates and the selected weather-station (m)
- MESSAGE: Error message with more info regarding what went wrong
- SUCCESS: Boolean indicating if data was retrieved ok
- *STATUS_CODE: Sometimes present in data, if a http-get was not successful*
- *HEADERS: Sometimes present in data, if a http-get was not successful*
- *CONTENT: Sometimes present in data, if a http-get was not successful*
- PRECIPITATION_FORECAST: information on forecasted precipitation

  - AVERAGE: the average expected precipitation mm/h)
  - TOTAL: the total expected precipitation (mm)
  - TIMEFRAME: the time-frame for the forecasted precipitation (s)
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
