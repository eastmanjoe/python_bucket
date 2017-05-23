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

    # modbus-tk
    logger.info('Number of Modbus Slave Ports is %d' % num_modbus_ports)
    logger.info('Number of Modbus Slaves per Port is %d' % num_slaves_per_port)

    for x in range(0, num_modbus_ports):
        logger.info('COM Port #%d is: %s' % (x + 1, com_ports[x]))

    try:
        for modbus_ports in range(0, num_modbus_ports):
            exec (
                'server_%d = modbus_rtu.RtuServer('
                'serial.Serial(port="%s", baudrate=9600, bytesize=8, parity="N", stopbits=1, xonxoff=0)'
                ')' %
                (
                    modbus_ports, str(com_ports[modbus_ports])
                )
            )
            exec ('server_%d.start()' % modbus_ports)
            exec ("server_%d.set_verbose(%s)" % (modbus_ports, verbose_enabled))

            if verbose_enabled:
                logger.info('Modbus-tk verbose enabled')
                # exec("server_%d.set_verbose(True)" % (modbus_ports))
            else:
                logger.info('Modbus-tk verbose disabled')

            for modbus_slaves in range(0, num_slaves_per_port):
                exec ("server_%d_slave_%d = server_%d.add_slave(11 + %d)" %
                      (
                          modbus_ports, modbus_slaves, modbus_ports, modbus_slaves
                      )
                      )
                exec ("server_%d_slave_%d.add_block('0', modbus_defines.HOLDING_REGISTERS, 100, 10)" %
                      (
                          modbus_ports, modbus_slaves
                      )
                      )

                holding_register_values = range(10 + (10 * modbus_slaves), 20 + (10 * modbus_slaves))

                exec ("server_%d_slave_%d.set_values('0', 100, [%s])" %
                      (modbus_ports, modbus_slaves, ','.join(map(str, holding_register_values)))
                      )

        # server_0.set_verbose(True)
        # server_1.set_verbose(True)

        # Connect to the slave
        logger.info('All slave(s) running...')
        logger.info('enter "quit" to close the server(s)')

        while True:
            cmd = sys.stdin.readline()
            cmd_args = cmd.split(' ')

            if (cmd.find('quit') == 0) or (cmd.find('q') == 0):
                sys.stdout.write('bye-bye\n')
                break

    finally:
        for modbus_ports in range(0, num_modbus_ports):
            exec ('server_%d.stop()' % modbus_ports)


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
    # logger = logging.getLogger('modbus_log')

    # setupLogger('debug', 'modbus_log.log')
    setup_logger(args.level, args.filename)

    logger.info('Script started on: %s' % time.asctime(time.localtime(time.time())))

    # logger.info('Modbus-tk verbose set to %s' % args.verbose)
    start_modbus_slave(args.num.split(':'), args.ports.split(':'), args.verbose)
