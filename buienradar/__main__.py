"""Command line interface for buienradar library.

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
"""
import logging
import sys

import pkg_resources
from docopt import docopt

from .buienradar import MESSAGE, SUCCESS, get_data


def main(argv=sys.argv[1:]):
    """Parse argument and start main program."""
    args = docopt(__doc__, argv=argv,
                  version=pkg_resources.require('buienradar')[0].version)

    level = logging.ERROR
    if args['-v']:
        level = logging.INFO
    if args['-v'] == 2:
        level = logging.DEBUG
    logging.basicConfig(level=level)

    log = logging.getLogger(__name__)
    log.info("Start...")

    result = get_data(
                      latitude=float(args['--latitude']),
                      longitude=float(args['--longitude']),
                      timeframe=int(args['--timeframe']),
                     )

    if result[SUCCESS]:
        log.info("Retrieved data:\n%s", result)
    else:
        log.error("Retrieving xml weather data was not successfull (%s)",
                  result[MESSAGE])


if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()
