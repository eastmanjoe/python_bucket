#!/usr/bin/env python
#
#
#
'''
This program searches for all available CSI dataloggers and reports the units found.
'''

#---------------------------------------------------------------------------#
# import os
import sys
import time
# import argparse
# import logging
# import requests
# import subprocess

import socket

def CSI_marco_polo(message):
    # the public network interface
    BIND_UDP_IP = socket.gethostbyname(socket.gethostname())
    SENDTO_UDP_IP = "255.255.255.255"

    # port to send and receive packets on
    UDP_PORT = 6785

    # create socket and set it up for UPD packets
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # set socket objects so
    #   - socket is non-blocking with a set timeout period in seconds
    #   - socket the socket level permissions to broadcast the UPD packet
    sock.settimeout(1.0)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # bind the socket to the public interface
    sock.bind((BIND_UDP_IP, UDP_PORT))

    # send CSI discovery broadcast message
    sock.sendto(message, (SENDTO_UDP_IP, UDP_PORT))

    # print "UDP target IP:", SENDTO_UDP_IP
    print "UDP port:", UDP_PORT

    while True:
        time.sleep(0.1)

        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        print "received message:", data



#---------------------------------------------------------------------------#
if __name__ == '__main__':

    # parser = argparse.ArgumentParser()
    # parser.add_argument('num', help='number of modbus slave ports and number of slaves per port (format is 1:1)')
    # parser.add_argument('ports', help='ports to use for the modbus slaves (format is COM1:COM2:COM3)')
    # parser.add_argument('-v','--verbose', help='enables/disable modbus-tk verbose mode', default='False')
    # parser.add_argument('-l','--level', help='defines the log level to be dispayed to the screen', default='info')
    # parser.add_argument('-f','--filename', help='defines the filename of the debugs log', default='')
    # args = parser.parse_args()

    data = "f21701e6c5"
    message = ''.join(chr(int(data[i:i+2], 16)) for i in range(0, len(data), 2))

    CSI_marco_polo(message)