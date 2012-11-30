# The purpose of the script is to import a loggernet
# .dat file and plot it for data analysis
#
# The loggernet .dat file is expected to have the TAO5 header
#
#
#TODO"s:
#   Search for data to be plotted

#import user library
import loggernetDatFile
import julianCalc

#import system library
import sys
import numpy as np
from pylab import *
from matplotlib.collections import LineCollection

def convertTimestamp2Julian(timestamp_gregorian):
    #break timestamp into a list
    buffer_str = timestamp_gregorian.strip('"')
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
    #print "The julian date of %s %s is %f" % (buffer_str[0], #buffer_str[1], split_data[0])
    return julianCalc.julian_date(buffer_timestamp[0], buffer_timestamp[1], buffer_timestamp[2], buffer_timestamp[3], buffer_timestamp[4], buffer_timestamp[5])


def plotData(device_variable, device_index, device_total, data_table):

    ys = []
    #find the variable to plot and put into list ys
    for device_num in range(device_index, device_index + device_total - 1):
        for string_num in range(1, device_num_of_strings + 1):
            # print '"' + device_variable.format(string_num) + '_Avg({:d})"'.format(device_num)
            # print data_table[1].index('"' + device_variable.format(string_num) + '_Avg({:d})"'.format(device_num))

            device_data = []
            for counter in range(4, len(data_table)):
                if data_table[counter][data_table[1].index('"' + device_variable.format(string_num) + '_Avg({:d})"'.format(device_num))] == '"NAN"':
                    # print data_table[counter][data_table[1].index('"' + device_variable.format(string_num) + '_Avg({:d})"'.format(device_num))]
                    device_data.append(0)
                else:
                    # print data_table[counter][data_table[1].index('"' + device_variable.format(string_num) + '_Avg({:d})"'.format(device_num))]
                    device_data.append(data_table[counter][data_table[1].index('"' + device_variable.format(string_num) + '_Avg({:d})"'.format(device_num))])

        ys.append(np.asarray(device_data))
    
    print ys

    x = arange(len(data_table))
    
    ###### PLOTTING DATA #########
    # We need to set the plot limits, they will not autoscale
    ax = axes()
    ax.set_xlim((amin(x), amax(x)))
    ax.set_ylim((amin(amin(ys)), amax(amax(ys))))

    ## colors is sequence of rgba tuples
    ## linestyle is a string or dash tuple. Legal string values are
    ##          solid|dashed|dashdot|dotted.  The dash tuple is
    ##          (offset, onoffseq) where onoffseq is an even length
    ##          tuple of on and off ink in points.
    ##          If linestyle is omitted, 'solid' is used
    ## See matplotlib.collections.LineCollection for more information
    ## Make a sequence of x,y pairs

    line_segments = LineCollection([list(zip(x, y)) for y in ys],
        linewidths=(0.5, 1, 1.5, 2), linestyles = 'solid')
    line_segments.set_array(x)
    ax.add_collection(line_segments)
    fig = gcf()
    axcb = fig.colorbar(line_segments)
    # axcb.set_label('Line Number')
    ax.set_title('SCB Number: {:d}'.format(device_index))
    sci(line_segments)  # This allows interactive changing of the colormap.
    show()
    return 0


if __name__ == "__main__":

    #Data to plot
    device_variable = 'scb_dc_current_{:02d}'
    device_index = 1
    device_total = 10
    device_num_of_strings = 5

    file_id = loggernetDatFile.openFile(sys.argv[1])
    print sys.argv[1]

    if file_id != "":
        data = loggernetDatFile.importFile(file_id)
        data_table = loggernetDatFile.parseDatData(data)
        
        for counter in range(4, len(data_table)):
            data_table[counter][0] = convertTimestamp2Julian(data_table[counter][0])
        
        # print data_table
        plotData(device_variable, device_index, device_total, data_table)
