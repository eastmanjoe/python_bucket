#!/usr/bin/env python

'''
Run Cora commands
'''

#---------------------------------------------------------------------------#
#import packages
import os
import sys
import argparse
import time
import logging
import threading
from subprocess import Popen, PIPE, STDOUT
import json

#---------------------------------------------------------------------------#
class Cora(threading.Thread):
    '''
    a thread that launches the cora_cmd service and
    connect to the LoggerNet server specifiec
    '''

    def __init__(self, server_ip, username, password):
        super(Cora, self).__init__()
        self.name = 'Cora'
        self.threadID = 2
        self.stoprequest = threading.Event()
        self.server_ip = server_ip
        self.username = username
        self.password = password


    def run(self):
        logger.info('starting cora')
        self.cora = "cora"
        self.cora += " --input={connect " + server_ip
        if username != "":
            self.cora += " --username=" + self.username
            self.cora += " --password=" + self.password

        cora += ";}"

        self.terminal = Popen(self.cora, stdout=PIPE, stdin=PIPE, stderr=STDOUT)

    def join(self):
        self.stoprequest.set()
        super(dataValidation, self).join(timeout)

        logger.info('stopping cora')

    def list_stations(self):

        cmd += "list-stations;"
        cmd += "}"

    def network_map_xml(self):

        cmd += "make-xml-network-map --format=xml" + ";"
        cmd += "}"

    def get_data_fill_days(self, station_name):
        cmd += "get-value " + station_name + "Status.DataFillDays(1);"
        cmd += "}"

    def list_devices(self):
        '''
        get a list of the devices on the loggernet server
        '''

        cmd = "list-devices;}"

        # print cora_cmd

        # run list-device cora script command to get list of devices on server
        # output = subprocess.Popen(cora_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # list_of_devices, error = output.communicate()
        list_of_devices = self.terminal.communicate(cora_cmd + cmd)

        # Extract the device list
        list_of_devices = list_of_devices[list_of_devices.find("*list-devices"):list_of_devices.find("+list-devices")]
        list_of_devices = list_of_devices.strip("*list-devices")
        list_of_devices = list_of_devices.strip("\r\n")
        list_of_devices = list_of_devices.split("\r\n")

        # print list_of_devices

        device_list = []

        for device in list_of_devices[1:len(list_of_devices) - 1]:
            # start = device.find("{")
            # stop = device.find("}")
            # device = device[start + 1:len(device) - 1]

            device = device.replace("{", "")
            device = device.replace("}", "")
            device = device.split()

            device_list.append(device)

        print device_list

        outFile = open("LoggerNet_" + self.server_ip + "_Settings.xml", "w")
        doc.write(outFile)


#---------------------------------------------------------------------------#
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('server_ip', help='ip address of the LoggerNet server')
    parser.add_argument('--username', help='username for LoggerNet server', default="")
    parser.add_argument('--password', help='password for LoggerNet server', default="")
    args = parser.parse_args()

    list_devices(args.server_ip, args.username, args.password)