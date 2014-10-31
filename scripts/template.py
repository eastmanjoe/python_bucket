#!/usr/bin/env python
#
#
#
'''
This program starts two modbus slaves for the DAQ code to query.
'''

#---------------------------------------------------------------------------#
import os
import sys
import time
import argparse
import logging
import requests
import subprocess

import logging

def setupLogger(loglevel, log_filename):

    # assuming loglevel is bound to the string value obtained from the
    # command line argument. Convert to upper case to allow the user to
    # specify --log=DEBUG or --log=debug
    loglevel = loglevel.upper()

    numeric_level = getattr(logging, loglevel, None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)

    logger.setLevel(loglevel)

    # configure logger
    handler_stream_formatter = logging.Formatter('%(levelname)s: %(message)s')
    handler_stream = logging.StreamHandler()
    handler_stream.setLevel(loglevel)
    handler_stream.setFormatter(handler_stream_formatter)
    logger.addHandler(handler_stream)

    if log_filename != '':
        log_path = 'C:\\cygwin\\home\\jeastman\\python_bucket\\debug_logs\\'
        # log_path = 'c:\\temp\\'
        # log_path = '/home/jeastman/logs/'
        handler_file = logging.FileHandler(log_path + log_filename)
        # handler_file = logging.FileHandler(log_path + log_filename)
        handler_file_formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s')
        handler_file.setFormatter(handler_file_formatter)
        handler_file.setLevel(loglevel)
        logger.addHandler(handler_file)

    logger.info('Log Level is: %s' % (loglevel))
    logger.info('Log Filename is: %s' % (log_filename))


#---------------------------------------------------------------------------#
if __name__ == '__main__':
    logger = logging.getLogger('logger')

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--sw_file', help='file path and name of Sierra Wireless file',
        default='C:\\Users\\jeastman\\Desktop\\Draker SN List_Truncated.csv'
        )
    parser.add_argument(
        '--sf_file', help='file path and name of SalesForce file',
        default='C:\\Users\\jeastman\\Desktop\\Projects with Cell Modem Report.csv'
        )
    parser.add_argument(
        '-l','--level',
        help='defines the log level to be dispayed to the screen',
        default='info'
        )
    parser.add_argument(
        '-f','--filename', help='defines the filename of the debugs log',
        default=''
        )
    args = parser.parse_args()

    setupLogger(args.level, args.filename)

    logger.info(
        'Script started on: %s' % time.asctime(time.localtime(time.time()))
        )