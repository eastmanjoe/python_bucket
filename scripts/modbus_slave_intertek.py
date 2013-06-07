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
# # pymodbus
# from pymodbus.server.async import StartSerialServer
# from pymodbus.device import ModbusDeviceIdentification
# from pymodbus.datastore import ModbusSequentialDataBlock
# from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
# from pymodbus.transaction import ModbusRtuFramer, ModbusAsciiFramer
#---------------------------------------------------------------------------#

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
    # # pymodbus
    # store = ModbusSlaveContext(
    #     # di = ModbusSequentialDataBlock(0, [17]*100),
    #     # co = ModbusSequentialDataBlock(0, [17]*100),
    #     hr = ModbusSequentialDataBlock(mbAddr, [17]*100),
    #     ir = ModbusSequentialDataBlock(mbAddr, [17]*100))
    # context = ModbusServerContext(slaves=store, single=True)

    # #---------------------------------------------------------------------------#
    # # initialize the server information
    # #---------------------------------------------------------------------------#
    # # If you don't set this or any fields, they are defaulted to empty strings.
    # #---------------------------------------------------------------------------#
    # identity = ModbusDeviceIdentification()
    # identity.VendorName  = 'Draker'
    # identity.ProductCode = 'PM'
    # identity.VendorUrl   = ''
    # identity.ProductName = 'Pymodbus Server'
    # identity.ModelName   = 'Pymodbus Server'
    # identity.MajorMinorRevision = '1.0'

    # #---------------------------------------------------------------------------#
    # # run the server you want
    # #---------------------------------------------------------------------------#
    # # StartTcpServer(context, identity=identity, address=("localhost", 5020))
    # #StartUdpServer(context, identity=identity, address=("localhost", 502))
    # StartSerialServer(context, identity=identity, port=comPort, framer=ModbusRtuFramer)
    # StartSerialServer(context, identity=identity, port=comPort, framer=ModbusRtuFramer)
    # #StartSerialServer(context, identity=identity, port='/dev/pts/3', framer=ModbusAsciiFramer)
    #---------------------------------------------------------------------------#

    #---------------------------------------------------------------------------#
    # modbus-tk
    try:
        server_USB0 = modbus_rtu.RtuServer(serial.Serial(port="/dev/ttyUSB0", baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))
        server_USB1 = modbus_rtu.RtuServer(serial.Serial(port="/dev/ttyUSB1", baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))

        #Connect to the slave
        logger.info("running...")
        # logger.info("enter 'quit' for closing the server")

        # Start Modbus Slave servers
        server_USB0.start()
        slave_USB0 = server_USB0.add_slave(11)

        server_USB1.start()
        slave_USB1 = server_USB1.add_slave(11)

        # Add data to Modbus Slave servers
        slave_USB0.add_block("0", cst.HOLDING_REGISTERS, 100, 10)
        slave_USB0.set_values("0", 100, [10, 11, 12, 13, 14, 15, 16, 17, 18, 19])

        slave_USB1.add_block("0", cst.HOLDING_REGISTERS, 100, 10)
        slave_USB1.set_values("0", 100, [20, 21, 22, 23, 24, 25, 26, 27, 28, 29])

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
    #---------------------------------------------------------------------------#
#---------------------------------------------------------------------------#


#---------------------------------------------------------------------------#
if __name__ == "__main__":

    logger = modbus_tk.utils.create_logger(name="console", record_format="%(message)s")

    startModbusSlave()
