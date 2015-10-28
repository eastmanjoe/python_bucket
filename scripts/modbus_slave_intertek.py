#!/usr/bin/env python

'''
Intertek Certification Program run on Netbook.
This program is used to provide the Pass/Fail indicator to the EMC testing team.
This program also starts two modbus slaves for the DAQ code to query.
'''

#import packages
import os
import sys
import serial
import serial.tools.list_ports

#---------------------------------------------------------------------------#
# modbus-tk
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu
import threading
#---------------------------------------------------------------------------#


#---------------------------------------------------------------------------#
# logging
import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)
#---------------------------------------------------------------------------#


#---------------------------------------------------------------------------#
# def determineComPort(devicename):
#     availableportlist = list(serial.tools.list_ports.comports())

#     data_rows = len(availableportlist)
#     data_columns = len(availableportlist.split(','))
#     # data_columns = 3

#     print "Port List has %d columns and %d rows" % (data_columns, data_rows)
#     print availableportlist

#     # return portvalue
#---------------------------------------------------------------------------#


#---------------------------------------------------------------------------#
def startModbusSlave():
    #---------------------------------------------------------------------------#
    # modbus-tk
    try:
        # server_USB0 = modbus_rtu.RtuServer(serial.Serial(port="/dev/ttyUSB0", baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))
        # server_USB1 = modbus_rtu.RtuServer(serial.Serial(port="/dev/ttyUSB1", baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))
        server_USB0 = modbus_rtu.RtuServer(serial.Serial(port="COM5", baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))
        server_USB1 = modbus_rtu.RtuServer(serial.Serial(port="COM6", baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))
        # server_USB2 = modbus_rtu.RtuServer(serial.Serial(port="COM19", baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))

        #Connect to the slave
        logger.info("running...")
        # logger.info("enter 'quit' for closing the server")

        # Start Modbus Slave servers
        server_USB0.start()
        server_USB1.start()
        # server_USB2.start()

        server_USB0.set_verbose(True)
        server_USB1.set_verbose(True)
        # server_USB2.set_verbose(True)

        for mb_addr in range(11, 44):
            slave_USB0 = server_USB0.add_slave(mb_addr)
            slave_USB0.add_block("0", cst.HOLDING_REGISTERS, 100, 10)
            slave_USB0.set_values("0", 100, [10, 11, 12, 13, 14, 15, 16, 17, 18, 19])

            slave_USB1 = server_USB1.add_slave(mb_addr)
            slave_USB1.add_block("0", cst.HOLDING_REGISTERS, 100, 10)
            slave_USB1.set_values("0", 100, [20, 21, 22, 23, 24, 25, 26, 27, 28, 29])

            # slave_USB2 = server_USB2.add_slave(mb_addr)
            # slave_USB2.add_block("0", cst.HOLDING_REGISTERS, 100, 10)
            # slave_USB2.set_values("0", 100, [20, 21, 22, 23, 24, 25, 26, 27, 28, 29])

        while True:
            cmd = sys.stdin.readline()
            args = cmd.split(" ")
            if cmd.find("quit")==0:
                sys.stdout.write("bye-bye\r\n")
                break
            else:
                sys.stdout.write("unknown command %s\r\n" % (args[0]))
    finally:
        server_USB0.stop()
        server_USB1.stop()
        # server_USB2.stop()
    #---------------------------------------------------------------------------#
#---------------------------------------------------------------------------#


#---------------------------------------------------------------------------#
if __name__ == "__main__":

    logger = modbus_tk.utils.create_logger(name="console", record_format="%(message)s")

    startModbusSlave()
