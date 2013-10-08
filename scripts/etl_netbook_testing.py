#!/usr/bin/env python

'''
Intertek Certification Program run on Netbook.
This program is used to provide the Pass/Fail indicator to the EMC testing team.
'''

#---------------------------------------------------------------------------#
#import packages
import os
import sys
import argparse
import time
import logging
import threading
import pymodbus
from pymodbus.client.sync import ModbusTcpClient as ModbusTcpClient
import math
#---------------------------------------------------------------------------#

#---------------------------------------------------------------------------#
# data validation
import json
import requests
#---------------------------------------------------------------------------#

#---------------------------------------------------------------------------#
def parseARGS(argv):
    # sys.stdout.write('argv is: %s\n\r' % (argv))

    parser = argparse.ArgumentParser()
    parser.add_argument('-l','--level', help='defines the log level to be dispayed to the screen', default='info')
    parser.add_argument('-f','--filename', help='defines the filename of the debugs log', default='')
    args = parser.parse_args()
    # sys.stdout.write('args is: %s\n\r' % (args))

    return (args.level, args.filename)
#---------------------------------------------------------------------------#

#---------------------------------------------------------------------------#
# def setupLogger(argv):
def setupLogger(loglevel, logfilename):
    # assuming loglevel is bound to the string value obtained from the
    # command line argument. Convert to upper case to allow the user to
    # specify --log=DEBUG or --log=debug
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)

    # configure logger
    logger.setLevel(logging.DEBUG)
    handler_stream_formatter = logging.Formatter('%(levelname)s: %(message)s')
    handler_stream = logging.StreamHandler()
    handler_stream.setFormatter(handler_stream_formatter)
    handler_stream.setLevel(loglevel.upper())
    logger.addHandler(handler_stream)

    if logfilename != '':
        handler_file = logging.FileHandler('/home/jeastman/logs/' + logfilename)
        logger.debug('Log Filename is: %s' % (handler_file))
        handler_file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        handler_file.setFormatter(handler_file_formatter)
        # handler_file.setLevel(level.DEBUG)
        logger.addHandler(handler_file)

    logger.debug('Log Level is: %s' % (loglevel))
    logger.debug('Log Filename is: %s' % (logfilename))
#---------------------------------------------------------------------------#


