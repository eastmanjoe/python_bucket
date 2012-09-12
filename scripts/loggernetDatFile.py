# The purpose of the script is to import a loggernet
# .dat file and parse it for future processing
#
# The loggernet .dat file is expected to have the TAO5 header
#
#
#TODO"s:

import sys


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


def parse(datfile):
    data = []

    row_data = parseLine(datfile)

    # Make sure file has data
    if row_data != "EOF":
        while True:
            row_data = parseLine(datfile)

            if row_data == "EOF":
                print "End Of File"
                break

            data.append(row_data)
    else:
        data = "EOF"

    datfile.close()
    return data


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
    """Check file extension"""
    if file_id != "":
        parse(file_id)
