#!/usr/bin/env python

# TODO's:
#   - Split syslog file into multiple files by date
import logging
import argparse

def openFile(file_pth):
    """Check file extension"""
    if file_pth.endswith('.syslog'):
        file_id = open(file_pth, 'r')
    else:
        file_id = ''
        print 'Wrong file type'

    return file_id

def parseFile(datafile):

    line = datafile.readline()

    if not line:
        print 'End Of File'

    else:
        date = line[0:6]
        # open a new file with the new date
        file_id_write = open('C:\Draker\Projects\NYLE\Mooradian_Clifton_Park' + '\\' + date.replace(' ', '_') + '.syslog', 'w')
        file_id_write.write(line)

        while True:
            line = datafile.readline()

            if not line:
                print 'End Of File'
                break

            if line[0:6] != date:

                # close the existing file
                if not file_id_write.closed:
                    file_id_write.close()

                date = line[0:6]

                # open a new file with the new date
                file_id_write = open('C:\Draker\Projects\NYLE\Mooradian_Clifton_Park' + '\\' + date.replace(' ', '_') + '.syslog', 'w')
                # file_id_write = 'C:\Draker\Projects\NYLE\Mooradian_Clifton_Park' + '\\' + date.replace(' ', '_') + '.syslog'
                # print file_id_write

            file_id_write.write(line)

        file_id_write.close()
    datafile.close()

def extractPitcher(datafile):
    line = datafile.readline()

    if not line:
        print 'End of FIle'
    else:
        date = line[0:6]
        # open a new file with the new date
        file_id_write = open('C:\Draker\Projects\NYLE\Mooradian_Clifton_Park' + '\\' + date.replace(' ', '_') + '_pitcher.syslog', 'w')
        if 'Pitcher' in line:
            file_id_write.write(line)

        while True:
            line = datafile.readline()

            if not line:
                print 'End of File'
                break
            elif 'Pitcher' in line:
                file_id_write.write(line)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--level', help='defines the log level to be dispayed to the screen', default='info')
    parser.add_argument('-f', '--filename', help='defines the filename of the debugs log', default='')
    args = parser.parse_args()

    file_id = openFile(args.filename)
    if file_id != '':
        # parseFile(file_id)
        extractPitcher(file_id)
