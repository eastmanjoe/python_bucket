#!/usr/bin/env python

#Modbus Master using modbus-tk

#import sys
import serial
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu
import modbus_tk.modbus_tcp as modbus_tcp
import logging
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--level', help='defines the log level to be dispayed to the screen', default='info')
    parser.add_argument('-f', '--filename', help='defines the filename of the debugs log', default='')
    parser.add_argument('-ip', '--ipaddress', help='defines the ip address to query', default='')
    parser.add_argument('-p', '--port', help='set port of modbus slave', default='/dev/ttyUSB0')
    parser.add_argument('-mb', '--modbus_address', help='set Modbus Address', default='1')
    args = parser.parse_args()

    # assuming args.level is bound to the string value obtained from the
    # command line argument. Convert to upper case to allow the user to
    # specify --log=DEBUG or --log=debug
    numeric_level = getattr(logging, args.level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % args.level)

    logger = modbus_tk.utils.create_logger(name="console", level=args.level.upper(), record_format="%(levelname)s: %(message)s")
    # logger = logging.getLogger('modbus_tk_tcp_slave')
    # # configure logger
    # # logger.setLevel(logging.DEBUG)
    # handler_stream_formatter = logging.Formatter('%(levelname)s: %(message)s')
    # handler_stream = logging.StreamHandler()
    # handler_stream.setFormatter(handler_stream_formatter)
    # handler_stream.setLevel(args.level.upper())
    # logger.addHandler(handler_stream)
    logger.debug('Log Level is: %s' % (args.level.upper()))

    # if args.filename != '':
    #     handler_file = logging.FileHandler('/home/jeastman/logs/' + args.filename)
    #     logger.debug('Log Filename is: %s' % (handler_file))
    #     handler_file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    #     handler_file.setFormatter(handler_file_formatter)
    #     # handler_file.setLevel(level.DEBUG)
    #     logger.addHandler(handler_file)
    logger.debug('Log Filename is: %s' % (args.filename))

    try:
        reg_hex = []


        if args.port.isdigit():
            # if args.ipaddress.split('.') :
                # raise ValueError('Invalid IP Address')
            #Connect to the TCP slave
            master = modbus_tcp.TcpMaster(host=args.ipaddress, port=args.port, timeout_in_sec=1.0)
        else:
            # connect to the RTU slave
            master = modbus_rtu.RtuMaster(serial.Serial(port=args.port, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))
            # master = modbus_rtu.RtuMaster(serial.Serial(port=sys.argv[1], baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))
        master.set_timeout(1.0)
        master.set_verbose(True)
        logger.info("connected")

        # Serial Number
        regs = master.execute(int(args.modbus_address), cst.READ_HOLDING_REGISTERS, 9, 8)
        print regs

        # Instantaneous Data
        regs = master.execute(int(args.modbus_address), cst.READ_HOLDING_REGISTERS, 1000, 30)
        print regs

        master.close()

    except modbus_tk.modbus.ModbusError, e:
        logger.error("%s- Code=%d" % (e, e.get_exception_code()))