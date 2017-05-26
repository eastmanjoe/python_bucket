#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
"""
This program starts two modbus slaves for the DAQ code to query.

#  requirement 1: serial library must be installed in the system
#  requirement 2: modbus-tk  can be downloaded from the link below,
#  http://code.google.com/p/modbus-tk/downloads/detail?name=modbus-tk-0.4.2.zip
#  once downloaded it must be installed
#
#  This python script expects 3 STRING arguments passed-in as inputs:
#  1) Number of modbuses in use    e.g     1  or  2
#  2) COM PORT 'A'    e.g.    COM24   as recognized by the system
#  3) COM PORT 'B'    e.g.    COM21   as recognized by the system
#
#  How to call the script from the command line example,
#  C:\python> modbus_slave_DAS4_prod_test.py 1 COM24 COM21 True or
#  C:\python> modbus_slave_DAS4_prod_test.py 2 COM24 COM21 False or

"""

import sys
import time
import argparse
import serial
from serial.tools import list_ports
import os
import re
import logging
import contextlib
from io import StringIO

# chose an implementation, depending on os
#~ if sys.platform == 'cli':
#~ else:
if os.name == 'nt':  # sys.platform == 'win32':
    from serial.tools.list_ports_windows import comports
elif os.name == 'posix':
    from serial.tools.list_ports_posix import comports
#~ elif os.name == 'java':
else:
    raise ImportError("Sorry: no implementation for your platform ('{}') available".format(os.name))


# ---------------------------------------------------------------------------#
# modbus-tk
import modbus_tk
import modbus_tk.defines as modbus_defines
import modbus_tk.modbus_rtu as modbus_rtu
import modbus_tk.modbus_tcp as modbus_tcp


# ---------------------------------------------------------------------------#
def setup_logger(loglevel, logfilename):
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
        handler_file = logging.FileHandler(logfilename)
        # handler_file = logging.FileHandler('/home/jeastman/logs/' + logfilename)
        handler_file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        handler_file.setFormatter(handler_file_formatter)
        handler_file.setLevel(loglevel.upper())
        logger.addHandler(handler_file)

    logger.info('Log Level is: %s' % loglevel)
    logger.info('Log Filename is: %s' % logfilename)


# ---------------------------------------------------------------------------#
def show_ports(args):
    logger.info('Searching for available ports')
    logger.info('Available ports are:')

    ports = sorted(comports())
    avail_ports = []

    for n, (port, desc, hwid) in enumerate(ports, 1):
        logger.info('\t{}'.format(port))
        avail_ports.append(port)

    logger.debug('Finished searching for available ports')
    return avail_ports

# ---------------------------------------------------------------------------#
def run(args):
    # logger.info('Modbus-tk verbose set to %s' % args.verbose)
    start_modbus_slave(args.num.split(':'), args.ports.split(':'), args.verbose)


# ---------------------------------------------------------------------------#
def start_modbus_slave(modbus_ports_and_slaves_per_port, com_ports, verbose_enabled):
    num_modbus_ports = int(modbus_ports_and_slaves_per_port[0])
    num_slaves_per_port = int(modbus_ports_and_slaves_per_port[1])

    number_of_registers = 41000

    holding_register_values = [
        hreg for hreg in range(1, number_of_registers + 1)
    ]

    mb_server = []

    # modbus-tk
    logger.info('Number of Modbus Slave Ports is %d' % num_modbus_ports)
    logger.info('Number of Modbus Slaves per Port is %d' % num_slaves_per_port)

    try:
        for modbus_ports in range(0, num_modbus_ports):
            logger.info('COM Port #%d is: %s' % (modbus_ports + 1, com_ports[modbus_ports]))

            mb_server.append(
                modbus_rtu.RtuServer(
                    serial.Serial(
                        port=str(com_ports[modbus_ports]),
                        baudrate=9600,
                        bytesize=8,
                        parity="N",
                        stopbits=1,
                        xonxoff=False
                    )
                )
            )

            mb_server[modbus_ports].start()
            mb_server[modbus_ports].set_verbose(verbose_enabled)

            if verbose_enabled:
                logger.info('Modbus-tk verbose enabled')
                mb_server[modbus_ports].set_verbose(True)
            else:
                logger.info('Modbus-tk verbose disabled')


            for modbus_slaves in range(0, num_slaves_per_port):
                logger.debug('Adding modbus slave #{} to {} port'.format(1 + modbus_slaves, com_ports[modbus_ports]))
                mb_server[modbus_ports].add_slave(1 + modbus_slaves)

                mb_slave = mb_server[modbus_ports].get_slave(1 + modbus_slaves)
                mb_slave.add_block('0', modbus_defines.HOLDING_REGISTERS, 1, number_of_registers)
                mb_slave.set_values('0', 1, holding_register_values)
                mb_slave.add_block('1', modbus_defines.ANALOG_INPUTS, 1, number_of_registers)
                mb_slave.set_values('1', 1, holding_register_values)

                logger.debug(
                    'Added values {} to {} to modbus slave #{}'.format(
                        mb_slave.get_values('0', 1, 1)[0],
                        mb_slave.get_values('0', holding_register_values, 1)[0],
                        1 + modbus_slaves
                    )
                )

        # Connect to the slave
        logger.info('All slave(s) running...')
        logger.info('enter "quit" or "exit" to close the server(s)')

        while True:
            cmd = sys.stdin.readline()

            if (cmd.find('quit') == 0) or (cmd.find('q') == 0) or (cmd.find('exit') == 0):
                logger.info('bye-bye')
                break

    finally:
        for modbus_ports in range(0, num_modbus_ports):
            mb_server[modbus_ports].stop()


# ---------------------------------------------------------------------------#


# ---------------------------------------------------------------------------#
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    cli_parser = parser.add_subparsers()
    parser.add_argument('-v', '--verbose', help='enables/disable modbus-tk verbose mode', action='store_true')
    parser.add_argument('-l', '--level', help='defines the log level to be dispayed to the screen', default='info')
    parser.add_argument('-f', '--filename', help='defines the filename of the debugs log', default='')

    list_ports_parser = cli_parser.add_parser('show_ports', help='list available ports')
    list_ports_parser.set_defaults(func=show_ports)

    mb_slave_parser = cli_parser.add_parser('slave', help='run the modbus slave')
    mb_slave_parser.set_defaults(func=run)
    mb_slave_parser.add_argument('num', help='number of modbus slave ports and number of slaves per port (format is 1:1)')
    mb_slave_parser.add_argument('ports', help='ports to use for the modbus slaves (format is COM1:COM2:COM3)')

    args = parser.parse_args()

    if args.verbose:
        args.level = 'debug'

    # start-up logger
    logger = modbus_tk.utils.create_logger(name='console', level=args.level.upper(),
                                           record_format="%(message)s")

    setup_logger(args.level, args.filename)

    logger.info('Script started on: {}'.format(time.asctime(time.localtime(time.time()))))

    args.func(args)


