#!/usr/bin/env python

#Modbus Slave using modbus-tk

import sys

#add logging capability
import logging
import threading

import serial
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu

logger = modbus_tk.utils.create_logger(name="console", record_format="%(message)s")

if __name__ == "__main__":
    try:

        server = modbus_rtu.RtuServer(serial.Serial(port=6, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))
        server.set_verbose(True)

        #Connect to the slave
        logger.info("running...")
        logger.info("enter 'quit' for closing the server")

        server.start()

        slave_1 = server.add_slave(11)
        slave_1.add_block('0', cst.HOLDING_REGISTERS, 0, 100)
        slave_1.set_values('0', 0, [1,2,3])

        while True:
            cmd = sys.stdin.readline()
            args = cmd.split(' ')
            if cmd.find('quit')==0:
                sys.stdout.write('bye-bye\r\n')
                break
            elif args[0]=='add_slave':
                slave_id = int(args[1])
                server.add_slave(slave_id)
                sys.stdout.write('done: slave %d added\r\n' % (slave_id))
            elif args[0]=='add_block':
                slave_id = int(args[1])
                name = args[2]
                block_type = int(args[3])
                starting_address = int(args[4])
                length = int(args[5])
                slave = server.get_slave(slave_id)
                slave.add_block(name, block_type, starting_address, length)
                sys.stdout.write('done: block %s added\r\n' % (name))
            elif args[0]=='set_values':
                slave_id = int(args[1])
                name = args[2]
                address = int(args[3])
                values = []
                for v in args[4:]:
                    values.append(int(v))
                slave = server.get_slave(slave_id)
                slave.set_values(name, address, values)
                values = slave.get_values(name, address, len(values))
                sys.stdout.write('done: values written: %s\r\n' % (str(values)))
            elif args[0]=='get_values':
                slave_id = int(args[1])
                name = args[2]
                address = int(args[3])
                length = int(args[4])
                slave = server.get_slave(slave_id)
                values = slave.get_values(name, address, length)
                sys.stdout.write('done: values read: %s\r\n' % (str(values)))
            else:
                sys.stdout.write("unknown command %s\r\n" % (args[0]))

    finally:
        server.stop()