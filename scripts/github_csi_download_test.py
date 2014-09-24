#!/usr/bin/env python
#
#
#
'''
This program validates the gitHub download functionality for all projects in the project-firmware repository.
'''

#---------------------------------------------------------------------------#
import os
import sys
import time
import argparse
import logging
# import requests
import subprocess
import re


#---------------------------------------------------------------------------#
def getProjectList(folder_path):

    file_list = [f for f in os.listdir(folder_path) if os.path.splitext(f)[1] == ".cfg"]

    cfg_file_list = [f for f in file_list if re.match('s\d\d\d\d',f)]

    # print cfg_file_list

    project_list = []

    for f in cfg_file_list:
        match = re.match('s\d\d\d\d', f)
        buffer_str = match.group()
        buffer_str = buffer_str.replace('s', "")
        buffer_str = buffer_str.zfill(7)
        buffer_str += ".01"

        project_list.append(buffer_str)

    return project_list

def getProjectDasNum(folder_path):
    file_list = [f for f in os.listdir(folder_path) if os.path.splitext(f)[1] == ".CR1" or os.path.splitext(f)[1] == ".CR8"]

    cr_file_list = [f for f in file_list if re.match('s\d\d\d\d',f)]

    print cr_file_list

    project_list = []

    for f in cr_file_list:
        match = re.search('(s\d\d\d\d)(das-\d)', f)
        buffer_str[0] = match.group(1)
        buffer_str[0] = buffer_str[0].replace('s', "")
        buffer_str[0] = buffer_str[0].zfill(7)
        buffer_str[0] += ".01"


        buffer_str[1] = match.group(2)
        buffer_str[1] = buffer_str[1].uppercase()

        project_list.append(buffer_str)

    return project_list

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--path_project_firmware', help='path to the location of the Draker project-firmware repository', default='C:\home\jeastman\project-firmware\projects')
    parser.add_argument('--path_save-as', help='location to save the files to compare against the project-firmware', default='C:\home\jeastman\hardware-config\BaseStations\Testing\Validation')
    # parser.add_argument('-v','--verbose', help='enables/disable modbus-tk verbose mode', default='False')
    # parser.add_argument('-l','--level', help='defines the log level to be dispayed to the screen', default='info')
    # parser.add_argument('-f','--filename', help='defines the filename of the debugs log', default='')
    args = parser.parse_args()

    # sf_project_list = getProjectList(args.path_project_firmware)

    test_matrix = getProjectDasNum(args.path_project_firmware)
    print test_matrix

