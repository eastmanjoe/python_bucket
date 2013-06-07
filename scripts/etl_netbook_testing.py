#!/usr/bin/env python

'''
Intertek Certification Program run on Netbook.
This program is used to provide the Pass/Fail indicator to the EMC testing team.
This program also starts two modbus slaves for the DAQ code to query.
'''

#---------------------------------------------------------------------------#
#import packages
import os
import sys
import getopt
import time
import logging
import threading
from pymodbus.client.sync import ModbusTcpClient as ModbusTcpClient
#---------------------------------------------------------------------------#

#---------------------------------------------------------------------------#
# data validation
import json
import requests
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

    def run(self):
        client = ModbusTcpClient('localhost', port=8502)
        client.connect()

        while not self.stoprequest.isSet():
            # device_data = getJsonData('http://172.28.0.1/latest_data.json')
            device_data = getJsonData('http://localhost:8080/latest_data.json')

            sixnet_link_status = client.read_discrete_inputs(0, 8, unit=11)
            sixnet_pwr_status = client.read_discrete_inputs(29, 3, unit=11)

            logger.info('%s: %s' % (device_data['alpha']['env']['ESI-1']['identifier'], device_data['alpha']['env']['ESI-1']['serial_number']))
            logger.info('%s: %s' % (device_data['alpha']['env']['IRRA-1']['identifier'], device_data['alpha']['env']['IRRA-1']['irradiance_1']))
            logger.info('%s: %s' % (device_data['alpha']['env']['cts-1']['identifier'], device_data['alpha']['env']['cts-1']['cell_temp_01']))

            logger.debug('Power Bits: %s' % (sixnet_pwr_status.bits))
            logger.info('OK output: %s' % (sixnet_pwr_status.getBit(0)))
            logger.info('Power Input #1: %s' % (sixnet_pwr_status.getBit(1)))
            logger.info('Power Input #2: %s' % (sixnet_pwr_status.getBit(2)))

            logger.debug('Link Status Bits: %s' % sixnet_link_status.bits)
            logger.info('Port 1 Link: %s' % (sixnet_link_status.getBit(0)))
            logger.info('Port 2 Link: %s' % (sixnet_link_status.getBit(1)))
            logger.info('Port 3 Link: %s' % (sixnet_link_status.getBit(2)))
            logger.info('Port 4 Link: %s' % (sixnet_link_status.getBit(3)))
            logger.info('Port 5 Link: %s' % (sixnet_link_status.getBit(4)))
            logger.info('Port 6 Link: %s' % (sixnet_link_status.getBit(5)))
            logger.info('Port 7 Link: %s' % (sixnet_link_status.getBit(6)))
            logger.info('Port 8 Link: %s' % (sixnet_link_status.getBit(7)))

            logger.info('%s data: %s' % (device_data['alpha']['mbs1']['MBS-1']['identifier'], device_data['alpha']['mbs1']['MBS-1']['value01']))
            logger.info('%s data: %s' % (device_data['alpha']['mbs1']['MBS-1']['identifier'], device_data['alpha']['mbs1']['MBS-1']['value02']))
            logger.info('%s data: %s' % (device_data['alpha']['mbs1']['MBS-1']['identifier'], device_data['alpha']['mbs1']['MBS-1']['value03']))
            logger.info('%s data: %s' % (device_data['alpha']['mbs1']['MBS-1']['identifier'], device_data['alpha']['mbs1']['MBS-1']['value04']))
            logger.info('%s data: %s' % (device_data['alpha']['mbs1']['MBS-1']['identifier'], device_data['alpha']['mbs1']['MBS-1']['value05']))
            logger.info('%s data: %s' % (device_data['alpha']['mbs1']['MBS-1']['identifier'], device_data['alpha']['mbs1']['MBS-1']['value06']))
            logger.info('%s data: %s' % (device_data['alpha']['mbs1']['MBS-1']['identifier'], device_data['alpha']['mbs1']['MBS-1']['value07']))
            logger.info('%s data: %s' % (device_data['alpha']['mbs1']['MBS-1']['identifier'], device_data['alpha']['mbs1']['MBS-1']['value08']))
            logger.info('%s data: %s' % (device_data['alpha']['mbs1']['MBS-1']['identifier'], device_data['alpha']['mbs1']['MBS-1']['value09']))
            logger.info('%s data: %s' % (device_data['alpha']['mbs1']['MBS-1']['identifier'], device_data['alpha']['mbs1']['MBS-1']['value10']))
            logger.info('%s' % (device_data['alpha']['mbs1']['MBS-1']['freezetime']))

            logger.info('%s data: %s' % (device_data['alpha']['mbs2']['MBS-2']['identifier'], device_data['alpha']['mbs2']['MBS-2']['value01']))
            logger.info('%s data: %s' % (device_data['alpha']['mbs2']['MBS-2']['identifier'], device_data['alpha']['mbs2']['MBS-2']['value02']))
            logger.info('%s data: %s' % (device_data['alpha']['mbs2']['MBS-2']['identifier'], device_data['alpha']['mbs2']['MBS-2']['value03']))
            logger.info('%s data: %s' % (device_data['alpha']['mbs2']['MBS-2']['identifier'], device_data['alpha']['mbs2']['MBS-2']['value04']))
            logger.info('%s data: %s' % (device_data['alpha']['mbs2']['MBS-2']['identifier'], device_data['alpha']['mbs2']['MBS-2']['value05']))
            logger.info('%s data: %s' % (device_data['alpha']['mbs2']['MBS-2']['identifier'], device_data['alpha']['mbs2']['MBS-2']['value06']))
            logger.info('%s data: %s' % (device_data['alpha']['mbs2']['MBS-2']['identifier'], device_data['alpha']['mbs2']['MBS-2']['value07']))
            logger.info('%s data: %s' % (device_data['alpha']['mbs2']['MBS-2']['identifier'], device_data['alpha']['mbs2']['MBS-2']['value08']))
            logger.info('%s data: %s' % (device_data['alpha']['mbs2']['MBS-2']['identifier'], device_data['alpha']['mbs2']['MBS-2']['value09']))
            logger.info('%s data: %s' % (device_data['alpha']['mbs2']['MBS-2']['identifier'], device_data['alpha']['mbs2']['MBS-2']['value10']))
            logger.info('%s' % (device_data['alpha']['mbs2']['MBS-2']['freezetime']))

            logger.debug('self.begintest value: %s' % (self.begintest))

            if self.begintest:
                if checkModbusData('MBS-1', device_data['alpha']['mbs1']['MBS-1']):
                    logger.info('MBS-1: Modbus Data Valid')
                else:
                    logger.info('MBS-1: Modbus Data Invalid')


                if checkModbusData('MBS-2', device_data['alpha']['mbs2']['MBS-2']):
                    logger.info('MBS-2: Modbus Data Valid')
                else:
                    logger.info('MBS-2: Modbus Data Invalid')

            time.sleep(5)

        client.close()

    def join(self, timeout=None):
        self.stoprequest.set()
        super(dataValidation, self).join(timeout)

    def begintest(self):
        self.begintest = True

    def stoptest(self):
        self.begintest = False
