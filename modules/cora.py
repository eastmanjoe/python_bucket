#!/usr/bin/env python

'''
Run Cora commands
'''

#---------------------------------------------------------------------------#
#import packages
from argparse import ArgumentParser
from threading import Thread, Event
from subprocess import Popen, PIPE, STDOUT, STARTUPINFO, STARTF_USESHOWWINDOW

import os
import sys
import signal
import logging
import time
import json


#---------------------------------------------------------------------------#
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
    logger.info('Script Stopped on: %s' % time.asctime(
        time.localtime(time.time())))
    loggernet.stop()
    sys.exit(0)

#---------------------------------------------------------------------------#
class Cora(Thread):
    '''
    a thread that launches the cora_cmd service and
    connect to the LoggerNet server specifiec
    '''

    def __init__(self, server_ip, username, password, server_port=6789):
        super(Cora, self).__init__()
        self.name = 'Cora'
        self.threadID = 2
        self.stoprequest = Event()
        self.server_ip = server_ip
        self.username = username
        self.password = password
        self.server_port=server_port

        logger.info('starting cmd window')

        # startupinfo = STARTUPINFO()
        # startupinfo.dwFlags |= STARTF_USESHOWWINDOW

        try:
            pass
            self.cterm = Popen(
            'cora', stdin=PIPE, stdout=PIPE, stderr=None,
            universal_newlines=True)

            logger.debug('Startup: {}'.format(self.cterm.stdout.readline()))
            self.cterm.stdout.flush()

        except WindowsError:
            logger.error('cora command not found')
            sys.exit(0)


    def run(self):
        logger.info('connecting to {} with {}:{}'.format(
            self.server_ip, self.username, self.password
            )
        )

        if self.cterm.poll() == None:
            cmd = 'connect ' + self.server_ip

            if self.username != '':
                cmd += ' --name=' + self.username + ' '
                cmd += ' --password=' + self.password + ' '

            if self.server_port != 6789:
                cmd += '--server-port=' + self.server_port

            cmd += ';'

            self.cterm.stdin.write(cmd)

            cora_response = self.cterm.stdout.read()
            self.cterm.stdout.flush()
            logger.debug('Connect Response: {}'.format(cora_response))

            if '+connect' in cora_response:
                logger.info('connected to LoggerNet server: {}'.format(
                    self.server_ip))
            else:
                logger.error('{}'.format(cora_response))
        else:
            logger.error(
                'cannot connect to {} since cora is not running'.format(
                self.server_ip))
            stop()


    def stop(self, timeout=None):
        if self.cterm.poll() == None:
            self.cterm.stdin.write('exit;')
            # cora_response = self.cterm.stdin.write('exit;')
            self.cterm.terminate()

        self.stoprequest.set()
        super(Cora, self).join(timeout)

        logger.info('stopping cora')

    def list_stations(self):

        cmd += 'list-stations;'
        cmd += '}'

    def network_map_xml(self):

        cmd += 'make-xml-network-map --format=xml' + ';'
        cmd += '}'

    def get_data_fill_days(self, station_name):
        cmd += 'get-value ' + station_name + '.Status.DataFillDays(1);'
        cmd += '}'

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


#---------------------------------------------------------------------------#
if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('server_ip', help='ip address of the LoggerNet server')
    parser.add_argument(
        '--username', help='username for LoggerNet server', default=''
        )
    parser.add_argument(
        '--password', help='password for LoggerNet server', default=''
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

    #register Ctrl-C signal handler
    signal.signal(signal.SIGINT, signal_handler)

    logger = logging.getLogger('logger')
    setupLogger(args.level, args.filename)

    loggernet = Cora(args.server_ip, args.username, args.password)
    loggernet.start()
    # loggernet.list_devices()
    loggernet.stop()


    # list_devices(args.server_ip, args.username, args.password)