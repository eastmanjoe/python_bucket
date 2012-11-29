# The purpose of the script is to import a loggernet
# .dat file and plot it for data analysis
#
# The loggernet .dat file is expected to have the TAO5 header
#
#
#TODO"s:
#   Import loggernet file
#   Search for data to be plotted

#import user library
import loggernetDatFile
import julianCalc

#import system library
import sys
import numpy as np
from pylab import *
from matplotlib.collections import LineCollection


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#Data to plot
device_variable = 'scb_dc_current_{:02d}'
device_index = 3
device_total = 2


file_id = loggernetDatFile.openFile(sys.argv[1])

if file_id != "":
    data = loggernetDatFile.importFile(file_id)

data_table = []

#determine the number of rows and columns in the data table
data_rows = len(data)
data_columns = len(data[4].split(','))

print "Dat file has %d columns and %d rows" % (data_columns, data_rows - 3)

#Separate the imported data into header variables and a data table
for i in range(len(data)):
    if i == 0:
        data_header = data[0].split('","')

        #strip random quotes from strings
        for counter in range(len(data_header)):
            data_header[counter] = data_header[counter].strip('"')

    if i == 1:
        data_variables = data[1].split('","')

        #strip random quotes from strings
        for counter in range(len(data_variables)):
            data_variables[counter] = data_variables[counter].strip('"')

    #if i == 2:
        #data_units = data[2].split('","')

        #strip random quotes from strings
        #for counter in range(len(data_units)):
            #data_units[counter] = data_units[counter].strip('"')

    #if i == 3:
        #data_processing = data[3].split('","')

        #strip random quotes from strings
        #for counter in range(len(data_processing)):
            #data_processing[counter] = data_processing[counter].strip('"')

    if i >= 4:
        #put comma separated string into a list
        split_data = data[i].split(',')

        #break timestamp into a list
        buffer_str = split_data[0].strip('"')
        buffer_str = buffer_str.split(' ')
        buffer_timestamp = buffer_str[0].split('-')
        buffer_timestamp.extend(buffer_str[1].split(':'))

        #convert strings to integers
        buffer_timestamp[0] = int(buffer_timestamp[0])
        buffer_timestamp[1] = int(buffer_timestamp[1])
        buffer_timestamp[2] = int(buffer_timestamp[2])
        buffer_timestamp[3] = int(buffer_timestamp[3])
        buffer_timestamp[4] = int(buffer_timestamp[4])
        buffer_timestamp[5] = int(buffer_timestamp[5])

        #calculate the julian date from the timestamp
        split_data[0] = julianCalc.julian_date(buffer_timestamp[0],
            buffer_timestamp[1], buffer_timestamp[2], buffer_timestamp[3],
            buffer_timestamp[4], buffer_timestamp[5])
        #print "The julian date of %s %s is %f" % (buffer_str[0],
            #buffer_str[1], split_data[0])

        #convert numbers to either floats pr integers
        for i in range(1, len(split_data)):
            if is_number(split_data[i]):
                if '.' in split_data[i]:
                    split_data[i] = float(split_data[i])
                else:
                    split_data[i] = int(split_data[i])

        data_table.append(split_data)
        #print data_table

ys = []
#find the variable to plot and put into list ys
#for device_counter in range(1, device_total + 1):
for string_num in range(1, 3):
    print device_variable.format(string_num) + \
                "_Avg({:d})".format(device_index)

    x = [data_table[counter][0] for counter in range(len(data_table))]

    device_data = []
    for counter in range(len(data_table)):
        device_data.append(data_table[counter][data_variables.index(
                device_variable.format(string_num) +
                "_Avg({:d})".format(device_index))])

        print device_data

    device_data = np.array(device_data)
    print device_data
    #ys = numpy.vstack(([ys], [[device_data]])
    #print ys, "\n"

    #ys = [data_table[counter][data_variables.index(device_variable.format(
        #string_num) + "_Avg({:d})".format(device_index))]
        #for counter in range(len(data_table))]

#print x
#print ys
###### PLOTTING DATA #########
# We need to set the plot limits, they will not autoscale
#ax = axes()
#ax.set_xlim((amin(x), amax(x)))
#ax.set_ylim((amin(amin(ys)), amax(amax(ys))))

## colors is sequence of rgba tuples
## linestyle is a string or dash tuple. Legal string values are
##          solid|dashed|dashdot|dotted.  The dash tuple is (offset, onoffseq)
##          where onoffseq is an even length tuple of on and off ink in points.
##          If linestyle is omitted, 'solid' is used
## See matplotlib.collections.LineCollection for more information
## Make a sequence of x,y pairs
#print [list(zip(x, y)) for y in ys]

#line_segments = LineCollection([list(zip(x, y)) for y in ys],
    #linewidths=(0.5, 1, 1.5, 2), linestyles = 'solid')
#print line_segments
#line_segments.set_array(data_table[0])
#ax.add_collection(line_segments)
#fig = gcf()
#axcb = fig.colorbar(line_segments)
#axcb.set_label('Line Number')
#ax.set_title('SCB Number: {:d}'.format(device_index))
#sci(line_segments)  # This allows interactive changing of the colormap.
#show()
