#!/usr/bin/python
# -*- coding: utf-8 -*-

# urllib-tester - Web service connection tester.
# Copyright (C) 2017  Hakan Bayindir
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Import core packages first.
import os
import sys

# Then utilities.
import argparse
import logging
import urllib2

if __name__ == '__main__':

    # This is the global logging level. Will be changed with verbosity if required in the future.
    LOGGING_LEVEL = logging.ERROR

    # Let's start with building the argument parser.
    argumentParser = argparse.ArgumentParser()
    argumentParser.description = 'Try to connect web services with urllib2 and report errors.'

    argumentParser.add_argument ('-v', '--verbose', help = 'Print more detail about the process.', action = 'count')
    argumentParser.add_argument ('-q', '--quiet', help = 'Do not print anything to console.', action = 'store_true') # Will override --verbose.

    # Ability to handle version in-library is nice.
    argumentParser.add_argument ('-V', '--version', help = 'Print ' + argumentParser.prog + ' version and exit.', action = 'version', version = argumentParser.prog + ' version 0.0.1')

    # Mandatory FILE(s) argument. nargs = '+' means "at least one, but can provide more if you wish"
    argumentParser.add_argument ('ADDRESS', help = 'Host or IP address to be tested.', nargs = '+')

    arguments = argumentParser.parse_args()

    # At this point we have the required arguments, let's start with logging duties.
    if arguments.verbose != None :
        if arguments.verbose == 1:
            LOGGING_LEVEL = logging.WARN
        elif arguments.verbose == 2:
            LOGGING_LEVEL = logging.INFO
        elif arguments.verbose >= 3:
            LOGGING_LEVEL = logging.DEBUG

    # Set the logging level first:
    try:
        logging.basicConfig (filename = None, level = LOGGING_LEVEL,
                             format = '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
                             datefmt = '%Y-%m-%d %H:%M:%S')

        # Get the loca"l logger and start.
        localLogger = logging.getLogger (argumentParser.prog)

        localLogger.debug ('Logger setup completed.')
        localLogger.debug ('%s is starting.', sys.argv[0])
    except IOError as exception:
        print ('Something about disk I/O went bad: ' + str(exception))
        sys.exit (1)

    localLogger.debug ('Parsed arguments are %s', arguments)

    try:
        response = urllib2.urlopen(arguments.ADDRESS[0])
        logging.info ('The request for %s has returned %s.', arguments.ADDRESS[0], response.code)
    except ValueError as exception:
        print (exception)
        sys.exit (2)
