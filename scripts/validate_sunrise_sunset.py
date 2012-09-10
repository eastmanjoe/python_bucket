import solar
import datetime

latitude = 44.467806
longitude = -73.215565
altitude = 34


'''Import the Dat file'''
file_directory = '/home/jeastman/Programming/Python/sample_data/'
file_name = 'project_03_panelControl.dat'

file_id = open(file_directory + file_name, "r")

for line in file_id:
    print line,
