#!/usr/bin/env python

'''
Run Cora commands and generate an XML file with all of the settings
'''

#---------------------------------------------------------------------------#
#import packages
import os
import sys
import argparse
import time
import logging
import threading
import subprocess
from lxml import etree

#---------------------------------------------------------------------------#
def main(server_ip, username, password):

    page = etree.Element('loggerNet_Network')
    doc = etree.ElementTree(page)

    cora_cmd = "cora_cmd"
    cora_cmd += " --input={connect " + server_ip
    if username != "":
        cora_cmd += " --username=" + username
        cora_cmd += " --password=" + password

    cora_cmd += ";"

    cora_cmd += "list-devices;"
    cora_cmd += "}"

    # print cora_cmd

    # run list-device cora script command to get list of devices on server
    # output = subprocess.Popen(cora_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # list_of_devices, error = output.communicate()
    list_of_devices = subprocess.check_output(cora_cmd)

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

    outFile = open("LoggerNet_" + server_ip + "_Settings.xml", "w")
    doc.write(outFile)


#---------------------------------------------------------------------------#
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('server_ip', help='ip address of the LoggerNet server')
    parser.add_argument('--username', help='username for LoggerNet server', default="")
    parser.add_argument('--password', help='password for LoggerNet server', default="")
    args = parser.parse_args()

    main(args.server_ip, args.username, args.password)