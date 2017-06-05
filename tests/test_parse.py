"""testing xml parsing."""
from datetime import datetime, timedelta

from buienradar.buienradar import (
    DATA,
    FORECAST,
    MESSAGE,
    STATIONNAME,
    SUCCESS,
    TEMPERATURE,
    __get_ws_distance,
    __parse_data,
    __parse_precipfc_data
)


def get_imageurl():
    result = 'https://www.buienradar.nl/'
    result += 'resources/images/icons/weather/30x30/cc.png'
    return result


def test_precip_fc():
    """Test parsing precipitation forecast data."""

    data = ""
    for n in range(0, 24):
        data += "000|%s\n" % (datetime.now() +
                              timedelta(minutes=n*5)).strftime("%H:%M")

    result = __parse_precipfc_data(data, 3600)
    expect = {'average': 0.0, 'total': 0.0, 'timeframe': 3600}

    # test calling results in the loop close cleanly
    print(result)
    assert (expect == result)


def test_precip_fc2():
    """Test parsing precipitation forecast data."""

    data = ""
    for n in range(0, 24):
        data += "100|%s\n" % (datetime.now() +
                              timedelta(minutes=n*5)).strftime("%H:%M")

    result = __parse_precipfc_data(data, 3600)
    expect = {'average': 0.52, 'timeframe': 3600, 'total': 0.52}

    # test calling results in the loop close cleanly
    print(result)
    assert (expect == result)


def test_precip_fc3():
    """Test parsing precipitation forecast data."""

    data = ""
    for n in range(0, 24):
        data += "100|%s\n" % (datetime.now() +
                              timedelta(minutes=n*5)).strftime("%H:%M")

    result = __parse_precipfc_data(data, 1800)
    expect = {'average': 0.52, 'timeframe': 1800, 'total': 0.26}

    # test calling results in the loop close cleanly
    print(result)
    assert (expect == result)


def test_precip_fc4():
    """Test parsing precipitation forecast data."""

    data = ""
    for n in range(0, 24):
        data += "077|%s\n" % (datetime.now() +
                              timedelta(minutes=n*5)).strftime("%H:%M")

    result = __parse_precipfc_data(data, 1800)
    expect = {'average': 0.1, 'timeframe': 1800, 'total': 0.05}

    # test calling results in the loop close cleanly
    print(result)
    assert (expect == result)


