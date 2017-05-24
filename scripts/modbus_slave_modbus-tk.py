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

import time
import sys
import argparse
import serial

# ---------------------------------------------------------------------------#
# modbus-tk
import modbus_tk
import modbus_tk.defines as modbus_defines
import modbus_tk.modbus_rtu as modbus_rtu
import modbus_tk.modbus_tcp as modbus_tcp
# ---------------------------------------------------------------------------#

# ---------------------------------------------------------------------------#
# logging
import logging


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
        handler_file = logging.FileHandler('c:\\temp\\' + logfilename)
        # handler_file = logging.FileHandler('/home/jeastman/logs/' + logfilename)
        handler_file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        handler_file.setFormatter(handler_file_formatter)
        handler_file.setLevel(loglevel.upper())
        logger.addHandler(handler_file)

    logger.info('Log Level is: %s' % loglevel)
    logger.info('Log Filename is: %s' % logfilename)


# ---------------------------------------------------------------------------#


# ---------------------------------------------------------------------------#
def start_modbus_slave(modbus_ports_and_slaves_per_port, com_ports, verbose_enabled):
    num_modbus_ports = int(modbus_ports_and_slaves_per_port[0])
    num_slaves_per_port = int(modbus_ports_and_slaves_per_port[1])

    mb_server = []
    mb_server_slave = []

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
                holding_register_values = list(range(10 + (10 * modbus_slaves), 20 + (10 * modbus_slaves)))

                mb_server_slave.append(mb_server[modbus_ports].add_slave(1 + modbus_slaves))
                mb_server_slave[modbus_slaves].add_block('0', modbus_defines.HOLDING_REGISTERS, 1, 40000)
                # mb_server_slave[modbus_slaves].set_values('0', 100, ','.join(map(str, holding_register_values)))
                mb_server_slave[modbus_slaves].set_values('0', 100, ','.join([str(hreg) for hreg in holding_register_values]))

        # Connect to the slave
        logger.info('All slave(s) running...')
        logger.info('enter "quit" to close the server(s)')

        while True:
            cmd = sys.stdin.readline()
            cmd_args = cmd.split(' ')

            if (cmd.find('quit') == 0) or (cmd.find('q') == 0):
                # sys.stdout.write('bye-bye\n')
                logger.info('bye-bye')
                break

    finally:
        for modbus_ports in range(0, num_modbus_ports):
            mb_server[modbus_ports].stop()


# ---------------------------------------------------------------------------#


# ---------------------------------------------------------------------------#
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('num', help='number of modbus slave ports and number of slaves per port (format is 1:1)')
    parser.add_argument('ports', help='ports to use for the modbus slaves (format is COM1:COM2:COM3)')
    parser.add_argument('-v', '--verbose', help='enables/disable modbus-tk verbose mode', action='store_true')
    parser.add_argument('-l', '--level', help='defines the log level to be dispayed to the screen', default='info')
    parser.add_argument('-f', '--filename', help='defines the filename of the debugs log', default='')
    args = parser.parse_args()

    if args.verbose:
        args.level = 'debug'

    # start-up logger
    logger = modbus_tk.utils.create_logger(name='console', level=args.level.upper(),
                                           record_format="%(levelname)s: %(message)s")

    setup_logger(args.level, args.filename)

    logger.info('Script started on: {}'.format(time.asctime(time.localtime(time.time()))))

    # logger.info('Modbus-tk verbose set to %s' % args.verbose)
    start_modbus_slave(args.num.split(':'), args.ports.split(':'), args.verbose)
