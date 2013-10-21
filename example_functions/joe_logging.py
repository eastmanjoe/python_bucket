#!/usr/bin/env python
'''
The purpose of the script is to setup loggers

The .csv file has headers on the first line
'''
import logging
import sys

#---------------------------------------------------------------------------#
def setupLogger(loglevel, logfilename):
    # assuming loglevel is bound to the string value obtained from the
    # command line argument. Convert to upper case to allow the user to
    # specify --log=DEBUG or --log=debug
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)

    # configure logger
    logger.setLevel(loglevel.upper())
    handler_stream_formatter = logging.Formatter('%(levelname)s: %(message)s')
    handler_stream = logging.StreamHandler()
    handler_stream.setFormatter(handler_stream_formatter)
    handler_stream.setLevel(loglevel.upper())
    logger.addHandler(handler_stream)
    logger.info('Log Level is: %s' % (loglevel))

    if logfilename != '':
        # handler_file = logging.FileHandler('/home/jeastman/logs/' + logfilename)
        handler_file = logging.FileHandler(logfilename)
        handler_file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        handler_file.setFormatter(handler_file_formatter)
        handler_file.setLevel(loglevel.upper())
        logger.addHandler(handler_file)
        logger.info('Log Filename is: %s' % (logfilename))

#---------------------------------------------------------------------------#

#---------------------------------------------------------------------------#
if __name__ == '__main__':

    # sys.stdout.write('argv is: %s\n\r' % (sys.argv[1:]))
    parser = argparse.ArgumentParser()
    parser.add_argument('-l','--level', help='defines the log level to be dispayed to the screen and writen to log file', default='info')
    parser.add_argument('-lf','--log_filename', help='defines the filename of the log file', default='')
    parser.add_argument('filename', help='defines the filenames to be parsed', default='', nargs='+')
    args = parser.parse_args()
    # sys.stdout.write('args is: %s\n\r' % (args))

    # args = parseARGS(sys.argv[1:])

    # start-up logger
    logger = logging.getLogger('parse_csv_file')

    # setupLogger('debug', 'modbus_log.log')
    setupLogger(args.level, args.log_filename)