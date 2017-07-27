#!/usr/bin/env python
#
#
#
'''
This module implements the UMB protocol for Lufft.

Reset to factory defaults:
    01 10 01 00 01 F0 03 02 25 10 11 03 4E 91 04

Query Wsx-UMB of actual temp (in Deg C) with ID: 1
    01 10 01 70 01 F0 05 02 2F 10 01 64 00 03 71 4B 04

Query Wsx-UMB of actual temp (in Deg C) with ID: 200
    01 10 C8 70 01 F0 05 02 2F 10 01 64 00 03 68 3D 04

'''

#---------------------------------------------------------------------------#
import os
from sys import exit
from time import sleep, localtime, time, asctime
import argparse
import logging
import signal
import serial
import struct

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
def signal_handler(signal, frame):
    print ('You pressed Ctrl+C')
    logger.info('Script Stopped on: %s' % asctime(
        localtime(time())))
    exit(0)


#---------------------------------------------------------------------------#
def calc_crc16(data, byteorder='little_endian'):
    crc = 0xFFFF

    for n in data:
        for i in range(0, 8):
            if (crc & 0x0001) ^ (n & 0x01):
                x16 = 0x8408
            else:
                x16 = 0x0000

            crc = crc >> 1
            crc ^= x16
            n = n >> 1

    if byteorder == 'little_endian':
        lsb = crc & 0x00FF
        msb = crc >> 8
    elif byteorder == 'big_endian':
        lsb = crc >> 8
        msb = crc & 0x00FF

    return [lsb, msb]


#---------------------------------------------------------------------------#
class UMBDevice(object):
    """docstring for UMBDevice"""
    def __init__(self, com_port, baud_rate):
        super(UMBDevice, self).__init__()
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.umb_header_version = 0x10
        self.sender_address = [0xF0, 0x01]

        self.umb_command = {
            'Multi-Channel Online Data': [0x2F, 0x10],
            'HW/SW Version': [0x20, 0x10],
            'New Device ID': [0x30, 0x10]
        }

        self.reciever_address = [0x70, 0x01]

        self.port = serial.Serial(
            port=self.com_port,
            baudrate=self.baud_rate,
            parity=serial.PARITY_NONE,
            stopbits=1,
            bytesize=serial.EIGHTBITS,
            xonxoff=False,
            timeout=5.0
            )

        if self.port.isOpen():
            self.port.close()

        self.port.open()

        # SOH
        self.command = [0x01]

        self.command.append(self.umb_header_version)

        self.command.append(self.reciever_address[1])
        self.command.append(self.reciever_address[0])

        self.command.append(self.sender_address[1])
        self.command.append(self.sender_address[0])

        # num_bytes
        self.command.append(0x05)

        # STX
        self.command.append(0x02)

        # request command
        self.command.append(self.umb_command['Multi-Channel Online Data'][0])

        # command version
        self.command.append(self.umb_command['Multi-Channel Online Data'][1])
        # command.append(0x10)

        # data
        self.command.append(0x01)
        self.command.append(0x64)
        self.command.append(0x00)

        # ETX
        self.command.append(0x03)


    def scan(self):

        command = list(self.command)


        for x in xrange(1,255):
            logger.info('Device ID: {} - Trying Query'.format(x))

            # set reciever address
            command[2] = x

            logger.debug('pre-crc: {}'.format(command))

            crc = calc_crc16(command)

            logger.debug('post-crc: {}'.format(command))

            # join the lists to a single serial string
            command_str = "".join([chr(x) for x in command])
            command_str += "".join([chr(x) for x in crc])

            # EOT
            command_str += chr(0x04)

            logger.debug('sent: {}'.format(command_str.encode('hex')))

            self.port.write(command_str)

            sleep(5)

            bytes_returned = self.port.inWaiting()

            if bytes_returned > 0:
                logger.info('Device ID: {} - Responded'.format(x))
                logger.debug('{}'.format(self.port.read(bytes_returned)))

            self.port.flushInput()

    def change_id():

        command = list(self.command)



    def close(self):
        self.port.close()


    def change_baud(self, baud_rate):
        self.port.baud_rate = baud_rate


#---------------------------------------------------------------------------#
if __name__ == '__main__':

    #register Ctrl-C signal handler
    signal.signal(signal.SIGINT, signal_handler)

    logger = logging.getLogger('logger')


    parser = argparse.ArgumentParser()
    parser.add_argument(
        'com_port', help='serial port to use to connect to Lufft Weather Station',
        default=''
        )
    parser.add_argument(
        '--baud_rate', help='baud rate of serial port', type=int,
        default='19200'
        )
    parser.add_argument(
        '--scan', help='scan the serial bus for a device', type=bool,
        default='False'
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
        'Script started on: %s' % asctime(localtime(time()))
        )

    bus = UMBDevice(args.com_port, args.baud_rate)
    bus.scan()
    bus.close()

    logger.info(
        'Script stopped on: %s' % asctime(localtime(time()))
        )
