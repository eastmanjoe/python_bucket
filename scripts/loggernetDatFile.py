# The purpose of the script is to import a loggernet
# .dat file and parse it for future processing
#
# The loggernet .dat file is expected to have the TAO5 header
#
#
#TODO"s:

import sys


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def validateToa5Header(dat_file_type):
    """Check Dat File Header to make sure it is TOA5"""
    if dat_file_type == "TOA5":
        print "File has the TOA5 header"
        return True
    else:
        print "File does not have the TAO5 header, exiting"
        return False


def parseLine(datfile):
    line = datfile.readline().strip()

    if not line:
        return "EOF"
    else:
        split_line = line.split(",")

#        for i in range(len(split_line)):
#            split_line[i] = split_line[i].strip('"')

        return split_line


def parseFile(datfile):
    data = []

    row_data = parseLine(datfile)
#    print row_data

    # Make sure file has data
    if row_data != "EOF":
        while True:
            data.append(row_data)
            row_data = parseLine(datfile)

            if row_data == "EOF":
                print "End Of File"
                break

#            print row_data
    else:
        data = "EOF"

    datfile.close()
    return data

def importFile(datfile):
    data = []

    line = datfile.readline().strip()

    # Make sure file has data
    if line != "EOF":
        while True:
            data.append(line)
            line = datfile.readline().strip()

            if not line:
#                print "End Of File"
                break
    else:
        data = "EOF"

    datfile.close()
    return data


def parseDatData(data):
    #determine the number of rows and columns in the data table
    data_rows = len(data)
    data_columns = len(data[4].split(','))

    print "Dat file has %d columns and %d rows" % (data_columns, data_rows - 3)

    data_table = []

    #Separate the imported data into header variables and a data table
    for row in range(len(data)):
        split_data = data[row].split(',')
        #print split_data
            
        if row < 4:

            data_table.append(split_data)

        #put data into data table
        elif row >= 4:

            text_start_index = []
            text_stop_index = []

            #find strings that are comma seperated, have been split and concatonate back together
            while True:
                text_start_index = [column.startswith('"') and not column.endswith('"') for column in split_data]
                text_stop_index = [not column.startswith('"') and column.endswith('"') for column in split_data]
                
                if True in text_start_index:
                    #print text_start_index.index(True)
                    #print text_stop_index.index(True)
                    
                    split_data[text_start_index.index(True):text_stop_index.index(True) + 1] = [','.join(split_data[text_start_index.index(True):text_stop_index.index(True) + 1])]
                else:
                    break

            #convert numbers to either floats or integers
            for c in range(1, len(split_data)):
                if is_number(split_data[c]):
                    if '.' in split_data[c]:
                        split_data[c] = float(split_data[c])
                    else:
                        split_data[c] = int(split_data[c])

            data_table.append(split_data)
            
    #print data_table
    return data_table


def openFile(file_pth):
    """Check file extension"""
    if file_pth.endswith(".dat"):
        file_id = open(file_pth, "r")
    else:
        file_id = ""
        print "Wrong file type"

    return file_id

if __name__ == "__main__":
    file_id = openFile(sys.argv[1])
    if file_id != "":
        parseFile(file_id)
