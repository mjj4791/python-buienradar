Changelog
=========
All notable changes to this project will be documented in this file.
Changes that did not make it into a new release are marked with [unreleased].

[unreleased/0.6]
""""""""""""""""
**added**

- example usage
- detect api respone with all "0"s or "-"s
- return all values a numbers (also - as 0 or 0.0)

**changed**

- improved precipitation forecast calculation
- improved/added unit tests
- windirection and windazimuth are now reversed

  - winddirection: N/O/Z etc
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