#---------------------------------------------------------------------------#
#---------------------------------------------------------------------------#


#---------------------------------------------------------------------------#
def getJsonData(url):

    resp = requests.get(url, timeout=3)
    logger.debug("%s" % (resp.text))

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
    # initialize input variables
    loglevel = ''
    log_filename = ''

    # start-up logger
    logger = logging.getLogger('etl_testing')

    # parse input arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'h-l:-f', ['--log=', '--file'])
    except getopt.GetoptError:
        print 'etl_netbook_testing.py --log=<loglevel>  --file=<filename.log>'
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print 'etl_netbook_testing.py --log=<loglevel> --file=<filename.log>'
            sys.exit()
        elif opt in ('-l', ' --log'):
            loglevel = arg
        elif opt in ('-f', ' --file'):
            log_filename = arg

    # assuming loglevel is bound to the string value obtained from the
    # command line argument. Convert to upper case to allow the user to
    # specify --log=DEBUG or --log=debug
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)

    # configure logger
    logger.setLevel(loglevel.upper())
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    handler_stream = logging.StreamHandler()
    handler_stream.setFormatter(formatter)
    handler_stream.setLevel(loglevel)
    logger.addHandler(handler_stream)

    if log_filename != '':
        handler_file = logging.FileHandler(log_filename)
        handler_file.setFormatter(formatter)
        handler_file.setLevel(level.DEBUG)
        logger.addHandler(handler_file)


    logger.info('running...')
    sys.stdout.write('running...\r\n')
    sys.stdout.write('enter "start" to start the test\r\n')
    sys.stdout.write('enter "stop" to stop the test\r\n')

    # start data thread
    validate_data_thread = dataValidation()
    validate_data_thread.start()

    # wait for user input
    while True:
        cmd = sys.stdin.readline()
        args = cmd.split(' ')

        if cmd.find('quit')==0:
            logger.info('bye-bye...')
            sys.stdout.write('bye-bye...\r\n')
            validate_data_thread.join()
            break
        elif cmd.find('start')==0:
            logger.info('Starting Test...')
            sys.stdout.write('Starting Test...\r\n')
            validate_data_thread.begintest
        elif cmd.find('stop')==0:
            logger.info('Stoping Test...')
            sys.stdout.write('Stoping Test...\r\n')
            validate_data_thread.stoptest
        elif cmd.find('help')==0:
            sys.stdout.write('enter "start" to start the test\r\n')
            sys.stdout.write('enter "stop" to stop the test\r\n')
        else:
            sys.stdout.write('unknown command %s\r\n' % (args[0]))
