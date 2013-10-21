#!/usr/bin/env python

# The purpose of the script is to import a .csv file
# and parse it for future processing
#
# The .csv file has headers on the first line
#


import sys
import argparse
import os
import sys
import logging
import collections
import csv
import time

#---------------------------------------------------------------------------#
# def parseARGS(argv):
    # sys.stdout.write('argv is: %s\n\r' % (argv))
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-v','--verbose', help='enables/disable modbus-tk verbose mode', default='False')
    # parser.add_argument('-l','--level', help='defines the log level to be dispayed to the screen and writen to log file', default='info')
    # parser.add_argument('-lf','--log_filename', help='defines the filename of the log file', default='')
    # parser.add_argument('filename', help='defines the filenames to be parsed', default='', nargs='+')
    # args = parser.parse_args()
    # sys.stdout.write('args is: %s\n\r' % (args))

    # return (args.filename, args.verbose, args.level, args.log_filename)
#---------------------------------------------------------------------------#

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
    # logger.setLevel('INFO')
    handler_stream_formatter = logging.Formatter('%(levelname)s: %(message)s')
    handler_stream = logging.StreamHandler()
    handler_stream.setFormatter(handler_stream_formatter)
    # handler_stream.setLevel(loglevel.upper())
    handler_stream.setLevel('INFO')
    logger.addHandler(handler_stream)
    logger.info('Log Level is: %s' % (loglevel))

    if logfilename != '':
        # handler_file = logging.FileHandler('/home/jeastman/logs/' + logfilename)
        handler_file = logging.FileHandler(logfilename)
        logger.debug('Log Filename is: %s' % (handler_file))
        handler_file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        handler_file.setFormatter(handler_file_formatter)
        handler_file.setLevel(loglevel.upper())
        logger.addHandler(handler_file)
        logger.info('Log Filename is: %s' % (logfilename))

#---------------------------------------------------------------------------#

#---------------------------------------------------------------------------#
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
#---------------------------------------------------------------------------#

#---------------------------------------------------------------------------#
def parseLine(datfile):
    line = datfile.readline().strip()

    if not line:
        return 'EOF'
    else:
        split_line = line.split('","')

#        for i in range(len(split_line)):
#            split_line[i] = split_line[i].strip('"')

        return split_line
#---------------------------------------------------------------------------#

#---------------------------------------------------------------------------#
def parseFile(datfile):
    data = []

    row_data = parseLine(datfile)

    # Make sure file has data
    if row_data != "EOF":
        while True:
            data.append(row_data)
            row_data = parseLine(datfile)

            if row_data == "EOF":
                print "End Of File"
                break

    else:
        data = "EOF"

    datfile.close()
    return data
#---------------------------------------------------------------------------#

#---------------------------------------------------------------------------#
def openFile(file_pth):
    """Check file extension"""
    if file_pth.endswith('.csv'):
        file_id = open(file_pth, 'r')
    else:
        file_id = ''
        print 'Wrong file type'

    return file_id
#---------------------------------------------------------------------------#

#---------------------------------------------------------------------------#
if __name__ == '__main__':

    # sys.stdout.write('argv is: %s\n\r' % (sys.argv[1:]))
    parser = argparse.ArgumentParser()
    parser.add_argument('-ll','--level', help='defines the log level to be dispayed to the screen and writen to log file', default='info')
    parser.add_argument('-lf','--log_filename', help='defines the filename of the log file', default='')
    parser.add_argument('filename', help='defines the filenames to be parsed', default='', nargs=2)
    parser.add_argument('column_name', help='defines the column to be compared to be parsed', default='')
    args = parser.parse_args()
    # sys.stdout.write('args is: %s\n\r' % (args))

    # args = parseARGS(sys.argv[1:])

    # start-up logger
    logger = logging.getLogger('parse_csv_file')

    # setupLogger('debug', 'modbus_log.log')
    setupLogger(args.level, args.log_filename)

    logger.debug('#---------------------------------------------------------------------------#')
    logger.debug('#---------------------------------------------------------------------------#')
    logger.debug('#---------------------------------------------------------------------------#')

    #timestamp
    localtime = time.asctime(time.localtime(time.time()) )
    logger.info('Script was started on: %s' % localtime)

    logger.info('File #1 is: %s', args.filename[0])
    logger.info('File #2 is: %s', args.filename[1])
    logger.info('Column Name to be compared: %s', args.column_name)


    #---------------------------------------------------------------------------#
    column_to_search = 9999

    with open(args.filename[0], 'rb') as csv_file_1_read:
            with open('C:\\Draker\\PandV\\merging_databases\misc_eng_parts.csv', 'wb') as csv_file_write:
                csv_file_1_reader = csv.reader(csv_file_1_read, delimiter=',')
                csv_file_writer = csv.writer(csv_file_write, delimiter=',')


                for row in csv_file_1_reader:
                    row_data_in_file_2 = False

                    if row:
                        if args.column_name in row and column_to_search == 9999:
                            column_to_search = row.index(args.column_name)
                            logger.info('Searching Column: %d', column_to_search)

                        logger.debug('Searching: %s', row[column_to_search])

                        with open(args.filename[1], 'rb') as csv_file_2_read:
                            csv_file_2_reader = csv.reader(csv_file_2_read, delimiter=',')

                            for line in csv_file_2_reader:
                                if line:
                                    if row[column_to_search] in line:
                                        row_data_in_file_2 = True
                                        logger.debug('Part Number found in File 2: %s', row[column_to_search])
                                        break

                                    else:
                                        row_data_in_file_2 = False
                                else:
                                    logger.debug('End of File')
                                    break

                        if not row_data_in_file_2 or args.column_name in row:
                            csv_file_writer.writerow(row)
                        else:
                            logger.debug('Row Data is in File 2: %s', row[column_to_search])
                    else:
                        logger.debug('#---------------------------------------------------------------------------#')
                        logger.debug('#---------------------------------------------------------------------------#')
                        logger.debug('#---------------------------------------------------------------------------#')
                        break
    #---------------------------------------------------------------------------#

#---------------------------------------------------------------------------#