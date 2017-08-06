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
    {'data': {'winddirection': 'ZZO', 'temperature': 13.3, 'forecast': [{'datetime': datetime.datetime(2017, 8, 7, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'rainchance': 0, 'condition': {'exact_nl': 'Mix van opklaringen en middelbare of lage bewolking', 'exact': 'Mix of clear and medium or low clouds', 'condcode': 'b', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/b.png', 'condition': 'cloudy', 'detailed': 'partlycloudy'}, 'snow': 0.0, 'temperature': 23.0, 'sunchance': 60, 'mintemp': 10.0, 'windforce': 3, 'maxtemp': 23.0, 'rain': 0.0}, {'datetime': datetime.datetime(2017, 8, 8, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'rainchance': 80, 'condition': {'exact_nl': 'Zwaar bewolkt en regen', 'exact': 'Heavily clouded with rain', 'condcode': 'q', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/q.png', 'condition': 'rainy', 'detailed': 'rainy'}, 'snow': 0.0, 'temperature': 20.0, 'sunchance': 20, 'mintemp': 13.0, 'windforce': 3, 'maxtemp': 20.0, 'rain': 6.0}, {'datetime': datetime.datetime(2017, 8, 9, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'rainchance': 80, 'condition': {'exact_nl': 'Afwisselend bewolkt met (mogelijk) wat lichte regen', 'exact': 'Alternatingly cloudy with some light rain', 'condcode': 'f', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/f.png', 'condition': 'rainy', 'detailed': 'partlycloudy-light-rain'}, 'snow': 0.0, 'temperature': 19.0, 'sunchance': 30, 'mintemp': 12.0, 'windforce': 3, 'maxtemp': 19.0, 'rain': 6.0}, {'datetime': datetime.datetime(2017, 8, 10, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'rainchance': 80, 'condition': {'exact_nl': 'Afwisselend bewolkt met (mogelijk) wat lichte regen', 'exact': 'Alternatingly cloudy with some light rain', 'condcode': 'f', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/f.png', 'condition': 'rainy', 'detailed': 'partlycloudy-light-rain'}, 'snow': 0.0, 'temperature': 17.0, 'sunchance': 30, 'mintemp': 11.0, 'windforce': 3, 'maxtemp': 17.0, 'rain': 12.0}, {'datetime': datetime.datetime(2017, 8, 11, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'rainchance': 60, 'condition': {'exact_nl': 'Afwisselend bewolkt met (mogelijk) wat lichte regen', 'exact': 'Alternatingly cloudy with some light rain', 'condcode': 'f', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/f.png', 'condition': 'rainy', 'detailed': 'partlycloudy-light-rain'}, 'snow': 0.0, 'temperature': 17.0, 'sunchance': 30, 'mintemp': 11.0, 'windforce': 4, 'maxtemp': 17.0, 'rain': 8.0}], 'precipitation': 0.0, 'stationname': 'De Bilt (6260)', 'groundtemperature': 10.8, 'measured': datetime.datetime(2017, 8, 6, 22, 40, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'irradiance': 0, 'pressure': 1022.32, 'condition': {'exact_nl': 'Zwaar bewolkt', 'exact': 'Heavily clouded', 'condcode': 'c', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/cc.png', 'condition': 'cloudy', 'detailed': 'cloudy'}, 'windazimuth': 162, 'windgust': 1.3, 'precipitation_forecast': {'total': 0.0, 'average': 0.0, 'timeframe': 60}, 'humidity': 92, 'windforce': 1, 'attribution': 'Data provided by buienradar.nl', 'visibility': 36200, 'windspeed': 0.94}, 'success': True, 'distance': 4.235064, 'msg': None}

    $ python -m buienradar -v
    INFO:__main__:Start...
    INFO:buienradar.buienradar:Getting buienradar data for latitude=52.091579, longitude=5.119734
    INFO:buienradar.buienradar:Retrieving xml weather data (https://xml.buienradar.nl/)...
    INFO:buienradar.buienradar:Retrieving xml weather data (http://gadgets.buienradar.nl/data/raintext/?lat=52.09&lon=5.12)...
    INFO:buienradar.buienradar:Parse ws data: latitude: 52.091579, longitude: 5.119734
    INFO:__main__:result: {'msg': None, 'success': True, 'data': {'attribution': 'Data provided by buienradar.nl', 'forecast': [{'snow': 0.0, 'condition': {'condition': 'cloudy', 'exact': 'Mix of clear and medium or low clouds', 'detailed': 'partlycloudy', 'exact_nl': 'Mix van opklaringen en middelbare of lage bewolking', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/b.png', 'condcode': 'b'}, 'temperature': 23.0, 'mintemp': 10.0, 'rainchance': 0, 'maxtemp': 23.0, 'windforce': 3, 'sunchance': 60, 'datetime': datetime.datetime(2017, 8, 7, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'rain': 0.0}, {'snow': 0.0, 'condition': {'condition': 'rainy', 'exact': 'Heavily clouded with rain', 'detailed': 'rainy', 'exact_nl': 'Zwaar bewolkt en regen', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/q.png', 'condcode': 'q'}, 'temperature': 20.0, 'mintemp': 13.0, 'rainchance': 80, 'maxtemp': 20.0, 'windforce': 3, 'sunchance': 20, 'datetime': datetime.datetime(2017, 8, 8, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'rain': 6.0}, {'snow': 0.0, 'condition': {'condition': 'rainy', 'exact': 'Alternatingly cloudy with some light rain', 'detailed': 'partlycloudy-light-rain', 'exact_nl': 'Afwisselend bewolkt met (mogelijk) wat lichte regen', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/f.png', 'condcode': 'f'}, 'temperature': 19.0, 'mintemp': 12.0, 'rainchance': 80, 'maxtemp': 19.0, 'windforce': 3, 'sunchance': 30, 'datetime': datetime.datetime(2017, 8, 9, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'rain': 6.0}, {'snow': 0.0, 'condition': {'condition': 'rainy', 'exact': 'Alternatingly cloudy with some light rain', 'detailed': 'partlycloudy-light-rain', 'exact_nl': 'Afwisselend bewolkt met (mogelijk) wat lichte regen', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/f.png', 'condcode': 'f'}, 'temperature': 17.0, 'mintemp': 11.0, 'rainchance': 80, 'maxtemp': 17.0, 'windforce': 3, 'sunchance': 30, 'datetime': datetime.datetime(2017, 8, 10, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'rain': 12.0}, {'snow': 0.0, 'condition': {'condition': 'rainy', 'exact': 'Alternatingly cloudy with some light rain', 'detailed': 'partlycloudy-light-rain', 'exact_nl': 'Afwisselend bewolkt met (mogelijk) wat lichte regen', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/f.png', 'condcode': 'f'}, 'temperature': 17.0, 'mintemp': 11.0, 'rainchance': 60, 'maxtemp': 17.0, 'windforce': 4, 'sunchance': 30, 'datetime': datetime.datetime(2017, 8, 11, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'rain': 8.0}], 'temperature': 12.9, 'visibility': 46400, 'windforce': 1, 'irradiance': 0, 'winddirection': 'ZZO', 'condition': {'condition': 'cloudy', 'exact': 'Heavily clouded', 'detailed': 'cloudy', 'exact_nl': 'Zwaar bewolkt', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/cc.png', 'condcode': 'c'}, 'precipitation': 0.0, 'windgust': 1.4, 'precipitation_forecast': {'timeframe': 60, 'total': 0.0, 'average': 0.0}, 'measured': datetime.datetime(2017, 8, 6, 22, 50, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'humidity': 94, 'groundtemperature': 10.7, 'pressure': 1022.32, 'windspeed': 1.09, 'windazimuth': 162, 'stationname': 'De Bilt (6260)'}, 'distance': 4.235064}
    {'msg': None, 'success': True, 'data': {'attribution': 'Data provided by buienradar.nl', 'forecast': [{'snow': 0.0, 'condition': {'condition': 'cloudy', 'exact': 'Mix of clear and medium or low clouds', 'detailed': 'partlycloudy', 'exact_nl': 'Mix van opklaringen en middelbare of lage bewolking', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/b.png', 'condcode': 'b'}, 'temperature': 23.0, 'mintemp': 10.0, 'rainchance': 0, 'maxtemp': 23.0, 'windforce': 3, 'sunchance': 60, 'datetime': datetime.datetime(2017, 8, 7, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'rain': 0.0}, {'snow': 0.0, 'condition': {'condition': 'rainy', 'exact': 'Heavily clouded with rain', 'detailed': 'rainy', 'exact_nl': 'Zwaar bewolkt en regen', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/q.png', 'condcode': 'q'}, 'temperature': 20.0, 'mintemp': 13.0, 'rainchance': 80, 'maxtemp': 20.0, 'windforce': 3, 'sunchance': 20, 'datetime': datetime.datetime(2017, 8, 8, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'rain': 6.0}, {'snow': 0.0, 'condition': {'condition': 'rainy', 'exact': 'Alternatingly cloudy with some light rain', 'detailed': 'partlycloudy-light-rain', 'exact_nl': 'Afwisselend bewolkt met (mogelijk) wat lichte regen', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/f.png', 'condcode': 'f'}, 'temperature': 19.0, 'mintemp': 12.0, 'rainchance': 80, 'maxtemp': 19.0, 'windforce': 3, 'sunchance': 30, 'datetime': datetime.datetime(2017, 8, 9, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'rain': 6.0}, {'snow': 0.0, 'condition': {'condition': 'rainy', 'exact': 'Alternatingly cloudy with some light rain', 'detailed': 'partlycloudy-light-rain', 'exact_nl': 'Afwisselend bewolkt met (mogelijk) wat lichte regen', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/f.png', 'condcode': 'f'}, 'temperature': 17.0, 'mintemp': 11.0, 'rainchance': 80, 'maxtemp': 17.0, 'windforce': 3, 'sunchance': 30, 'datetime': datetime.datetime(2017, 8, 10, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'rain': 12.0}, {'snow': 0.0, 'condition': {'condition': 'rainy', 'exact': 'Alternatingly cloudy with some light rain', 'detailed': 'partlycloudy-light-rain', 'exact_nl': 'Afwisselend bewolkt met (mogelijk) wat lichte regen', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/f.png', 'condcode': 'f'}, 'temperature': 17.0, 'mintemp': 11.0, 'rainchance': 60, 'maxtemp': 17.0, 'windforce': 4, 'sunchance': 30, 'datetime': datetime.datetime(2017, 8, 11, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'rain': 8.0}], 'temperature': 12.9, 'visibility': 46400, 'windforce': 1, 'irradiance': 0, 'winddirection': 'ZZO', 'condition': {'condition': 'cloudy', 'exact': 'Heavily clouded', 'detailed': 'cloudy', 'exact_nl': 'Zwaar bewolkt', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/cc.png', 'condcode': 'c'}, 'precipitation': 0.0, 'windgust': 1.4, 'precipitation_forecast': {'timeframe': 60, 'total': 0.0, 'average': 0.0}, 'measured': datetime.datetime(2017, 8, 6, 22, 50, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'humidity': 94, 'groundtemperature': 10.7, 'pressure': 1022.32, 'windspeed': 1.09, 'windazimuth': 162, 'stationname': 'De Bilt (6260)'}, 'distance': 4.235064}

    $ python -m buienradar -v --longitude=5.10 --latitude=52.1 --timeframe=45
    INFO:__main__:Start...    
    INFO:buienradar.buienradar:Getting buienradar data for latitude=52.1, longitude=5.1
    INFO:buienradar.buienradar:Retrieving xml weather data (https://xml.buienradar.nl/)...
    INFO:buienradar.buienradar:Retrieving xml weather data (http://gadgets.buienradar.nl/data/raintext/?lat=52.1&lon=5.1)...
    INFO:buienradar.buienradar:Parse ws data: latitude: 52.1, longitude: 5.1
    INFO:__main__:result: {'data': {'irradiance': 0, 'forecast': [{'condition': {'condition': 'cloudy', 'exact_nl': 'Mix van opklaringen en middelbare of lage bewolking', 'exact': 'Mix of clear and medium or low clouds', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/b.png', 'condcode': 'b', 'detailed': 'partlycloudy'}, 'mintemp': 10.0, 'windforce': 3, 'sunchance': 60, 'maxtemp': 23.0, 'rainchance': 0, 'datetime': datetime.datetime(2017, 8, 7, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'snow': 0.0, 'rain': 0.0, 'temperature': 23.0}, {'condition': {'condition': 'rainy', 'exact_nl': 'Zwaar bewolkt en regen', 'exact': 'Heavily clouded with rain', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/q.png', 'condcode': 'q', 'detailed': 'rainy'}, 'mintemp': 13.0, 'windforce': 3, 'sunchance': 20, 'maxtemp': 20.0, 'rainchance': 80, 'datetime': datetime.datetime(2017, 8, 8, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'snow': 0.0, 'rain': 6.0, 'temperature': 20.0}, {'condition': {'condition': 'rainy', 'exact_nl': 'Afwisselend bewolkt met (mogelijk) wat lichte regen', 'exact': 'Alternatingly cloudy with some light rain', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/f.png', 'condcode': 'f', 'detailed': 'partlycloudy-light-rain'}, 'mintemp': 12.0, 'windforce': 3, 'sunchance': 30, 'maxtemp': 19.0, 'rainchance': 80, 'datetime': datetime.datetime(2017, 8, 9, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'snow': 0.0, 'rain': 6.0, 'temperature': 19.0}, {'condition': {'condition': 'rainy', 'exact_nl': 'Afwisselend bewolkt met (mogelijk) wat lichte regen', 'exact': 'Alternatingly cloudy with some light rain', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/f.png', 'condcode': 'f', 'detailed': 'partlycloudy-light-rain'}, 'mintemp': 11.0, 'windforce': 3, 'sunchance': 30, 'maxtemp': 17.0, 'rainchance': 80, 'datetime': datetime.datetime(2017, 8, 10, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'snow': 0.0, 'rain': 12.0, 'temperature': 17.0}, {'condition': {'condition': 'rainy', 'exact_nl': 'Afwisselend bewolkt met (mogelijk) wat lichte regen', 'exact': 'Alternatingly cloudy with some light rain', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/f.png', 'condcode': 'f', 'detailed': 'partlycloudy-light-rain'}, 'mintemp': 11.0, 'windforce': 4, 'sunchance': 30, 'maxtemp': 17.0, 'rainchance': 60, 'datetime': datetime.datetime(2017, 8, 11, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'snow': 0.0, 'rain': 8.0, 'temperature': 17.0}], 'measured': datetime.datetime(2017, 8, 6, 22, 50, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'pressure': 1022.32, 'visibility': 46400, 'windspeed': 1.09, 'winddirection': 'ZZO', 'windazimuth': 162, 'groundtemperature': 10.7, 'humidity': 94, 'condition': {'condition': 'cloudy', 'exact_nl': 'Zwaar bewolkt', 'exact': 'Heavily clouded', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/cc.png', 'condcode': 'c', 'detailed': 'cloudy'}, 'windgust': 1.4, 'precipitation_forecast': {'average': 0.0, 'timeframe': 45, 'total': 0.0}, 'precipitation': 0.0, 'attribution': 'Data provided by buienradar.nl', 'stationname': 'De Bilt (6260)', 'windforce': 1, 'temperature': 12.9}, 'distance': 5.48199, 'success': True, 'msg': None}
    {'data': {'irradiance': 0, 'forecast': [{'condition': {'condition': 'cloudy', 'exact_nl': 'Mix van opklaringen en middelbare of lage bewolking', 'exact': 'Mix of clear and medium or low clouds', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/b.png', 'condcode': 'b', 'detailed': 'partlycloudy'}, 'mintemp': 10.0, 'windforce': 3, 'sunchance': 60, 'maxtemp': 23.0, 'rainchance': 0, 'datetime': datetime.datetime(2017, 8, 7, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'snow': 0.0, 'rain': 0.0, 'temperature': 23.0}, {'condition': {'condition': 'rainy', 'exact_nl': 'Zwaar bewolkt en regen', 'exact': 'Heavily clouded with rain', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/q.png', 'condcode': 'q', 'detailed': 'rainy'}, 'mintemp': 13.0, 'windforce': 3, 'sunchance': 20, 'maxtemp': 20.0, 'rainchance': 80, 'datetime': datetime.datetime(2017, 8, 8, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'snow': 0.0, 'rain': 6.0, 'temperature': 20.0}, {'condition': {'condition': 'rainy', 'exact_nl': 'Afwisselend bewolkt met (mogelijk) wat lichte regen', 'exact': 'Alternatingly cloudy with some light rain', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/f.png', 'condcode': 'f', 'detailed': 'partlycloudy-light-rain'}, 'mintemp': 12.0, 'windforce': 3, 'sunchance': 30, 'maxtemp': 19.0, 'rainchance': 80, 'datetime': datetime.datetime(2017, 8, 9, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'snow': 0.0, 'rain': 6.0, 'temperature': 19.0}, {'condition': {'condition': 'rainy', 'exact_nl': 'Afwisselend bewolkt met (mogelijk) wat lichte regen', 'exact': 'Alternatingly cloudy with some light rain', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/f.png', 'condcode': 'f', 'detailed': 'partlycloudy-light-rain'}, 'mintemp': 11.0, 'windforce': 3, 'sunchance': 30, 'maxtemp': 17.0, 'rainchance': 80, 'datetime': datetime.datetime(2017, 8, 10, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'snow': 0.0, 'rain': 12.0, 'temperature': 17.0}, {'condition': {'condition': 'rainy', 'exact_nl': 'Afwisselend bewolkt met (mogelijk) wat lichte regen', 'exact': 'Alternatingly cloudy with some light rain', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/f.png', 'condcode': 'f', 'detailed': 'partlycloudy-light-rain'}, 'mintemp': 11.0, 'windforce': 4, 'sunchance': 30, 'maxtemp': 17.0, 'rainchance': 60, 'datetime': datetime.datetime(2017, 8, 11, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'snow': 0.0, 'rain': 8.0, 'temperature': 17.0}], 'measured': datetime.datetime(2017, 8, 6, 22, 50, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 'pressure': 1022.32, 'visibility': 46400, 'windspeed': 1.09, 'winddirection': 'ZZO', 'windazimuth': 162, 'groundtemperature': 10.7, 'humidity': 94, 'condition': {'condition': 'cloudy', 'exact_nl': 'Zwaar bewolkt', 'exact': 'Heavily clouded', 'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/cc.png', 'condcode': 'c', 'detailed': 'cloudy'}, 'windgust': 1.4, 'precipitation_forecast': {'average': 0.0, 'timeframe': 45, 'total': 0.0}, 'precipitation': 0.0, 'attribution': 'Data provided by buienradar.nl', 'stationname': 'De Bilt (6260)', 'windforce': 1, 'temperature': 12.9}, 'distance': 5.48199, 'success': True, 'msg': None}



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
        'success': True, 
        'msg': None
        'data': {
            'attribution': 'Data provided by buienradar.nl', 
            'condition': {
                'condition': 'cloudy', 
                'exact_nl': 'Zwaar bewolkt', 
                'exact': 'Heavily clouded', 
                'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/cc.png', 
                'condcode': 'c', 
                'detailed': 'cloudy'}, 
            'groundtemperature': 10.7, 
            'humidity': 94, 
            'irradiance': 0, 
            'measured': datetime.datetime(2017, 8, 6, 22, 50, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 
            'precipitation': 0.0, 
            'precipitation_forecast': {
                'average': 0.0, 
                'timeframe': 45, 
                'total': 0.0}, 
            'pressure': 1022.32, 
            'stationname': 'De Bilt (6260)', 
            'temperature': 12.9
            'visibility': 46400, 
            'windspeed': 1.09, 
            'winddirection': 'ZZO', 
            'windazimuth': 162, 
            'windgust': 1.4, 
            'windforce': 1, 
            'forecast': [
                {'condition': {
                    'condition': 'cloudy', 
                    'exact_nl': 'Mix van opklaringen en middelbare of lage bewolking', 
                    'exact': 'Mix of clear and medium or low clouds', 
                    'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/b.png', 
                    'condcode': 'b', 
                    'detailed': 'partlycloudy'}, 
                'datetime': datetime.datetime(2017, 8, 7, 12, 0, tzinfo=<DstTzInfo 'Europe/Amsterdam' CEST+2:00:00 DST>), 
                'mintemp': 10.0, 
                'maxtemp': 23.0, 
                'temperature': 23.0, 
                'sunchance': 60, 
                'rainchance': 0, 
                'snow': 0.0, 
                'rain': 0.0, 
                'windforce': 3}
                ...
                ],
        }, 
    }
    
    
Use the constants defined in the buienradar component to get the data from the returned dictionary:

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
  - IMAGE: A symbol for the current weather
    
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
    
    - CONDITION: the expected condition (see condition above)
    - RAIN: the expected rain in (mm)
    - SNOW: the expected snowfall (in cm)
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
- HUMIDITY: the relative humidity (%)
- WINDAZIMUTH: where the wind is coming from: N (North), Z (south), NO (North-East), etc.
- WINDSPEED: the wind speed in m/s
- WINDDIRECTION: where the wind is coming from in degrees, with true north at 0° and progressing clockwise
- WINDFORCE: the wind speed/force in Bft
- PRECIPITATION: the amount of precipitation/rain in mm/h
- PRECIPITATION_FORECAST: information on forecasted precipitation

  - AVERAGE: the average expected precipitation (mm/h)
  - TOTAL: the total expected precipitation (mm)
  - TIMEFRAME: the time-frame for the forecasted precipitation (min)
