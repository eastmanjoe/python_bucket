#!/usr/bin/env python
#
#
#
'''
This program starts two modbus slaves for the DAQ code to query.
'''

#---------------------------------------------------------------------------#
import os
import sys
import time
import argparse
import logging
import requests
import subprocess


#---------------------------------------------------------------------------#
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('num', help='number of modbus slave ports and number of slaves per port (format is 1:1)')
    parser.add_argument('ports', help='ports to use for the modbus slaves (format is COM1:COM2:COM3)')
    parser.add_argument('-v','--verbose', help='enables/disable modbus-tk verbose mode', default='False')
    parser.add_argument('-l','--level', help='defines the log level to be dispayed to the screen', default='info')
    parser.add_argument('-f','--filename', help='defines the filename of the debugs log', default='')
    args = parser.parse_args()