#---------------------------------------------------------------------------#
#---------------------------------------------------------------------------#
class dataValidation(threading.Thread):
    """docstring for dataValidation"""
    def __init__(self):
        super(dataValidation, self).__init__()
        self.threadID = 2
        self.name = 'data_validation'
        self.stoprequest = threading.Event()
        self.begintest = False
        self.testrunning = False
        self.modbusclient = ModbusTcpClient(host='172.28.0.41', port=502)


    def run(self):
        start_test_data = {}
        current_data = {}

        while not self.stoprequest.isSet():
            logger.info('%s' % time.strftime('%Y-%m-%d %H:%M:%S'))
            if self.testrunning: logger.info('Test is in-process')
            else: logger.info('Waiting for test to start')


            try:
                device_data = getJsonData('http://172.28.0.1/latest_data.json')
            except requests.exceptions.ConnectionError:
                logger.error('cannot connect to the site server, check all cable connections.')

            # environmental data
            try:
                licor_constant = -74.73 * 1000

                current_data['irradiance'] = device_data['alpha']['env']['IRRA-1']['irradiance_1'] * licor_constant

                cell_temp = {'A': 1.129241e-3, 'B': 2.341077e-4, 'C': 8.775468e-8}
                cell_temp['v_ratio'] = 5 / device_data['alpha']['env']['cts-1']['cell_temp_01']
                cell_temp['resistance'] = 24900/ (cell_temp['v_ratio'] - 1)
                cell_temp['temperature'] = (1 / (cell_temp['A'] + (cell_temp['B'] * math.log(cell_temp['resistance'])) + (cell_temp['C'] * pow(math.log(cell_temp['resistance']), 3)))) - 273.15

                current_data['cell_temp'] = cell_temp['temperature']

                logger.debug('%s: %s' % (device_data['alpha']['env']['ESI-1']['identifier'], device_data['alpha']['env']['ESI-1']['serial_number']))
                logger.debug('irradiance: %.2f W/m2' % (current_data['irradiance']))
                logger.debug('cell temperature: %.2f Degrees C' % (current_data['cell_temp']))

                if self.begintest:
                    start_test_data['irradiance'] = current_data['irradiance']
                    start_test_data['cell_temp'] = current_data['cell_temp']

                if self.testrunning:
                    logger.info('prev_irradiance: %.2f' % (start_test_data['irradiance']))
                    logger.info('prev_cell_temp: %.2f' % (start_test_data['cell_temp']))

                logger.info('curr_irradiance: %.2f' % (current_data['irradiance']))
                logger.info('curr_cell_temp: %.2f' % (current_data['cell_temp']))

                if self.testrunning:
                    # check env data
                    if (-25 < (start_test_data['irradiance'] - current_data['irradiance']) < 25):
                        logger.info('irradiance value within acceptable limits')
                        logger.debug('difference is: %.2f' % (start_test_data['irradiance'] - current_data['irradiance']))
                    else:
                        logger.error('irradiance value outside of acceptable limits')
                        logger.debug('difference is: %.2f' % (start_test_data['irradiance'] - current_data['irradiance']))

                    if (-5 < (start_test_data['cell_temp'] - current_data['cell_temp']) < 5):
                        logger.info('cell temperature value within acceptable limits')
                        logger.debug('difference is: %.2f' % (start_test_data['cell_temp'] - current_data['cell_temp']))
                    else:
                        logger.error('cell temperature value outside of acceptable limits')
                        logger.debug('difference is: %.2f' % (start_test_data['cell_temp'] - current_data['cell_temp']))

            except KeyError:
                logger.error('ENV data unavailable')

            # MBS-1 data
            try:
                mbs_data = []
                for i in range(1, 11):
                    mbs_data.append(device_data['alpha']['mbs1']['MBS-1']['value%02d' % (i)])
                logger.debug('%s data: %s' % (device_data['alpha']['mbs1']['MBS-1']['identifier'], mbs_data))

                # for i in range(1, 11):
                #     logger.debug('%s data: %s' % (device_data['alpha']['mbs1']['MBS-1']['identifier'], device_data['alpha']['mbs1']['MBS-1']['value%02d' % (i)]))

                if self.testrunning:
                    # check modbus data
                    if checkModbusData('MBS-1', device_data['alpha']['mbs1']['MBS-1']):
                        logger.info('MBS-1: Modbus Data VALID')
                    else:
                        logger.error('MBS-1: Modbus Data INVALID')

            except KeyError:
                logger.error('MBS-1 data unavailable')

            # MBS-2 data
            try:
                mbs_data = []
                for i in range(1, 11):
                    mbs_data.append(device_data['alpha']['mbs2']['MBS-2']['value%02d' % (i)])
                logger.debug('%s data: %s' % (device_data['alpha']['mbs2']['MBS-2']['identifier'], mbs_data))
                # for i in range(1, 11):
                #     logger.debug('%s data: %s' % (device_data['alpha']['mbs2']['MBS-2']['identifier'], device_data['alpha']['mbs2']['MBS-2']['value%02d' % (i)]))

                if self.testrunning:
                    if checkModbusData('MBS-2', device_data['alpha']['mbs2']['MBS-2']):
                        logger.info('MBS-2: Modbus Data VALID')
                    else:
                        logger.error('MBS-2: Modbus Data INVALID')

            except KeyError:
                logger.error('MBS-2 data unavailable')

            #sixnet data
            try:
                # try:
                    if not self.modbusclient.connect():
                        logger.error('failing to connect to sixnet Ethernet switch for Modbus query')

                    sixnet_link_status = self.modbusclient.read_discrete_inputs(0, 8, unit=11)
                    sixnet_pwr_status = self.modbusclient.read_discrete_inputs(29, 3, unit=11)

                    if self.begintest:
                        start_test_data['link_bits'] = sixnet_link_status.bits
                        start_test_data['status_bits'] = sixnet_pwr_status.bits

                    if self.testrunning:
                        logger.debug('prev_link_bits: %s' % (start_test_data['link_bits']))
                        logger.debug('prev_status_bits: %s' % (start_test_data['status_bits']))

                    logger.debug('curr_link_bits: %s' % (sixnet_link_status.bits))
                    logger.debug('curr_status_bits: %s' % (sixnet_pwr_status.bits))


                    if self.testrunning:
                        if start_test_data['link_bits'] != sixnet_link_status.bits:
                            logger.error('sixnet "link" status has changed')
                        elif start_test_data['status_bits'] != sixnet_pwr_status.bits:
                            logger.error('sixnet "OK" status has changed')
                        else:
                            logger.info('sixnet switch status is good')


                # except KeyError:
                    # logger.error('sixnet data unavailable')
            except pymodbus.exceptions.ConnectionException:
                logger.error('Sixnet Modbus query failed')

            if self.begintest:
                self.begintest = False
                self.testrunning = True

            time.sleep(5)
            os.system('clear')

        self.modbusclient.close()

    def join(self, timeout=None):
        if self.testrunning:
            logger.info('Stopping Test...')
            self.testrunning = False

        self.stoprequest.set()
        super(dataValidation, self).join(timeout)

    def starttest(self, timeout=None):
        self.begintest = True

    def stoptest(self, timeout=None):
        self.testrunning = False
