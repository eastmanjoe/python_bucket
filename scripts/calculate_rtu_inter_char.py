#!/usr/bin/env python

# Modbus Slave using modbus-tk
# This is the function that calculates the inter character delay
# according to the Modbus specification.

# This function is located in the utils.py file of the modbus_tk
# library.  The call to the function in the modbus_rtu.py file
# needs to be updated.  The function is called on line 84, 147

import sys

#add logging capability
import logging
import threading

import serial

def calculate_rtu_inter_char(baudrate, bytesize, parity, stopbits):
    """calculates the interchar delay from the baudrate"""
    if baudrate <= 19200:
        if parity == "N":
            paritybits = 0.00
        elif parity == "O":
            paritybits = 1.00
        elif parity == "E":
            paritybits = 1.00
        
        return (bytesize + paritybits + stopbits) / baudrate
    else:
        return 0.000750

if __name__ == "__main__":
    serial_USB0 = serial.Serial(port="/dev/ttyUSB0", baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0)
    print "%f" % calculate_rtu_inter_char(serial_USB0.baudrate, serial_USB0.bytesize, serial_USB0.parity, serial_USB0.stopbits)
    
    serial_USB0 = serial.Serial(port="/dev/ttyUSB0", baudrate=9600, bytesize=8, parity='E', stopbits=1, xonxoff=0)
    print "%f" % calculate_rtu_inter_char(serial_USB0.baudrate, serial_USB0.bytesize, serial_USB0.parity, serial_USB0.stopbits)
    
    serial_USB0 = serial.Serial(port="/dev/ttyUSB0", baudrate=38400, bytesize=8, parity='E', stopbits=1, xonxoff=0)
    print "%f" % calculate_rtu_inter_char(serial_USB0.baudrate, serial_USB0.bytesize, serial_USB0.parity, serial_USB0.stopbits)
