#!/usr/bin/env python

#Modbus Master using modbus-tk

#import sys
import serial
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu
import logging

logger = modbus_tk.utils.create_logger("console")

if __name__ == "__main__":
    try:
        #Connect to the slave
        master = modbus_rtu.RtuMaster(serial.Serial(port='/dev/ttyUSB1', baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))
        # master = modbus_rtu.RtuMaster(serial.Serial(port=sys.argv[1], baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))
        master.set_timeout(5.0)
        master.set_verbose(True)
        logger.info("connected")

        logger.info(master.execute(11, cst.READ_HOLDING_REGISTERS, 100, 10))
        # logger.info(master.execute(sys.argv[2], cst.READ_HOLDING_REGISTERS, 0, 10))

    except modbus_tk.modbus.ModbusError, e:
        logger.error("%s- Code=%d" % (e, e.get_exception_code()))