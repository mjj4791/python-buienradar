"""Buienradar library to get parsed weather data from buienradar.nl."""
import logging

from buienradar.buienradar_json import get_json_data, parse_json_data
from buienradar.buienradar_xml import get_xml_data, parse_xml_data
from buienradar.constants import (
    __BRCONDITIONS,
    CONDCODE,
    CONDITION,
    DETAILED,
    EXACT,
    EXACTNL
)

log = logging.getLogger(__name__)


def get_data(latitude=52.091579, longitude=5.119734, usexml=False):
    """Get buienradar xml data and return results."""
    if usexml:
        log.info("Getting buienradar XML data for latitude=%s, longitude=%s",
                 latitude, longitude)
        return get_xml_data(latitude, longitude)
    else:
        log.info("Getting buienradar JSON data for latitude=%s, longitude=%s",
                 latitude, longitude)
        return get_json_data(latitude, longitude)


def parse_data(content, raincontent, latitude=52.091579,
               longitude=5.119734, timeframe=60, usexml=False):
    """Parse the raw data and return as data dictionary."""
    if usexml:
        return parse_xml_data(content, raincontent,
                              latitude, longitude, timeframe)
    else:
        return parse_json_data(content, raincontent,
                               latitude, longitude, timeframe)


def condition_from_code(condcode):
    """Get the condition name from the condition code."""
    if condcode in __BRCONDITIONS:
        cond_data = __BRCONDITIONS[condcode]

        return {CONDCODE: condcode,
                CONDITION: cond_data[0],
                DETAILED: cond_data[1],
                EXACT: cond_data[2],
                EXACTNL: cond_data[3],
                }
    return None
