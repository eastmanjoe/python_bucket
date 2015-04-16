#!/usr/bin/env python
#
#
#
'''
Perform the power cycling tests on the DBS4 image

Example:
    python sixnet_io.py 10.11.50.60 502 1 -f ferrit_bead_test_20150324.txt
'''

import logging
import argparse
import time
import sys
import signal
from platform import system
import random

import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_tcp as modbus_tcp
import modbus_tk.modbus_rtu as modbus_rtu
#---------------------------------------------------------------------------#
def signal_handler(signal, frame):
    print ('You pressed Ctrl+C')
    response = controller.set_multiple_digital_outputs(1, 2, ['OFF', 'OFF'])
    controller.disconnect()
    logger.info('Test Stoped on: %s' % time.asctime(time.localtime(time.time())))
    sys.exit(0)


#---------------------------------------------------------------------------#
def setupLogger(loglevel, logfilename):
    # assuming loglevel is bound to the string value obtained from the
    # command line argument. Convert to upper case to allow the user to
    # specify --log=DEBUG or --log=debug
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)

    # configure logger
    # logger.setLevel(loglevel.upper())
    # handler_stream_formatter = logging.Formatter('%(levelname)s: %(message)s')
    # handler_stream = logging.StreamHandler()
    # handler_stream.setFormatter(handler_stream_formatter)
    # handler_stream.setLevel(loglevel.upper())
    # logger.addHandler(handler_stream)

    if logfilename != '':
        if system() == 'Windows':
            handler_file = logging.FileHandler('c:\\temp\\' + logfilename)
        elif system() == 'Linux':
            handler_file = logging.FileHandler('/tmp/' + logfilename)

        handler_file_formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s')
        handler_file.setFormatter(handler_file_formatter)
        handler_file.setLevel(loglevel.upper())
        logger.addHandler(handler_file)

    logger.info('Log Level is: %s' % (loglevel))
    logger.info('Log Filename is: %s' % (logfilename))

#---------------------------------------------------------------------------#
class SixnetIo:
    '''

    '''
    def __init__(self, ip_addr, mb_port, mb_addr, verbose):
        self.ip_addr = ip_addr

        if mb_port.isdigit():
            self.mb_port = int(mb_port)
            self.mb_bus = 'TCP'
        else:
            self.mb_port = mb_port
            self.mb_bus = 'RTU'

        self.mb_addr = mb_addr
        self.verbose = verbose

        self.fw_version = ''

        try:
            if self.mb_bus == 'TCP':
                self.master = modbus_tcp.TcpMaster(
                    host=self.ip_addr, port=self.mb_port, timeout_in_sec=1.0)
            elif self.mb_bus == 'RTU':
                self.master = modbus_rtu.RtuMaster(
                    host=self.ip_addr, port=self.mb_port, timeout_in_sec=1.0)

            self.master.set_timeout(1.0)
            self.master.set_verbose(verbose)

        except modbus_tk.modbus.ModbusError, e:
            logger.error("%s- Code=%d" % (e, e.get_exception_code()))


    def do_state_conv(self, do_state):
        if do_state == 'ON':
            return 1
        else:
            return 0


    def set_digital_output(self, do_num, do_state):

        # the register for the digital output is 1 less than the digital output number
        regs = self.master.execute(self.mb_addr,
            cst.WRITE_SINGLE_COIL, do_num - 1, 1, self.do_state_conv(do_state))

        return regs


    def set_multiple_digital_outputs(self, do_num_start, do_total, do_state):
        state = []

        if len(do_state) == 1:
            for x in xrange(do_total):
                    state.append(self.do_state_conv(x))
        else:
            for x in do_state:
                state.append(self.do_state_conv(x))

        tuple(state)

        regs = self.master.execute(self.mb_addr,
            cst.WRITE_MULTIPLE_COILS, do_num_start - 1, do_total, state)

        return regs

    def get_digital_input(self, di_num):
        regs = self.master.execute(self.mb_addr, cst.READ_COILS, di_num - 1, 1)

        return regs

    def get_multiple_digital_inputs(self, di_num_start, di_total):
        regs = self.master.execute(self.mb_addr,
            cst.READ_COILS, di_num_start - 1, di_total)

        return regs

    def get_status(self):
        self.master.execute(self.mb_addr, cst.READ_HOLDING_REGISTERS, 0x2010, 5)
        self.master.execute(self.mb_addr, cst.READ_HOLDING_REGISTERS, 0x2030, 5)

    def disconnect(self):
        self.master.close()
#---------------------------------------------------------------------------#


#---------------------------------------------------------------------------#
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ipaddress',
        help='defines the ip address to query', default='')
    parser.add_argument('port', help='set port of modbus slave', default=502)
    parser.add_argument('modbus_address', type=int,
        help='set Modbus Address', default='1')
    parser.add_argument('-l', '--level', type=str,
        help='defines the log level to be dispayed to the screen', default='info')
    parser.add_argument('-f', '--filename', type=str,
        help='defines the filename of the debugs log', default='')
    parser.add_argument('-v', '--verbose', type=bool,
        help='enables/disable modbus-tk verbose mode', default='False')
    args = parser.parse_args()

    # start-up logger
    logger = modbus_tk.utils.create_logger(name='console',
        level=args.level.upper() ,record_format="%(levelname)s: %(message)s")

    setupLogger(args.level, args.filename)


    #start instance of sixnet i/o class
    controller = SixnetIo(args.ipaddress, args.port, args.modbus_address, args.verbose)

    #register Ctrl-C signal handler
    signal.signal(signal.SIGINT, signal_handler)

    logger.info('Test Started on: %s' % time.asctime(time.localtime(time.time())))

    #initialize cycle counter to zero
    count = 0

    while True:

        count += 1
        logger.info('Cycle # is: %d' % count)

        # DO1 = DUT#1
        # DO2 = DUT#2


        #----------------------------------------------------------------------#
        # Simulating disconnecting the connector
        response = controller.set_multiple_digital_outputs(1, 2, ['ON', 'ON'])

        delay = random.randint(5, 300)
        logger.info('Off Delay is: %d' % delay)
        time.sleep(delay)


        response = controller.set_multiple_digital_outputs(1, 2, ['OFF', 'OFF'])

        delay = random.randint(5, 300)
        logger.info('On Delay is: %d' % delay)
        time.sleep(delay)
        #----------------------------------------------------------------------#