#---------------------------------------------------------------------------#
#---------------------------------------------------------------------------#


#---------------------------------------------------------------------------#
def getJsonData(url):

    resp = requests.get(url, timeout=3)

    data = resp.json()

    return data
#---------------------------------------------------------------------------#

#---------------------------------------------------------------------------#
def checkModbusData(device_number, data):

    mbs_1_dictonary = {'value01': 10,'value02': 11,'value03': 12,'value04': 13,'value05': 14,'value06': 15,'value07': 16,
        'value08': 17,'value09': 18,'value10': 19}

    mbs_2_dictonary = {'value01': 20,'value02': 21,'value03': 22,'value04': 23,'value05': 24,'value06': 25,'value07': 26,
        'value08': 27,'value09': 28,'value10': 29}

    if device_number == 'MBS-1':
        for value in mbs_1_dictonary:
            if data[value] == mbs_1_dictonary[value]:
                pass
            else:
                return False

    elif device_number == 'MBS-2':
        for value in mbs_2_dictonary:
            if data[value] == mbs_2_dictonary[value]:
                pass
            else:
                return False

    return True
#---------------------------------------------------------------------------#

#---------------------------------------------------------------------------#
if __name__ == "__main__":

    # start-up logger
    logger = logging.getLogger('etl_testing')

    args = parseARGS(sys.argv[1:])
    # sys.stdout.write('Log Level is: %s\n\rLog Filename is: %s\n\r' % (args[0], args[1]))

    # setupLogger('debug', 'etl_testing.log')
    setupLogger(args[0], args[1])

    os.system('clear')
    logger.info('Running...')

    # start data thread
    validate_data_thread = dataValidation()
    validate_data_thread.start()

    # wait for user input
    while True:
        cmd = sys.stdin.readline()
        args = cmd.split(' ')

        if cmd.find('quit')==0:
            validate_data_thread.join()
            logger.info('bye-bye...')
            break
        elif cmd.find('restart')==0:
            os.system('clear')

            # stop validate_data_thread
            validate_data_thread.join()

            # tell user restarting in 30 seconds
            logger.info('Restarting in %i seconds' % (30))

            for i in range(1, 31):
                if (((30 - i) % 5) == 0) and ((30 - i) != 0):
                    logger.info('Restarting in %i seconds' % (30 - i))
                elif (2 <= (30 - i) <= 4):
                    logger.info('Restarting in %i seconds' % (30 - i))
                elif (30 - i) == 1:
                    logger.info('Restarting in %i second' % (30 - i))

                time.sleep(1)

            # restart validate_data_thread
            validate_data_thread = dataValidation()
            validate_data_thread.start()
            logger.info('Restarted...')
        elif cmd.find('start')==0:
            os.system('clear')
            logger.info('Starting Test...')
            validate_data_thread.starttest()
        elif cmd.find('stop')==0:
            logger.info('Stopping Test...')
            validate_data_thread.stoptest()
        elif cmd.find('help')==0:
            sys.stdout.write('enter "start" to start the test\r\n')
            sys.stdout.write('enter "stop" to stop the test\r\n')
            sys.stdout.write('enter "restart" to restart the testing, if errors recieved\r\n')
        else:
            sys.stdout.write('unknown command %s\r\n' % (args[0]))
