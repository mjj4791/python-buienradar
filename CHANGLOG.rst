Changelog
=========
All notable changes to this project will be documented in this file.

[1.0.7] - 2025-02-04
""""""""""""""""""""
**changed**

- json:
  - support iconurl conditionimage independent of casing (upper/lower case)
  - apply workaround for condition image, if needed (convert filename uppercase)
- xml:
  - support icon/id independent if casing (upper/lower case)
  - apply workaround for condition image, if needed (convert filename uppercase)


[1.0.6] - 2024-06-09
""""""""""""""""""""
**changed**

- make pytz.timezone(__TIMEZONE) a constant to prevent a locking call on each use


[1.0.5] - 2021-11-27
""""""""""""""""""""
**changed**

- Support precipitation data with (dtuch) floating point numbers (using , as a decimal separator)
- Decreases some logging to debug


[1.0.3/4] - 2019-12-15
""""""""""""""""""""""
**changed**

- updated readme / documentation
- updated setup.py (set content type for readme).

[1.0.2] - 2019-12-15
""""""""""""""""""""
**changed**

- derive condition from icon url and no longer using condition text
- updated tests
- lowered loglevel of missng weather-data elements to debug

**new**

- added nighttime indicator in condition section; derived from icon url


[1.0.1] - 2019-06-10
""""""""""""""""""""
**changed**

- updated version logic in setup
- moved url logic to separate module
- updated calculation of forcasted temperature and rain (json)
- New sensor types:

    - added (json only): barometerfcnamenl
    - added forecast for (json only):

        - windspeed (estimated using windforce)
        - windazimuth (estimated using winddirection)


[1.0.0] - 2019-03-02
""""""""""""""""""""
**changed**

- moved from old XML API to new json API

**new**

- New sensor types:

  - added (json only): barometerfc, barometerfcname, feeltemperature, rainlast24hour, rainlasthour
  - added forecast for (json only): minrain, maxrain


[0.91] - 2018-02-15
"""""""""""""""""""
**changed**

- fixed an unexpected exception in case the internet is down or DNS is unavailable


[0.9] - 2017-08-07
""""""""""""""""""
**changed**

- removed symbol and image, replaced by condition element

**new**

- added detailed condition element
- added snow to forecast
- added condition to forecast

[0.8] - 2017-07-27
""""""""""""""""""
**changed**

- all datetimes are now real datetimes
- datetimes contain tzinfo (Europe/Amsterdam)
- prevent unnecessary http-redirects when fetching raindata

[0.7] - 2017-06-02
""""""""""""""""""
**changed**

- updated readme & changelog
- bumped version to 0.7

[0.6] - 2017-06-01
""""""""""""""""""
**added**

- example usage
- detect api response with all "0"s or "-"s
- return all values a numbers (also '-' as 0 or 0.0)

**changed**

- improved precipitation forecast calculation
- improved/added unit tests
- windirection and windazimuth are now reversed

  - winddirection: N/O/Z etc.
  - windazimuth: is measured in degrees

- removed 'Meetstation ' from station name

[0.5] - 2017-06-10
""""""""""""""""""
This version is non-functional / should not be used.
**added**

- measured date/time added to data section
- added precipitation forecast
- add secondary url for buienradar api

**changed**

- fixed linting

[0.4] - 2017-05-28
""""""""""""""""""
**added**

- when call to primary url fails, use secondary url
- CHANGELOG

**changed**



[0.3] - 2017-05-21
""""""""""""""""""
**added**

- code sample in README.rst

**changed**

- fixed 'stationname'-key in result[data]
- forecast moved into data-section


[0.2] - 2017-05-21
""""""""""""""""""
**added**

- unittests
- distance in result

**changed**

- fixed exception handling


[0.1] - 2017-05-21
******************
Initial version