def test_readdata1():
    """Test loading and parsing xml file."""
    # load buienradar.xml
    file = open('tests/buienradar.xml', 'r')
    data = file.read()
    file.close()

    # select first weatherstation
    # Meetstation Arcen (6391)
    latitude = 51.50
    longitude = 6.20
    result = __parse_data(data, latitude, longitude)
    print(result)
    assert(result[SUCCESS] and result[MESSAGE] is None)

    # check the selected weatherstation:
    assert(result[SUCCESS] and
           '(6391)' in result[DATA][STATIONNAME])

    # check the data:
    fc1 = (datetime.today() + timedelta(days=1))
    fc2 = (datetime.today() + timedelta(days=2))
    fc3 = (datetime.today() + timedelta(days=3))
    fc4 = (datetime.today() + timedelta(days=4))
    fc5 = (datetime.today() + timedelta(days=5))

    fc1 = fc1.replace(hour=0, minute=0, second=0, microsecond=0)
    fc2 = fc2.replace(hour=0, minute=0, second=0, microsecond=0)
    fc3 = fc3.replace(hour=0, minute=0, second=0, microsecond=0)
    fc4 = fc4.replace(hour=0, minute=0, second=0, microsecond=0)
    fc5 = fc5.replace(hour=0, minute=0, second=0, microsecond=0)

    # Expected result:
    expect = {
        'data': {
            'windgust': '4.4',
            'windspeed': '3.13',
            'temperature': '16.3',
            'stationname': 'Meetstation Arcen (6391)',
            'windazimuth': 'ONO',
            'symbol': 'Zwaar bewolkt',
            'windforce': '2',
            'pressure': '1021.23',
            'winddirection': '77',
            'humidity': '95',
            'image': get_imageurl(),
            'attribution': 'Data provided by buienradar.nl',
            'groundtemperature': '15.9',
            'precipitation': '2',
            'measured': '05/19/2017 00:20:00',
            'irradiance': '614',
            'visibility': '38400',
            'forecast': [
                {'datetime': fc1, 'temperature': 16.0, 'max_temp': 16.0,
                 'min_temp': 8.0, 'rain_chance': 15, 'sun_chance': None,
                 'rain': None, 'windforce': 3},
                {'datetime': fc2, 'temperature': 17.0, 'max_temp': 17.0,
                 'min_temp': 8.0, 'rain_chance': 1, 'sun_chance': 43,
                 'rain': None, 'windforce': 3},
                {'datetime': fc3, 'temperature': 22.0, 'max_temp': 22.0,
                 'min_temp': 10.0, 'rain_chance': 3, 'sun_chance': None,
                 'rain': None, 'windforce': 4},
                {'datetime': fc4, 'temperature': 18.0, 'max_temp': 18.0,
                 'min_temp': 11.0, 'rain_chance': 43, 'sun_chance': None,
                 'rain': 1.8, 'windforce': 4},
                {'datetime': fc5, 'temperature': 15.0, 'max_temp': 15.0,
                 'min_temp': 9.0, 'rain_chance': 76, 'sun_chance': None,
                 'rain': 4.4, 'windforce': 4}
                ],
            },
        'success': True,
        'msg': None,
        'distance': 0.0
    }
    assert(expect == result)


def test_readdata2():
    """Test loading and parsing xml file."""
    # load buienradar.xml
    file = open('tests/buienradar.xml', 'r')
    data = file.read()
    file.close()

    # select non-first weather stationnaam
    # gps coordinates not exact, so non-zero distance
    # Meetstation De Bilt (6260)
    latitude = 52.11
    longitude = 5.19
    result = __parse_data(data, latitude, longitude)
    print(result)
    assert(result[SUCCESS] and
           result[MESSAGE] is None)

    # check the selected weatherstation:
    assert(result[SUCCESS] and
           '(6260)' in result[DATA][STATIONNAME])

    # check the data:
    fc1 = (datetime.today() + timedelta(days=1))
    fc2 = (datetime.today() + timedelta(days=2))
    fc3 = (datetime.today() + timedelta(days=3))
    fc4 = (datetime.today() + timedelta(days=4))
    fc5 = (datetime.today() + timedelta(days=5))

    fc1 = fc1.replace(hour=0, minute=0, second=0, microsecond=0)
    fc2 = fc2.replace(hour=0, minute=0, second=0, microsecond=0)
    fc3 = fc3.replace(hour=0, minute=0, second=0, microsecond=0)
    fc4 = fc4.replace(hour=0, minute=0, second=0, microsecond=0)
    fc5 = fc5.replace(hour=0, minute=0, second=0, microsecond=0)

    # Expected result:
    expect = {
        'data': {
            'humidity': '88',
            'windforce': '3',
            'windgust': '6.4',
            'windspeed': '4.64',
            'winddirection': '72',
            'visibility': '14800',
            'attribution': 'Data provided by buienradar.nl',
            'symbol': 'Zwaar bewolkt',
            'temperature': '16.0',
            'measured': '05/19/2017 00:20:00',
            'groundtemperature': '15.4',
            'pressure': '1008.72',
            'image': get_imageurl(),
            'stationname': 'Meetstation De Bilt (6260)',
            'precipitation': '-',
            'windazimuth': 'ONO',
            'irradiance': '-',
            'forecast': [
                {'datetime': fc1, 'temperature': 16.0, 'max_temp': 16.0,
                 'min_temp': 8.0, 'rain_chance': 15, 'sun_chance': None,
                 'rain': None, 'windforce': 3},
                {'datetime': fc2, 'temperature': 17.0, 'max_temp': 17.0,
                 'min_temp': 8.0, 'rain_chance': 1, 'sun_chance': 43,
                 'rain': None, 'windforce': 3},
                {'datetime': fc3, 'temperature': 22.0, 'max_temp': 22.0,
                 'min_temp': 10.0, 'rain_chance': 3, 'sun_chance': None,
                 'rain': None, 'windforce': 4},
                {'datetime': fc4, 'temperature': 18.0, 'max_temp': 18.0,
                 'min_temp': 11.0, 'rain_chance': 43, 'sun_chance': None,
                 'rain': 1.8, 'windforce': 4},
                {'datetime': fc5, 'temperature': 15.0, 'max_temp': 15.0,
                 'min_temp': 9.0, 'rain_chance': 76, 'sun_chance': None,
                 'rain': 4.4, 'windforce': 4}
            ],
        },
        'success': True,
        'distance': 1.306732,
        'msg': None}
    assert(expect == result)


