#!/usr/bin/env python

'''
Run Cora commands
'''

#---------------------------------------------------------------------------#
#import packages
from argparse import ArgumentParser
from threading import Thread, Event
# from subprocess import Popen, PIPE, STDOUT, STARTUPINFO, STARTF_USESHOWWINDOW
import subprocess
from logging.config import fileConfig

import os
import sys
import signal
import logging
import time
import json
import re

__version__ = '0.0.1'
#---------------------------------------------------------------------------#
def signal_handler(signal, frame):
    print ('You pressed Ctrl+C')
    logger.info('Script Stopped on: %s' % time.asctime(
        time.localtime(time.time())))
    sys.exit(0)

#---------------------------------------------------------------------------#
class Cora(Thread):
    '''
    a thread that launches the cora_cmd service and
    connect to the LoggerNet server specifiec
    '''

    def __init__(self, server_ip, username, password, server_port=6789):
        self.server_ip = server_ip
        self.username = username
        self.password = password
        self.server_port = server_port

        cora_connect = 'connect ' + server_ip + ' '
        cora_connect += '--name="' + username + '" '
        cora_connect += '--password="' + password + '" '
        cora_connect += '--server-port=' + str(server_port)
        cora_connect += ';'

        self.cora = ['cora --echo=on --input={', cora_connect, '','}']

    def list_stations(self):

        station_list = []
        station_name = re.compile(r'\{\{(?P<station_name>.*)\}\s+\d+\}')

        self.cora[2] += 'list-stations;'

        cora_output = subprocess.check_output(' '.join(self.cora))
        # logger.debug('{}'.format(cora_output))

        if 'unsupported message' in cora_output:
            logger.error('"list-stations" command not supported by LoggerNet server')
            return []

        elif 'invalid security' in cora_output:
            logger.error('Server security prevented this command from executing.')
            return []

        elif 'orphaned session' in cora_output:
            logger.error('The connection to the server was lost while this command was executing.')
            return []

        elif 'connection lost' in cora_output:
            logger.error('The connection to the server was lost while this command was executing.')
            return []

        else:
            for line in cora_output.split('\n'):
                # logger.debug('{}'.format(line.strip()))
                sn_match =  station_name.match(line.strip())
                if sn_match:
                    station_list.append(sn_match.group('station_name'))

            return station_list

    def list_files(self, station_name):
        regex = re.compile(r"^list-files \{(.*)\};")
        error = re.compile(r"-list-files,(?P<error_message>.+)", re.MULTILINE)
        cpu_file = re.compile(r"^\{CPU:\w.+")

        file_list = {}

        self.cora[2] += 'list-files ' + station_name + ';'

        cora_output = subprocess.check_output(' '.join(self.cora))

        logger.debug('{}'.format(cora_output))

        error_str = error.search(cora_output)

        if error_str:
            if 'Expected the device name' == error_str.group('error_message').strip():
                logger.error('The name of the device is expected as the first argument.')

            elif 'unknown' == error_str.group('error_message').strip():
                logger.error('The server sent a response code that corascript is unable to recognise')

            elif 'session failure' == error_str.group('error_message').strip():
                logger.error('The server connection was lost while the transaction was executing.')

            elif 'invalid device name' == error_str.group('error_message').strip():
                logger.error("The device name specified does not exist in the server's network map.")

            elif 'blocked by server' == error_str.group('error_message').strip():
                logger.error('Server security prevented the command from executing.')

            elif 'unsupported' == error_str.group('error_message').strip():
                logger.error('The server or the specified device does not support the command.')

            elif 'blocked by logger' == error_str.group('error_message').strip():
                logger.error('The security code setting for the specified device is not valid.')

            elif 'communication disabled' == error_str.group('error_message').strip():
                logger.info('Communication with the datalogger is disabled.')

            elif 'communication failed' == error_str.group('error_message').strip():
                logger.error('Communication with the datalogger failed.')

            return error_str.group('error_message').strip()
        else:
            for line in cora_output.split('\n'):
                line = line.strip()

                if re.match(r"^\{CPU:\w.+", line):
                    file_info = line.split(' ')

                    file_list['Filename'] = file_info[0]

                    for parameter in file_info[1:].split('='):
                        file_list[parameter[0]] = parameter[1]

                # logger.info('{}'.format(file_list))

            return file_list

    def network_map_xml(self):

        cmd = 'make-xml-network-map --format=xml;'

    def get_data_fill_days(self, station_name):
        self.cora[2] = 'get-value ' + station_name + '.Status.DataFillDays(1);'


    def list_devices(self):
        '''
        get a list of the devices on the loggernet server
        '''
        self.cterm.stdin.write('list-devices;')
        list_of_devices = self.cterm.stdout.read()
        self.cterm.stdout.flush()
        # print list_of_devices
        logger.debug ('{}'.format(list_of_devices))
        # cmd = 'list-devices;}'

        # print cora_cmd

        # run list-device cora script command to get list of devices on server
        # output = subprocess.Popen(
        #       cora_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        #       )
        # list_of_devices, error = output.communicate()
        # list_of_devices = self.cterm.communicate(cora_cmd + cmd)

        # Extract the device list
        # list_of_devices = list_of_devices[list_of_devices.find(
        #    '*list-devices'):list_of_devices.find('+list-devices'
        #    )]
        # list_of_devices = list_of_devices.strip('*list-devices')
        # list_of_devices = list_of_devices.strip('\r\n')
        # list_of_devices = list_of_devices.split('\r\n')

        # print list_of_devices

        # device_list = []

        # for device in list_of_devices[1:len(list_of_devices) - 1]:
        #     # start = device.find('{')
        #     # stop = device.find('}')
        #     # device = device[start + 1:len(device) - 1]

        #     device = device.replace('{', ')
        #     device = device.replace('}', ')
        #     device = device.split()

        #     device_list.append(device)

        # print device_list

        # outFile = open('LoggerNet_' + self.server_ip + '_Settings.xml', 'w')
        # doc.write(outFile)

    def get_program_stats(self, station_name):
        cmd = 'get-program-stats ' + station_name + ';'


