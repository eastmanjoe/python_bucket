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
import requests
import json
# import subprocess

import socket

class csi_logger:
    """utilities to work with CSI CR1000 and CR800 dataloggers
    """
    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.udp_port = 6785
        self.username = "customer"
        self.password = "monitoring"

    def CSI_marco_polo(self):

        # F2 = 242 = o grave
        # 17 = 023 = End Transmission Block (ETB)
        # 01 = 001 = ^A (Start of Header [SOH])
        # E6 = 230 = ae ligature 1
        # C5 = 197 = A ring

        data = "f21701e6c5"
        message = ''.join(chr(int(data[i:i+2], 16)) for i in range(0, len(data), 2))

        # the public network interface
        BIND_UDP_IP = socket.gethostbyname(socket.gethostname())
        SENDTO_UDP_IP = "255.255.255.255"

        # port to send and receive packets on
        self.udp_port = 6785

        # create socket and set it up for UPD packets
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # set socket objects so
        #   - socket is non-blocking with a set timeout period in seconds
        #   - socket the socket level permissions to broadcast the UPD packet
        sock.settimeout(5.0)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        # bind the socket to the public interface
        sock.bind((BIND_UDP_IP, self.udp_port))

        # send CSI discovery broadcast message
        sock.sendto(message, (SENDTO_UDP_IP, self.udp_port))

        # print "UDP target IP:", SENDTO_UDP_IP
        print "UDP port:", self.udp_port


        try:
            while True:
                time.sleep(0.1)
                data, addr = sock.recvfrom(1024)
                print "received message", data, "from", addr

        except socket.timeout:
            print "socket timed out"

        except socket.error:
            print socket.error


    def set_parameter(self, variable_name, variable_value):
        r = requests.get('http://'+ self.ip_address + '?command=SetValueEx&uri=dl:public.' +
                variable_name + '&value=' + str(variable_value) + '&format=json', auth=(self.username, self.password))


    def get_parameter(self, variable_name):
        r = requests.get('http://'+ self.ip_address + '?command=DataQuery&uri=dl:public.' +
                variable_name + '&mode=most-recent&format=json', auth=(self.username, self.password))

        data = r.json()
        return data['data'][0]['vals'][0]

#---------------------------------------------------------------------------#
if __name__ == '__main__':

    # parser = argparse.ArgumentParser()
    # parser.add_argument('num', help='number of modbus slave ports and number of slaves per port (format is 1:1)')
    # parser.add_argument('ports', help='ports to use for the modbus slaves (format is COM1:COM2:COM3)')
    # parser.add_argument('-v','--verbose', help='enables/disable modbus-tk verbose mode', default='False')
    # parser.add_argument('-l','--level', help='defines the log level to be dispayed to the screen', default='info')
    # parser.add_argument('-f','--filename', help='defines the filename of the debugs log', default='')
    # args = parser.parse_args()

    csi1 = csi_logger("10.11.50.10")
    # csi1.CSI_marco_polo()

    #Testing srs pvel implementation
    srs_voltage_se1 = [0.64289750,0.63949850,0.63881920,0.63813960,0.63746040,0.63813950,0.63746030,0.64017710,0.63949780]
    srs_voltage_se2 = [0.07494464,0.07504404,0.07473980,0.07436641,0.07392697,0.07375891,0.07335327,0.07328543,0.07284599]
    srs_irrad_calc = [874.4999,875.6597,872.1097,867.7527,862.6251,860.6641,855.9308,855.1392,850.0116]
    srs_irrad_adj_calc = [880.9921,881.3920,877.6937,873.1905,867.9192,866.1095,861.2330,861.0343,855.7617]
    srs_temp_calc = [8.979917,10.861669,11.169285,11.461944,11.739671,11.332165,11.616329,10.116208,10.392824]
    srs_irrad = []
    srs_irrad_adj = []
    srs_temp = []

    for count in range(len(srs_voltage_se1)):
        print 'getting dataset #', count + 1, 'of', len(srs_voltage_se1)
        csi1.set_parameter("srs_voltage_se1", srs_voltage_se1[count])
        csi1.set_parameter("srs_voltage_se2", srs_voltage_se2[count])

        #wait for logger to make calculation
        time.sleep(4)

        #get calculations
        srs_irrad.append(csi1.get_parameter("srs_irrad"))
        srs_irrad_adj.append(csi1.get_parameter("srs_irrad_adj"))
        srs_temp.append(csi1.get_parameter("srs_temp"))

    print "Datalogger Calculated Irradiance Values", srs_irrad
    print "Excel      Calculated Irradiance Values", srs_irrad_calc

    print "Datalogger Calculated Irradiance Adjusted Values", srs_irrad_adj
    print "Excel      Calculated Irradiance Adjusted Values", srs_irrad_adj_calc

    print "Datalogger Calculated Temperature Values", srs_temp
    print "Excel      Calculated Temperature Values", srs_temp_calc