def test_readdata3():
    """Test loading and parsing xml file."""
    # load buienradar.xml
    file = open('tests/buienradar.xml', 'r')
    data = file.read()
    file.close()

    # select last weather stationnaam
    # gps coordinates not exact, so non-zero distance
    # Meetstation Zeeplatform K13 (6252)
    latitude = 53.23
    longitude = 3.23
    result = __parse_data(data, latitude, longitude)
    print(result)
    assert(result[SUCCESS] and
           result[MESSAGE] is None)

    # check the selected weatherstation:
    assert(result[SUCCESS] and
           '(6252)' in result[DATA][STATIONNAME])

    # check the data:
    fc1 = (datetime.today() + timedelta(days=1))
    fc2 = (datetime.today() + timedelta(days=2))
    fc3 = (datetime.today() + timedelta(days=3))
    fc4 = (datetime.today() + timedelta(days=4))
    fc5 = (datetime.today() + timedelta(days=5))

    fc1 = fc1.replace(hour=0, minute=0, second=0, microsecond=0)
    fc2 = fc2.replace(hour=0, minute=0, second=0, microsecond=0)
    fc3 = fc3.replace(hour=0, minute=0, second=0, microsecond=0)
    fc4 = fc4.replace(hour=0, minute=0, second=0, microsecond=0)
    fc5 = fc5.replace(hour=0, minute=0, second=0, microsecond=0)

    # Expected result:
    expect = {
        'msg': None,
        'success': True,
        'distance': 1.297928,
        'data': {
            'attribution': 'Data provided by buienradar.nl',
            'windspeed': '8.16',
            'windazimuth': 'O',
            'groundtemperature': '-',
            'windforce': '5',
            'precipitation': '-',
            'humidity': '47',
            'pressure': '1004.95',
            'symbol': 'Zwaar bewolkt',
            'measured': '05/19/2017 00:20:00',
            'winddirection': '59',
            'stationname': 'Meetstation Zeeplatform K13 (6252)',
            'temperature': '16.8',
            'visibility': '6200',
            'irradiance': '614',
            'windgust': '14',
            'image': get_imageurl(),
            'forecast': [
                    {'datetime': fc1, 'temperature': 16.0, 'max_temp': 16.0,
                     'min_temp': 8.0, 'rain_chance': 15, 'sun_chance': None,
                     'rain': None, 'windforce': 3},
                    {'datetime': fc2, 'temperature': 17.0, 'max_temp': 17.0,
                     'min_temp': 8.0, 'rain_chance': 1, 'sun_chance': 43,
                     'rain': None, 'windforce': 3},
                    {'datetime': fc3, 'temperature': 22.0, 'max_temp': 22.0,
                     'min_temp': 10.0, 'rain_chance': 3, 'sun_chance': None,
                     'rain': None, 'windforce': 4},
                    {'datetime': fc4, 'temperature': 18.0, 'max_temp': 18.0,
                     'min_temp': 11.0, 'rain_chance': 43, 'sun_chance': None,
                     'rain': 1.8, 'windforce': 4},
                    {'datetime': fc5, 'temperature': 15.0, 'max_temp': 15.0,
                     'min_temp': 9.0, 'rain_chance': 76, 'sun_chance': None,
                     'rain': 4.4, 'windforce': 4}
                ]
            },
        }
    assert(expect == result)