#---------------------------------------------------------------------------#
if __name__ == '__main__':

    loggernet_servers = {
        "localhost": "localhost", "LN1": "98.129.42.26", "LN2": "98.129.42.29",
        "LN3": "98.129.42.31", "LN4": "67.192.199.229", "LN5": "67.192.199.230",
        "LN6": "67.192.199.228", "LN7": "98.129.111.74", "LN8": "67.192.161.134",
        "LN9": "67.192.161.135", "LN10": "104.130.151.188", "LN11": "104.197.108.210",
        "all": "all servers"
        }

    station = {}

    parser = ArgumentParser()
    parser.add_argument(
        'server_ip', help='ip address of the LoggerNet server', default=''
        )
    parser.add_argument(
        '--username', help='username for LoggerNet server', default='Joe'
        )
    parser.add_argument(
        '--password', help='password for LoggerNet server', default='w4LdL4fe'
        )
    parser.add_argument(
        '-v', '--version', action='version',version='%(prog)s ' + __version__
        )
    args = parser.parse_args()

    #register Ctrl-C signal handler
    signal.signal(signal.SIGINT, signal_handler)

    fileConfig('cora.ini')
    logger = logging.getLogger('cora')

    loggernet = Cora(args.server_ip, args.username, args.password)
    # station_list = loggernet.list_stations()
    # logger.info('{}'.format(station_list))

    # for station_name in station_list:
    #     station[station_name] = {}
    #     station[station_name]['list-files'] = loggernet.list_files(station_name)

    # station_name = 'draker_22-north'
    station_name = 'swinerton_water-treatment'
    # station_name = 'Unisolar_hunter-panels'
    station[station_name] = {}
    station[station_name]['list-files'] = loggernet.list_files(station_name)

    logger.info('{}'.format(station))