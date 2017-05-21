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
"""
import logging
import sys
import buienradar
from buienradar import SUCCESS, MESSAGE, CONTENT
import pkg_resources
from docopt import docopt


def main(argv=sys.argv[1:]):
    """Parse argument and start main program."""
    args = docopt(__doc__, argv=argv,
                  version=0.1)
    #version=pkg_resources.require('buienradar')[0].version)
    level = logging.ERROR
    if args['-v']:
        level = logging.INFO
    if args['-v'] == 2:
        level = logging.DEBUG
    logging.basicConfig(level=level)

    log = logging.getLogger(__name__)
    log.info("Start...")

    result = buienradar.get()

    if result[SUCCESS]:
        parsed = buienradar.parse(
                                    result[CONTENT], 
                                    latitude=float(args['--latitude']),
                                    longitude=float(args['--longitude'])
                                )
        log.info("Retrieved data:\n%s", parsed)
    else:
        log.error("Retrieving xml weather data was not successfull (%s)", result[MESSAGE])


if __name__ == '__main__':
    # execute only if run as the entry point into the program
    main()