def test_noxml():
    """Test loading and parsing invalid xml file."""
    # load noxml_file
    file = open('tests/buienradar_noxml.xml', 'r')
    data = file.read()
    file.close()

    result = __parse_data(data)

    # test calling results in the loop close cleanly
    print(result)
    assert (result[SUCCESS] is False and
            result[MESSAGE] == 'Unable to parse content as xml.')


def test_noroot():
    """Test loading and parsing invalid xml file."""
    # load noxml_file
    file = open('tests/buienradar_noroot.xml', 'r')
    data = file.read()
    file.close()

    result = __parse_data(data)

    # test calling results in the loop close cleanly
    print(result)
    assert (result[SUCCESS] is False and
            result[MESSAGE] == 'Unable to parse content as xml.')


def test_nows():
    """Test loading and parsing invalid xml file; no weatherstation."""
    file = open('tests/buienradar_nows.xml', 'r')
    data = file.read()
    file.close()

    result = __parse_data(data)
    # test calling results in the loop close cleanly
    print(result)
    assert (result[SUCCESS] is False and
            result[MESSAGE] == 'No location selected.')

    file = open('tests/buienradar_nows2.xml', 'r')
    data = file.read()
    file.close()

    result = __parse_data(data)
    # test calling results in the loop close cleanly
    print(result)
    assert (result[SUCCESS] is False and
            result[MESSAGE] == 'No location selected.')

    file = open('tests/buienradar_nows3.xml', 'r')
    data = file.read()
    file.close()

    result = __parse_data(data)
    # test calling results in the loop close cleanly
    print(result)
    assert (result[SUCCESS] is False and
            result[MESSAGE] == 'No location selected.')

    file = open('tests/buienradar_nows4.xml', 'r')
    data = file.read()
    file.close()

    result = __parse_data(data)
    # test calling results in the loop close cleanly
    print(result)
    assert (result[SUCCESS] is False and
            result[MESSAGE] == 'No location selected.')

    file = open('tests/buienradar_nows5.xml', 'r')
    data = file.read()
    file.close()

    result = __parse_data(data)
    # test calling results in the loop close cleanly
    print(result)
    assert (result[SUCCESS] is False and
            result[MESSAGE] == 'No location selected.')


def test_wsdistancen_with_none():
    """Test distance function without valid input."""
    latitude = 51.50
    longitude = 6.20
    distance = __get_ws_distance(None, latitude, longitude)
    print(distance)
    assert (distance is None)


def test_nofc():
    """Test loading and parsing invalid xml file: no forecast data."""
    file = open('tests/buienradar_nofc.xml', 'r')
    data = file.read()
    file.close()

    result = __parse_data(data)

    # test calling results in the loop close cleanly
    print(result)
    assert (result[SUCCESS] and
            result[MESSAGE] == 'Unable to extract forecast data.')


def test_nofc2():
    """Test loading and parsing invalid xml file; no forecast."""
    file = open('tests/buienradar_nofc2.xml', 'r')
    data = file.read()
    file.close()

    result = __parse_data(data)

    # test calling results in the loop close cleanly
    print(result)
    assert (result[SUCCESS] and
            len(result[DATA][FORECAST]) == 0)


