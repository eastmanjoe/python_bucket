# The purpose of the script is to import a loggernet
# .dat file and parse it for future processing
#
# The loggernet .dat file is expected to have the TAO5 header
#
#
#TODO's:
#   import data

import sys

def validateToa5Header(dat_file_type):
    '''Check Dat File Header to make sure it is TOA5'''
    if dat_file_type == "TOA5":
        print "File has the TOA5 header"
        return True
    else:
        print "File does not have the TAO5 header, exiting"
        return False

def parseDatFileLine(datfile):
    line = datfile.readline().strip()

    if not line:
        return "EOF"
    else:
        split_line = line.split(',')

        for i in range(len(split_line)):
            split_line[i] = split_line[i].strip('"')

        return split_line

def parseDatFile(datfile):
    header = []
    data = []

    row_data = parseDatFileLine(datfile)
    header.append(row_data)
    print header
    
    if validateToa5Header(header[0][0]):
        for row in range(1, 4):
            row_data = parseDatFileLine(datfile)
            header.append(row_data)
            print header

        while True:
            row_data = parseDatFileLine(datfile)

            if row_data == "EOF": 
                print "End Of File"
                break

            data.append(row_data)
            print row_data

    datfile.close()



if __name__ == "__main__":

    '''Check file extension'''
    if sys.argv[1].endswith('.dat'):
        file_id = open(sys.argv[1], 'r')
        parseDatFile(file_id)
    else:
        print 'Wrong file type'
