from buienradar.buienradar import (
    CONTENT,
    RAINCONTENT,
    SUCCESS,
    get_data,
    parse_data
)

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
