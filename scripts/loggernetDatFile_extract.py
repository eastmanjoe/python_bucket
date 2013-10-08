# The purpose of the script is to import a loggernet
# .dat file and parse it for future processing
#
# The loggernet .dat file is expected to have the TAO5 header


import sys

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def parseFile(datfile):
    # Locate index of column numbers of interest
    header_title_1 = 'TIMESTAMP'
    header_title_2 = 'srs_irrad_Avg(2)'
    header_title_3 = 'met_irrad_02_Avg'

    data = []
    data_table = []
    dat_file = []

    line = datfile.readline().strip()

    # Make sure file has data
    if not line:
        data = 'EOF'

    else:
        while True:
            # data.append(line)
            line = datfile.readline().strip()

            if not line:
                print 'End Of File'
                break



    datfile.close()

    # determine the number of rows and columns in the data table
    data_columns = len(data[4].split(','))
    # data_rows = len(data)
    data_rows = 12

    print 'Dat file has %d columns and %d rows' % (data_columns, data_rows)


    # get data into data table
    # for row in range(len(data)):
    for row in range(data_rows):
        split_data = data[row].split(',')

        if row == 1:
            data_table.append(split_data)

        elif row == 2:
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



            data_table.append(split_data)

    # print data_table


    header_title_1_index = data_table[0].index('"' + header_title_1 + '"')
    header_title_2_index = data_table[0].index('"' + header_title_2 + '"')
    header_title_3_index = data_table[0].index('"' + header_title_3 + '"')

    print '%s index is %d' % (header_title_1, header_title_1_index)
    print '%s index is %d' % (header_title_2, header_title_2_index)
    print '%s index is %d' % (header_title_3, header_title_3_index)

    # print data_table[0][header_title_1_index]
    # print data_table[0][header_title_2_index]
    # print data_table[0][header_title_3_index]

    for row in range(data_rows - 2):
        dat_file_row = [data_table[row][header_title_1_index], data_table[row][header_title_2_index], data_table[row][header_title_3_index]]
        print dat_file_row
        dat_file.append(dat_file_row)

    print dat_file


def openFile(file_pth):
    """Check file extension"""
    if file_pth.endswith('.dat'):
        file_id = open(file_pth, 'r')
    else:
        file_id = ''
        print 'Wrong file type'

    return file_id

if __name__ == '__main__':
    file_id = openFile(sys.argv[1])
    if file_id != '':
        parseFile(file_id)
