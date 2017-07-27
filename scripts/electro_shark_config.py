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

class ElectroShark:
    """Class to handle Electro Industries Shark 100"""

    def __init__(self, port, mb_address):
        if ":" in port:
            print "Modbus TCP"
            self.ip_addr = port.split(":")[0]
            self.port = int(port.split(":")[1])
            self.master = modbus_tcp.TcpMaster(host=self.ip_addr, port=int(self.port), timeout_in_sec=1.0)
        else:
            print "Modbus RTU"
            self.ip_addr = ""
            self.port = port
            self.master = modbus_rtu.RtuMaster(serial.Serial(port=self.port, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))

        self.mb_address = int(mb_address)
        self.master.set_timeout(1.0)
        self.master.set_verbose(True)
        self.name = ""
        self.serial_number = ""

        # configuration data
        self.ct_multiplier = 1
        self.ct_denominator = 5

        self.ct_numerator = 5
        self.pt_numerator = 120
        self.pt_denominator = 120

        self.pt_multiplier = 1
        self.hookup = "3 element wye"

        self.averaging_method = "block"
        self.averaging_interval = 15
        self.averaging_subinterval = 1

        self.power_scale = "kilo"
        self.num_energy_digits = 8
        self.energy_scale = "kilo"
        self.energy_decimal_places = 0

        self.num_phase_screens = "ABC"
        self.scroll = "yes"
        self.passwd_reset = "yes"
        self.passwd_config = "yes"
        self.power_direction = "load"
        self.pf_correction = "yes"

    def updateConfig(self):
        pass

    def printRegisters(self):
        pass

    def getName(self):

        string = ""
        self.name = ""

        regs = self.master.execute(self.mb_address, cst.READ_HOLDING_REGISTERS, 0, 8)

        for value in regs:
            hex_value = format(value, '04x')
            string += hex_value

        self.name = string[:len(string)].decode('hex')

        return self.name

    def getSerialNumber(self):

        string = ""
        self.serial_number = ""

        regs = self.master.execute(self.mb_address, cst.READ_HOLDING_REGISTERS, 8, 8)

        for value in regs:
            hex_value = format(value, '04x')
            string += hex_value

        self.serial_number = string[:len(string)].decode('hex')

        return self.serial_number

    def setConfig(self, password):
        meter_settings = [
            # CT multiplier & denominator
            # high byte is denominator (1 or 5, read-only), low byte is multiplier (1, 10, or 100
            # ddddddddmmmmmmmm
            0b0000000000000000,
            # CT numerator
            100,
            # PT numerator
            120,
            # PT denominator
            120,
            # PT multiplier & hookup
            # MMMMmmmmmmmm is PT multiplier (1,10, 100, 1000),
            # hhhh is hookup enumeration (0 = 3 element wye[9S], 1 = delta 2 CTs[5S], 3 = 2.5 element wye[6S])
            # mmmmmmmmMMMMhhhh
            0b0000000000000000,
            # Averaging Method
            # iiiiii = interval (5,15,30,60)
            # b = 0-block or 1-rolling
            # sss = # subintervals (1,2,3,4)
            # --iiiiiib----sss
            0b0000000000000000,
            # Power & Energy Format
            # pppp = power scale (0-unit, 3-kilo, 6-mega, 8-auto)
            # nn = number of energy digits (5-8 --> 0-3)
            # eee = energy scale (0-unit, 3-kilo, 6-mega)
            # ddd = energy digits after decimal point (0-6)
            # !! Energy registers should be reset after a format change. !!
            # pppp--nn-eee-ddd
            0b0000000000000000,
            # Operating Mode Screen Enables
            # eeeeeeee = op mode screen rows on(1) or off(0), rows top to bottom are bits low order to high order
            # 00000000eeeeeeee
            0b0000000000000000
            ]

        # g = enable alternate full scale bargraph current (1=on, 0=off)
        # nn = number of phases for voltage & current screens (3=ABC, 2=AB, 1=A, 0=ABC)
        # s = scroll (1=on, 0=off)
        # r = password for reset in use (1=on, 0=off)
        # p = password for configuration in use (1=on, 0=off)
        # w = pwr dir (0-view as load, 1-view as generator)
        # f = flip power factor sign (1=yes, 0=no)
        # 0b---g--nnsrp--wf-
        user_settings = 0b0000000000000000

        "initiate programmable settings update"
        self.master.execute(self.mb_address, cst.WRITE_MULTIPLE_REGISTERS, 22000, output_value=password)

        "write updated meter config"
        self.master.execute(self.mb_address, cst.WRITE_MULTIPLE_REGISTERS, 30000, output_value=meter_settings)
        self.master.execute(self.mb_address, cst.WRITE_MULTIPLE_REGISTERS, 30015, output_value=user_settings)

        "save settings to eeprom by reading the calculated checksum and writing it back"
        regs = self.master.execute(self.mb_address, cst.READ_HOLDING_REGISTERS, 22002, 1)
        self.master.execute(self.mb_address, cst.WRITE_SINGLE_REGISTER, 22003, output_value=regs)

        "terminate programmable settings update"
        self.master.execute(self.mb_address, cst.WRITE_MULTIPLE_REGISTERS, 22001, output_value=password)

    def getConfig(self):
        regs = self.master.execute(self.mb_address, cst.READ_HOLDING_REGISTERS, 30000, 7)
        self.ct_multiplier = 1
        self.ct_denominator = 5

        self.ct_numerator = 5
        self.pt_numerator = 120
        self.pt_denominator = 120

        self.pt_multiplier = 1
        self.hookup = "3 element wye"

        self.averaging_method = "block"
        self.averaging_interval = 15
        self.averaging_subinterval = 1

        self.power_scale = "kilo"
        self.num_energy_digits = 8
        self.energy_scale = "kilo"
        self.energy_decimal_places = 0

        regs = self.master.execute(self.mb_address, cst.READ_HOLDING_REGISTERS, 30015, 1)
        self.num_phase_screens = "ABC"
        self.scroll = "yes"
        self.passwd_reset = "yes"
        self.passwd_config = "yes"
        self.power_direction = "load"
        self.pf_correction = "yes"

    def close(self):
        self.master.close()




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

    if args.port.isdigit():
        port = args.ipaddress + ":" + args.port

    try:
        # meter_01 = ElectroShark(port, args.modbus_address)
        meter_01 = ElectroShark("10.11.50.53:502", args.modbus_address)
        meter_02 = ElectroShark("10.11.50.53:503", args.modbus_address)

        # logger.info("connected")

        # Serial Number
        print "Meter 1 Name is: " + meter_01.getName()
        print "Meter 1 Serial Number is: " + meter_01.getSerialNumber()
        print "Meter 2 Name is: " + meter_02.getName()
        print "Meter 2 Serial Number is: " + meter_02.getSerialNumber()

        # Instantaneous Data
        # regs = master.execute(int(args.modbus_address), cst.READ_HOLDING_REGISTERS, 1000, 30)
        # print regs

        meter_01.close()
        meter_02.close()

    except modbus_tk.modbus.ModbusError, e:
        logger.error("%s- Code=%d" % (e, e.get_exception_code()))