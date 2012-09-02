# The purpose of the script is to import a loggernet
# .dat file and parse it for future processing
#
# The loggernet .dat file is expected to have the TAO5 header
#

import sys


file_folder = "/home/jeastman/programming/python/sample_data/"
file_name = "project_00_fifteenMin.dat"
'''Import the Dat file'''
#input_file = open(sys.argv[1], "r")
input_file = open(file_folder + file_name, "r")

for counter in input_file:
    line_buffer = input_file.readline()
    line_buffer = line_buffer.lower()
    print line_buffer