def test_missing_data():
    """Test loading and parsing invalid xml file; missing data fields."""
    file = open('tests/buienradar_missing.xml', 'r')
    data = file.read()
    file.close()

    latitude = 51.50
    longitude = 6.20
    result = __parse_data(data, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and
            result[MESSAGE] == "Missing key(s) in br data: stationnaam ")

    latitude = 52.07
    longitude = 5.88
    result = __parse_data(data, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and
            result[MESSAGE] == "Missing key(s) in br data: icoonactueel ")

    latitude = 52.65
    longitude = 4.98
    result = __parse_data(data, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and
            result[MESSAGE] == "Missing key(s) in br data: luchtvochtigheid ")

    latitude = 52.10
    longitude = 5.18
    result = __parse_data(data, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and
            result[MESSAGE] == "Missing key(s) in br data: temperatuurGC ")

    latitude = 52.92
    longitude = 4.78
    result = __parse_data(data, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and
            result[MESSAGE] == "Missing key(s) in br data: temperatuur10cm ")

    latitude = 51.45
    longitude = 5.42
    result = __parse_data(data, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and
            result[MESSAGE] == "Missing key(s) in br data: windsnelheidMS ")

    latitude = 51.20
    longitude = 5.77
    result = __parse_data(data, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and
            result[MESSAGE] == "Missing key(s) in br data: windsnelheidBF ")

    latitude = 52.00
    longitude = 3.28
    result = __parse_data(data, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and
            result[MESSAGE] == "Missing key(s) in br data: windrichtingGR ")

    latitude = 51.57
    longitude = 4.93
    result = __parse_data(data, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and
            result[MESSAGE] == "Missing key(s) in br data: windrichting ")

    latitude = 52.07
    longitude = 6.65
    result = __parse_data(data, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and
            result[MESSAGE] == "Missing key(s) in br data: luchtdruk ")

    latitude = 52.43
    longitude = 6.27
    result = __parse_data(data, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and
            result[MESSAGE] == "Missing key(s) in br data: windstotenMS ")

    latitude = 51.87
    longitude = 5.15
    result = __parse_data(data, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and
            result[MESSAGE] == "Missing key(s) in br data: regenMMPU ")

    latitude = 51.98
    longitude = 4.10
    result = __parse_data(data, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and
            result[MESSAGE] == "Missing key(s) in br data: zonintensiteitWM2 ")


def test_invalid_data():
    """Test loading and parsing xml file with data that cannot be parsed."""
    file = open('tests/buienradar_invalidfc1.xml', 'r')
    data = file.read()
    file.close()

    latitude = 51.98
    longitude = 4.10
    result = __parse_data(data, latitude, longitude)
    print(result)
    assert(result[SUCCESS] and
           result[MESSAGE] is None)
    # test missing maxtemp:
    assert(len(result[DATA][FORECAST]) == 5 and
           result[DATA][FORECAST][0][TEMPERATURE] is None)
    # test missing maxgtemp and maxtempmax:
    assert(len(result[DATA][FORECAST]) == 5 and
           result[DATA][FORECAST][2][TEMPERATURE] is None)

    # read xml with invalid ws coordinates
    file = open('tests/buienradar_invalidws1.xml', 'r')
    data = file.read()
    file.close()

    # 'Meetstation Arcen' contains invalid gps info,
    # 'Meetstation Volkel' will be selected as alternative
    latitude = 51.50
    longitude = 6.20
    result = __parse_data(data, latitude, longitude)
    print(result)
    assert(result[SUCCESS] and
           '(6375)' in result[DATA][STATIONNAME])

    # 'Meetstation Arnhem' contains invalid gps info,
    # 'Meetstation De Bilt' will be selected as alternative
    latitude = 52.07
    longitude = 5.88
    result = __parse_data(data, latitude, longitude)
    print(result)
    assert(result[SUCCESS] and
           '(6260)' in result[DATA][STATIONNAME])

    # 'Meetstation Berkhout' contains invalid gps info,
    # 'Meetstation Wijdenes' will be selected as alternative
    latitude = 52.65
    longitude = 4.98
    result = __parse_data(data, latitude, longitude)
    print(result)
    assert(result[SUCCESS] and
           '(6248)' in result[DATA][STATIONNAME])
