Python buienradar library
=========================

Library and CLI tools for interacting with buienradar xml/api.

http://xml.buienradar.nl
http://api.buienradar.nl).


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

    $ python buienradar -h
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

