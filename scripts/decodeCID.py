#!/usr/bin/env python
#
#
#
'''
This program decodes the CID of a SD and microSD cards.  The SD card must be
attached directly to CPU via the PCI bus or SD bus and not through the USB bus.

In linux the CID can be accessed via /sys/block/<block device name>/device/cid

Example CID:
    03534453533038478019f5ed3500ec65

    Mfg ID:                 0x03
    OEM ID/Application ID:  0x53, 0x44
    Product Name:           0x5353303847 [ASCII: SS08G]
    Product Revision:       0x80 [BCD: 8.0]
    Serial Number:          0x19f5ed35 [Decimal: 435547445]
    Mfg Date Code:          0x0ec [BCD: 0 14/12]
    CRC7 Checksum:          0x65
'''

#---------------------------------------------------------------------------#
import os
import sys
import time
import argparse
import logging
from subprocess import call
import signal

__version__ = '1.0.0'

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
        #log_path = 'C:\\cygwin\\home\\jeastman\\python_bucket\\debug_logs\\'
        # log_path = 'c:\\temp\\'
        # log_path = '/home/jeastman/logs/'
        log_path = '~/logs/'
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
def signal_handler(signal, frame):
    print ('You pressed Ctrl+C')
    logger.info('Script Stopped on: %s' % time.asctime(
        time.localtime(time.time())))
    sys.exit(0)

def getCID(device):
    filename = '/sys/block/' + device + '/device/cid'

    with open(filename, 'r') as fid:
        data = fid.read()
        data.rstrip('\n')

    return data

def decodeCID(data):

    #03 5344 5353303847 80 19f5ed35 0 0ec 65
    # :  0x53, 0x44
    # Product Name:           0x5353303847 [ASCII: SS08G]
    # Product Revision:       0x80 [BCD: 8.0]
    # Serial Number:          0x19f5ed35 [Decimal: 435547445]
    # Mfg Date Code:          0x0ec [BCD: 0 14/12]
    # CRC7 Checksum:

    decoded_CID = {'mfg ID': int(data[0:2], base=16)}
    decoded_CID['OEM ID'] = int(data[2:4])
    decoded_CID['Application ID'] = int(data[4:6])
    decoded_CID['Product Name'] = data[6:16].decode('hex')
    decoded_CID['Product Revision'] = str(int(data[16:17])) + '.' + str(int(data[17:18]))
    decoded_CID['Serial Number'] = int(data[18:26], base=16)
    decoded_CID['Mfg Date Code'] = str(int(data[27:28], base=16)) + ' ' + str(int(data[28:29], base=16)) + '/' + str(int(data[29:30], base=16))
    decoded_CID['CRC7 Checksum'] = data[30:32]

    logger.debug(decoded_CID)

    return decoded_CID


#---------------------------------------------------------------------------#
if __name__ == '__main__':

    #register Ctrl-C signal handler
    signal.signal(signal.SIGINT, signal_handler)

    logger = logging.getLogger('logger')

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'block_device_name', help='name of the block device to decode the CID'
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
    parser.add_argument(
        '-v', '--version', action='version',version='%(prog)s ' + __version__
        )
    args = parser.parse_args()

    setupLogger(args.level, args.filename)

    logger.info(
        'Script started on: %s' % time.asctime(time.localtime(time.time()))
        )

    CID = {'raw':getCID(args.block_device_name)}
    CID.update(decodeCID(CID['raw']))

    logger.info('The CID is: %s' % CID['raw'])
    logger.info('   Mfg ID: %0#4x' % CID['mfg ID'])
    logger.info('   OEM ID/Application ID: %0#4x, %0#4x' % (CID['OEM ID'], CID['Application ID']))
    logger.info('   Product Name: %s' % CID['Product Name'])
    logger.info('   Product Revision: %s' % CID['Product Revision'])
    logger.info('   Serial Number: %d' % CID['Serial Number'])
    logger.info('   Mfg Date Code: %s' % CID['Mfg Date Code'])
