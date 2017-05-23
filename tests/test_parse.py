"""testing xml parsing."""
from datetime import datetime

from buienradar.buienradar import (
    DATA,
    FORECAST,
    MESSAGE,
    STATIONNAME,
    SUCCESS,
    TEMPERATURE,
    __get_ws_distance,
    parse_data
)


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
    result = parse_data(data, latitude, longitude)
    print(result)
    assert(result[SUCCESS] and result[MESSAGE] is None)

    # check the selected weatherstation:
    assert(result[SUCCESS] and '(6391)' in result[DATA][STATIONNAME])

    # check the data:
    # Expected result:
    expect = {
        'data': {
            'windgust': '4.4',
            'windspeed': '3.13',
            'temperature': '16.3',
            'stationnaam': 'Meetstation Arcen (6391)',
            'windazimuth': 'ONO',
            'symbol': 'Zwaar bewolkt',
            'windforce': '2',
            'pressure': '1021.23',
            'winddirection': '77',
            'humidity': '95',
            'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/cc.png',
            'attribution': 'Data provided by buienradar.nl',
            'groundtemperature': '15.9',
            'precipitation': '2',
            'irradiance': '614',
            'visibility': '38400'
            },
        'success': True,
        'msg': None,
        'forecast': [
            {'temperature': 16.0, 'datetime': datetime(2017, 5, 24, 0, 0)},
            {'temperature': 17.0, 'datetime': datetime(2017, 5, 25, 0, 0)},
            {'temperature': 22.0, 'datetime': datetime(2017, 5, 26, 0, 0)},
            {'temperature': 18.0, 'datetime': datetime(2017, 5, 27, 0, 0)},
            {'temperature': 15.0, 'datetime': datetime(2017, 5, 28, 0, 0)}],
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
    result = parse_data(data, latitude, longitude)
    print(result)
    assert(result[SUCCESS] and result[MESSAGE] is None)

    # check the selected weatherstation:
    assert(result[SUCCESS] and '(6260)' in result[DATA][STATIONNAME])

    # check the data:
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
            'groundtemperature': '15.4',
            'pressure': '1008.72',
            'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/cc.png',
            'stationnaam': 'Meetstation De Bilt (6260)',
            'precipitation': '-',
            'windazimuth': 'ONO',
            'irradiance': '-'
        },
        'success': True,
        'distance': 1.306732,
        'forecast': [
            {'datetime': datetime(2017, 5, 24, 0, 0), 'temperature': 16.0},
            {'datetime': datetime(2017, 5, 25, 0, 0), 'temperature': 17.0},
            {'datetime': datetime(2017, 5, 26, 0, 0), 'temperature': 22.0},
            {'datetime': datetime(2017, 5, 27, 0, 0), 'temperature': 18.0},
            {'datetime': datetime(2017, 5, 28, 0, 0), 'temperature': 15.0}
        ],
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
    result = parse_data(data, latitude, longitude)
    print(result)
    assert(result[SUCCESS] and result[MESSAGE] is None)

    # check the selected weatherstation:
    assert(result[SUCCESS] and '(6252)' in result[DATA][STATIONNAME])

    # check the data:
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
            'winddirection': '59',
            'stationnaam': 'Meetstation Zeeplatform K13 (6252)',
            'temperature': '16.8',
            'visibility': '6200',
            'irradiance': '614',
            'windgust': '14',
            'image': 'https://www.buienradar.nl/resources/images/icons/weather/30x30/cc.png'
        },
        'forecast': [
            {'datetime': datetime(2017, 5, 24, 0, 0), 'temperature': 16.0},
            {'datetime': datetime(2017, 5, 25, 0, 0), 'temperature': 17.0},
            {'datetime': datetime(2017, 5, 26, 0, 0), 'temperature': 22.0},
            {'datetime': datetime(2017, 5, 27, 0, 0), 'temperature': 18.0},
            {'datetime': datetime(2017, 5, 28, 0, 0), 'temperature': 15.0}
            ]
        }
    assert(expect == result)


def test_noxml():
    """Test loading and parsing invalid xml file."""
    # load noxml_file
    file = open('tests/buienradar_noxml.xml', 'r')
    data = file.read()
    file.close()

    result = parse_data(data)

    # test calling results in the loop close cleanly
    print(result)
    assert (result[SUCCESS] is False and result[MESSAGE] == 'Unable to parse content as xml.')


def test_noroot():
    """Test loading and parsing invalid xml file."""
    # load noxml_file
    file = open('tests/buienradar_noroot.xml', 'r')
    data = file.read()
    file.close()

    result = parse_data(data)

    # test calling results in the loop close cleanly
    print(result)
    assert (result[SUCCESS] is False and result[MESSAGE] == 'Unable to parse content as xml.')


