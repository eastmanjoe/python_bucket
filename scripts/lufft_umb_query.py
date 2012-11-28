#Lufft Set Into Programming Mode

import sys
import serial
import logging
import time
import array

#Common ASCII Codes
SOH = 0x01
STX = 0x02
ETX = 0x03
EOT = 0x04
LF = 0x0A
CR = 0x0D

#Calculate CRC-CCITT
def calc_crc_ccitt(crc_buff, data_value):
    for x in range(0,8):
        if (crc_buff & 0x0001) ^ (data_value & 0x01):
            xor_mask = 0x8408
        else:
            xor_mask = 0x0000

        #shift crc buffer
        crc_buff = crc_buff >> 1

        #XOR in the x16 value
        crc_buff ^= xor_mask

        #shift data_value for next iteration
        data_value = data_value >> 1
        pass
    pass

    return crc_buff

#def generate_umb_binary(command, command_ver,):


if __name__ == "__main__":
    device_address = int(sys.argv[1])
    #umb_command = sys.argv[2]
    #umb_command_ver = float(sys.argv[3])

    #print device_address
    #print umb_command
    #print umb_command_ver

    # Connect to the slave
    serialPort = serial.Serial(port=4, baudrate=19200, bytesize=8, parity='N', stopbits=1, xonxoff=0, timeout=0.5)

    command = []

    #UMB Binary Request
    command.append(SOH)
    command.append(0x10)
    command.append(int(device_address))
    command.append(0x70)
    command.append(0x01)
    command.append(0xF0)
    command.append(0x0F)
    command.append(STX)

    #request status
    # command.append(chr(0x26))
    # command.append(chr(0x10))

    #protocol change
    # command.append(chr(0x2B))
    # command.append(chr(0x10))
    # command.append(chr(0x10))

    #request measurements (100, 200, 300, 400, 500, 110)
    command.append(0x2F)
    command.append(0x10)

    command.append(0x06)
    command.append(0x64)
    command.append(0x00)
    command.append(0xC8)
    command.append(0x00)
    command.append(0x2C)
    command.append(0x01)
    command.append(0x90)
    command.append(0x01)
    command.append(0xF4)
    command.append(0x01)
    command.append(0x6E)
    command.append(0x00)

    #end of data transmission
    command.append(ETX)

    #initialize crc start value (0xFFFF)
    crc = 0xFFFF

    #calculate crc-ccitt for command
    for x in range(len(command)):
        crc = calc_crc_ccitt(crc, command[x])
        pass

    command.append(crc & 0x00FF)
    command.append(crc >> 8)
    command.append(EOT)

    command_sent = array.array('B', command).tostring()

    umb_response = 0

    for x in range(30):
        serialPort.write(command_sent)
        umb_response = serialPort.read(65)
        print umb_response
        time.sleep(1)
        pass

    serialPort.close()