def test_nows():
    """Test loading and parsing invalid xml file; no weatherstation."""
    file = open('tests/buienradar_nows.xml', 'r')
    data = file.read()
    file.close()

    result = parse_data(data)
    # test calling results in the loop close cleanly
    print(result)
    assert (result[SUCCESS] is False and result[MESSAGE] == 'No location selected.')

    file = open('tests/buienradar_nows2.xml', 'r')
    data = file.read()
    file.close()

    result = parse_data(data)
    # test calling results in the loop close cleanly
    print(result)
    assert (result[SUCCESS] is False and result[MESSAGE] == 'No location selected.')

    file = open('tests/buienradar_nows3.xml', 'r')
    data = file.read()
    file.close()

    result = parse_data(data)
    # test calling results in the loop close cleanly
    print(result)
    assert (result[SUCCESS] is False and result[MESSAGE] == 'No location selected.')

    file = open('tests/buienradar_nows4.xml', 'r')
    data = file.read()
    file.close()

    result = parse_data(data)
    # test calling results in the loop close cleanly
    print(result)
    assert (result[SUCCESS] is False and result[MESSAGE] == 'Unable to extract forecast data.')

    file = open('tests/buienradar_nows5.xml', 'r')
    data = file.read()
    file.close()

    result = parse_data(data)
    # test calling results in the loop close cleanly
    print(result)
    assert (result[SUCCESS] is False and result[MESSAGE] == 'No location selected.')


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

    result = parse_data(data)

    # test calling results in the loop close cleanly
    print(result)
    assert (result[SUCCESS] and result[MESSAGE] == 'Unable to extract forecast data.')


def test_nofc2():
    """Test loading and parsing invalid xml file; no forecast."""
    file = open('tests/buienradar_nofc2.xml', 'r')
    data = file.read()
    file.close()

    result = parse_data(data)

    # test calling results in the loop close cleanly
    print(result)
    assert (result[SUCCESS] and len(result[FORECAST]) == 0)


def test_missing_data():
    """Test loading and parsing invalid xml file; missing data fields."""
    file = open('tests/buienradar_missing.xml', 'r')
    data = file.read()
    file.close()

    latitude = 51.50
    longitude = 6.20
    result = parse_data(data, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and result[MESSAGE] == "Missing key(s) in br data: stationnaam ")

    latitude = 52.07
    longitude = 5.88
    result = parse_data(data, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and result[MESSAGE] == "Missing key(s) in br data: icoonactueel ")

    latitude = 52.65
    longitude = 4.98
    result = parse_data(data, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and result[MESSAGE] == "Missing key(s) in br data: luchtvochtigheid ")

    latitude = 52.10
    longitude = 5.18
    result = parse_data(data, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and result[MESSAGE] == "Missing key(s) in br data: temperatuurGC ")

    latitude = 52.92
    longitude = 4.78
    result = parse_data(data, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and result[MESSAGE] == "Missing key(s) in br data: temperatuur10cm ")

    latitude = 51.45
    longitude = 5.42
    result = parse_data(data, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and result[MESSAGE] == "Missing key(s) in br data: windsnelheidMS ")

    latitude = 51.20
    longitude = 5.77
    result = parse_data(data, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and result[MESSAGE] == "Missing key(s) in br data: windsnelheidBF ")

    latitude = 52.00
    longitude = 3.28
    result = parse_data(data, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and result[MESSAGE] == "Missing key(s) in br data: windrichtingGR ")

    latitude = 51.57
    longitude = 4.93
    result = parse_data(data, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and result[MESSAGE] == "Missing key(s) in br data: windrichting ")

    latitude = 52.07
    longitude = 6.65
    result = parse_data(data, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and result[MESSAGE] == "Missing key(s) in br data: luchtdruk ")

    latitude = 52.43
    longitude = 6.27
    result = parse_data(data, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and result[MESSAGE] == "Missing key(s) in br data: windstotenMS ")

    latitude = 51.87
    longitude = 5.15
    result = parse_data(data, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and result[MESSAGE] == "Missing key(s) in br data: regenMMPU ")

    latitude = 51.98
    longitude = 4.10
    result = parse_data(data, latitude, longitude)
    print(result)
    assert (result[SUCCESS] and result[MESSAGE] == "Missing key(s) in br data: zonintensiteitWM2 ")


def test_invalid_data():
    """Test loading and parsing xml file contianing data that cannot be parsed."""
    file = open('tests/buienradar_invalidfc1.xml', 'r')
    data = file.read()
    file.close()

    latitude = 51.98
    longitude = 4.10
    result = parse_data(data, latitude, longitude)
    print(result)
    assert(result[SUCCESS] and result[MESSAGE] is None)
    # test missing maxtemp:
    assert(len(result[FORECAST]) == 5 and result[FORECAST][0][TEMPERATURE] is None)
    # test missing maxtempmax:
    assert(len(result[FORECAST]) == 5 and result[FORECAST][1][TEMPERATURE] is None)
    # test missing maxgtemp and maxtempmax:
    assert(len(result[FORECAST]) == 5 and result[FORECAST][2][TEMPERATURE] is None)

    # read xml with invalid ws coordinates
    file = open('tests/buienradar_invalidws1.xml', 'r')
    data = file.read()
    file.close()

    # 'Meetstation Arcen' contains invalid gps info,
    # 'Meetstation Volkel' will be selected as alternative
    latitude = 51.50
    longitude = 6.20
    result = parse_data(data, latitude, longitude)
    print(result)
    assert(result[SUCCESS] and '(6375)' in result[DATA][STATIONNAME])

    # 'Meetstation Arnhem' contains invalid gps info,
    # 'Meetstation De Bilt' will be selected as alternative
    latitude = 52.07
    longitude = 5.88
    result = parse_data(data, latitude, longitude)
    print(result)
    assert(result[SUCCESS] and '(6260)' in result[DATA][STATIONNAME])

    # 'Meetstation Berkhout' contains invalid gps info,
    # 'Meetstation Wijdenes' will be selected as alternative
    latitude = 52.65
    longitude = 4.98
    result = parse_data(data, latitude, longitude)
    print(result)
    assert(result[SUCCESS] and '(6248)' in result[DATA][STATIONNAME])
