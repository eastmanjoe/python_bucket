#!/usr/bin/env python
#
#
#
'''
This program combines Draker SN List_Truncated.csv from Sierra Wireless and
Projects with Cell Modem Report.csv from SalesForce into a single CSV file
that can be imported SalesForce to apply serial numbers to cell modems.  Also
determine if cell modem is on the recall list.

Need to remove the last 8 lines of the Projects with Cell Modem Report.csv file
or else parseCSV will fail.

TODO's:
    - parse Projects with Cell Modem Report.csv
        {0: {'Product': 'Raven XE CDMA Cellular Digital Modem for Verizon Networks (Ethernet Version)',
            'Site Product Property: Value': '09608995366',
            'Site': '0000006 - Newark Motors Solar',
            'Property Name': 'ESN Decimal'},
        1: {'Product': 'Raven XE CDMA Cellular Digital Modem for Verizon Networks (Ethernet Version)',
            'Site Product Property: Value': '60894226',
            'Site': '0000006 - Newark Motors Solar',
            'Property Name': 'ESN Hex'},
        2: {'Product': 'Raven XE CDMA Cellular Digital Modem for Verizon Networks (Ethernet Version)',
            'Site Product Property: Value': '166.141.190.104',
            'Site': '0000006 - Newark Motors Solar',
            'Property Name': 'IP Address'},
        3: {'Product': 'Raven XE CDMA Cellular Digital Modem for Verizon Networks (Ethernet Version)',
            'Site Product Property: Value': '802-338-0768',
            'Site': '0000006 - Newark Motors Solar',
            'Property Name': 'Phone Number'},
        4: {'Product': 'Raven XT CDMA Cellular Digital Modem for Verizon Networks (Serial Version)',
            'Site Product Property: Value': '09611799293',
            'Site': '0000017 - Lundberg 1',
            'Property Name': 'ESN Decimal'},
        5: {'Product': 'Raven XT CDMA Cellular Digital Modem for Verizon Networks (Serial Version)',
            'Site Product Property: Value': '60B40AFD',
            'Site': '0000017 - Lundberg 1',
            'Property Name': 'ESN Hex'},
        6: {'Product': 'Raven XT CDMA Cellular Digital Modem for Verizon Networks (Serial Version)',
            'Site Product Property: Value': '166.141.190.147',
            'Site': '0000017 - Lundberg 1',
            'Property Name': 'IP Address'},
        7: {'Product': 'Raven XT CDMA Cellular Digital Modem for Verizon Networks (Serial Version)',
            'Site Product Property: Value': '802-734-9774\xa0',
            'Site': '0000017 - Lundberg 1',
            'Property Name': 'Phone Number'},
        8: {'Product': 'Raven XE CDMA Cellular Digital Modem for Verizon Networks (Ethernet Version)',
            'Site Product Property: Value': '09606790143',
            'Site': '0000020 - Santa Clara University Parking Structure',
            'Property Name': 'ESN Decimal'},
        9: {'Product': 'Raven XE CDMA Cellular Digital Modem for Verizon Networks (Ethernet Version)',
            'Site Product Property: Value': '09606789538',
            'Site': '0000020 - Santa Clara University Parking Structure',
            'Property Name': 'ESN Decimal'},
        10: {'Product': 'Raven XE CDMA Cellular Digital Modem for Verizon Networks (Ethernet Version)',
            'Site Product Property: Value': '60679BFF',
            'Site': '0000020 - Santa Clara University Parking Structure',
            'Property Name': 'ESN Hex'},
        11: {'Product': 'Raven XE CDMA Cellular Digital Modem for Verizon Networks (Ethernet Version)',
            'Site Product Property: Value': '606799A2',
            'Site': '0000020 - Santa Clara University Parking Structure',
            'Property Name': 'ESN Hex'},
        12: {'Product': 'Raven XE CDMA Cellular Digital Modem for Verizon Networks (Ethernet Version)',
            'Site Product Property: Value': '166.141.190.111',
            'Site': '0000020 - Santa Clara University Parking Structure',
            'Property Name': 'IP Address'},
        13: {'Product': 'Raven XE CDMA Cellular Digital Modem for Verizon Networks (Ethernet Version)',
            'Site Product Property: Value': '166.141.190.112',
            'Site': '0000020 - Santa Clara University Parking Structure',
            'Property Name': 'IP Address'},
        14: {'Product': 'Raven XE CDMA Cellular Digital Modem for Verizon Networks (Ethernet Version)',
            'Site Product Property: Value': '802-735-8333',
            'Site': '0000020 - Santa Clara University Parking Structure',
            'Property Name': 'Phone Number'},
        15: {'Product': 'Raven XE CDMA Cellular Digital Modem for Verizon Networks (Ethernet Version)',
            'Site Product Property: Value': '802-735-8334',
            'Site': '0000020 - Santa Clara University Parking Structure',
            'Property Name': 'Phone Number'},
        16: {'Product': 'Raven XT CDMA Cellular Digital Modem for Verizon Networks (Serial Version)',
            'Site Product Property: Value': '09611792047',
            'Site': '0000024 - SF PUC North Point - EXPIRED',
            'Property Name': 'ESN Decimal'},
        17: {'Product': 'Raven XT CDMA Cellular Digital Modem for Verizon Networks (Serial Version)',
            'Site Product Property: Value': '60B3EEAF',
            'Site': '0000024 - SF PUC North Point - EXPIRED',
            'Property Name': 'ESN Hex'},
        18: {'Product': 'Raven XT CDMA Cellular Digital Modem for Verizon Networks (Serial Version)',
            'Site Product Property: Value': '166.141.190.135',
            'Site': '0000024 - SF PUC North Point - EXPIRED',
            'Property Name': 'IP Address'},
        19: {'Product': 'Raven XT CDMA Cellular Digital Modem for Verizon Networks (Serial Version)',
            'Site Product Property: Value': '802-238-4177',
            'Site': '0000024 - SF PUC North Point - EXPIRED',
            'Property Name': 'Phone Number'},
        ...
        ...
        4916: {'Product': 'Raven XE CDMA Cellular Digital Modem for Verizon Networks (Ethernet Version)',
            'Site Product Property: Value': '09616018466',
            'Site': '0003554 - Ronald Verhoeven Dairy Farm',
            'Property Name': 'ESN Decimal'},
        4917: {'Product': 'Raven XE CDMA Cellular Digital Modem for Verizon Networks (Ethernet Version)',
            'Site Product Property: Value': '60F46C22',
            'Site': '0003554 - Ronald Verhoeven Dairy Farm',
            'Property Name': 'ESN Hex'},
        4918: {'Product': 'Raven XE CDMA Cellular Digital Modem for Verizon Networks (Ethernet Version)',
            'Site Product Property: Value': '166.141.174.096',
            'Site': '0003554 - Ronald Verhoeven Dairy Farm',
            'Property Name': 'IP Address'},
        4919: {'Product': 'Raven XE CDMA Cellular Digital Modem for Verizon Networks (Ethernet Version)',
            'Site Product Property: Value': '802-881-8607',
            'Site': '0003554 - Ronald Verhoeven Dairy Farm',
            'Property Name': 'Phone Number'},
        4920: {'Product': 'Raven XE CDMA Cellular Digital Modem for Verizon Networks (Ethernet Version)',
            'Site Product Property: Value': '1342802352',
            'Site': '0003554 - Ronald Verhoeven Dairy Farm',
            'Property Name': 'Serial Number'},
        ...
        ...
        4926: {'Product': 'Raven XE GSM Cellular Digital Modem (Ethernet Version) CANADA',
            'Site Product Property: Value': '70.28.251.86',
            'Site': '0003557 - Baltimore Arena',
            'Property Name': 'IP Address'},
        4927: {'Product': 'Raven XE GSM Cellular Digital Modem (Ethernet Version) CANADA',
            'Site Product Property: Value': '416-578-7237',
            'Site': '0003557 - Baltimore Arena',
            'Property Name': 'Phone Number'},
        4928: {'Product': 'Raven XE GSM Cellular Digital Modem (Ethernet Version) CANADA',
            'Site Product Property: Value': '89302610102012736443',
            'Site': '0003557 - Baltimore Arena',
            'Property Name': 'SIM Card Number'},
        ...
        ...
        4934: {'Product': None, 'Site Product Property: Value': 'Projects with Cell Modem List',
            'Site': None,
            'Property Name': None},
        4935: {'Product': None, 'Site Product Property: Value': 'Copyright (c) 2000-2014 salesforce.com, inc. All rights reserved.',
            'Site': None,
            'Property Name': None},
        4936: {'Product': None, 'Site Product Property: Value': 'Confidential Information - Do Not Distribute',
            'Site': None,
            'Property Name': None},
        4937: {'Product': None, 'Site Product Property: Value': 'Generated By:  Joe Eastman  11/13/2014 12:10 PM',
            'Site': None,
            'Property Name': None},
        4938: {'Product': None, 'Site Product Property: Value': 'Draker',
            'Site': None,
            'Property Name': None}
        }

    - generate the following dict entry for each project:
        {0:
            {'Site':'0000006 - Newark Motors Solar','ESN Decimal':'09608995366',
            'ESN Hex':'60894226', 'IP Address':'166.141.190.104',
            'Phone Number':'802-338-0768'},
        1:{},
        2:{}
        }

    - parse Draker SN List_Truncated.csv
        {0: {'ESN Dec': '09615950486', 'SN#': '1325794412', 'ESN Hex': '60F36296'},
        1: {'ESN Dec': '09615950472', 'SN#': '1325794439', 'ESN Hex': '60F36288'},
        2: {'ESN Dec': '09615950468', 'SN#': '1325793322', 'ESN Hex': '60F36284'},
        3: {'ESN Dec': '09615950465', 'SN#': '1325793301', 'ESN Hex': '60F36281'},
        4: {'ESN Dec': '09615950403', 'SN#': '1325793316', 'ESN Hex': '60F36243'},
        5: {'ESN Dec': '09615950402', 'SN#': '1325792306', 'ESN Hex': '60F36242'},
        ...
        ...
        580: {'ESN Dec': '09615242808', 'SN#': '1225709459', 'ESN Hex': '60E89638'}
        }

    - add serial number to formatted SalesForce dict
    - check if serial number is in the recall range
    - write dictionary to csv file

GOAL:
    Generate the following csv file from two different csv files:
        'Site', 'ESN Decimal', 'ESN Hex', 'Serial Number', 'IP Address', 'Phone Number', 'Product', 'Recalled'
        '0000006 - Newark Motors Solar', '09608995366', '60894226', '1006465880', '166.141.190.104', '802-338-0768'
'''

#---------------------------------------------------------------------------#
import argparse
import logging
import csv
import time

#---------------------------------------------------------------------------#
# global variables
# sw_dict = {}
# sf_dict = {}


#---------------------------------------------------------------------------#
def setupLogger(loglevel, log_filename):

    # assuming loglevel is bound to the string value obtained from the
    # command line argument. Convert to upper case to allow the user to
    # specify --log=DEBUG or --log=debug
    loglevel = loglevel.upper()

    numeric_level = getattr(logging, loglevel, None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)

    logger.setLevel(loglevel)

    # configure logger
    handler_stream_formatter = logging.Formatter('%(levelname)s: %(message)s')
    handler_stream = logging.StreamHandler()
    handler_stream.setLevel(loglevel)
    handler_stream.setFormatter(handler_stream_formatter)
    logger.addHandler(handler_stream)

    if log_filename != '':
        log_path = 'C:\\cygwin\\home\\jeastman\\python_bucket\\debug_logs\\'
        # log_path = 'c:\\temp\\'
        # log_path = '/home/jeastman/logs/'
        handler_file = logging.FileHandler(log_path + log_filename)
        # handler_file = logging.FileHandler(log_path + log_filename)
        handler_file_formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s')
        handler_file.setFormatter(handler_file_formatter)
        handler_file.setLevel(loglevel)
        logger.addHandler(handler_file)

    logger.info('Log Level is: %s' % (loglevel))
    logger.info('Log Filename is: %s' % (log_filename))



def parseCSV(file_pth):
    csv_dict = {}
    row_count = 0

    with open(file_pth, 'rb') as csvfile:
        logger.info('Parsing: %s' % csvfile.name)
        csv_dictreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')

        for row in csv_dictreader:
            # if row_count == 17:
                # logger.debug(csv_dict)
                # break

            # logger.debug(row)
            csv_dict[row_count] = row

            row_count += 1

        logger.debug(csv_dict)
        logger.info('Closing: %s' % csvfile.name)

    return csv_dict



def formatSfdict(dict_sf):
    formatSfdict = {}
    count = 0

    for sf_key, sf_value in dict_sf.items():
        if dict_sf[sf_key]['Site']:
            pass

    return formatted_sf_dict



def combineSwSfDict(sw_dict, sf_dict):
    combined_dict = dict(sf_dict)

    for sw_key, sw_value in sw_dict.items():
        for sf_key, sf_value in sf_dict.items():
            if sw_value['ESN Hex'] == sf_value['ESN Hex']:
                combined_dict[sf_key]['Serial Number'] = sw_value['SN#']

    return combined_dict


def isModemRecalled(site_dict):
    recalled = False
    sn = int(site_dict['Serial Number'][:4])

    if 'Raven XE' in site_dict['Product']:
        if (sn >= 1134 and sn <= 1142) or (sn >= 1221 and sn <= 1252):
            recalled = True

    elif 'Raven XT' in site_dict['Product']:
        if sn >= 1221 and sn <= 1325:
            recalled = True

    return recalled



def writeCSV(file_pth, write_dict):
    fieldnames = [
        'Site', 'ESN Decimal', 'ESN Hex', 'Serial Number',
        'IP Address', 'Phone Number', 'Product', 'Recalled'
        ]

    with open(file_pth, 'wb') as csvfile:
        logger.info('Writing: %s' % csvfile.name)

        csv_dictwriter = csv.DictWriter(
            csvfile, fieldnames, delimiter=','
            )

        csv_dictwriter.writeheader()

        for row in write_dict:
            csv_dictwriter.writerow(write_dict[row])



#---------------------------------------------------------------------------#
if __name__ == '__main__':
    logger = logging.getLogger('logger')

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--sw_file', help='file path and name of Sierra Wireless file',
        default='C:\\Users\\jeastman\\Desktop\\Draker SN List_Truncated.csv'
        )
    parser.add_argument(
        '--sf_file', help='file path and name of SalesForce file',
        default='C:\\Users\\jeastman\\Desktop\\Projects with Cell Modem Report 2.csv'
        )
    parser.add_argument(
        '--write_file', help='file path and name of complete file',
        default='C:\\Users\\jeastman\\Desktop\\Projects with Cell Modem Report - All Info.csv'
        )
    parser.add_argument(
        '-l','--level',
        help='defines the log level to be dispayed to the screen',
        default='debug'
        )
    parser.add_argument(
        '-f','--filename', help='defines the filename of the debugs log',
        default=''
        )
    args = parser.parse_args()

    # sf_dict = {
    #     0: {'Site': '0000006 - Newark Motors Solar', 'ESN Decimal': '09608995366',
    #          'ESN Hex':'60894226',
    #          'IP Address':'166.141.190.104', 'Phone Number':'802-338-0768',
    #          'Product': 'Raven XE CDMA Cellular Digital Modem for Verizon Networks (Ethernet Version)'
    #         },

    #     1: {'Site': '0000017 - Lundberg 1', 'ESN Decimal': '09611799293',
    #         'ESN Hex':'60B40AFD',
    #         'IP Address':'166.141.190.147', 'Phone Number':'802-734-9774',
    #          'Product': 'Raven XT CDMA Cellular Digital Modem for Verizon Networks (Serial Version)'
    #         },

    #     2: {'Site': '0000020 - Santa Clara University Parking Structure',
    #         'ESN Decimal': '09606790143',
    #         'ESN Hex':'60679BFF',
    #         'IP Address':'166.141.190.111', 'Phone Number':'802-735-8333',
    #          'Product': 'Raven XE CDMA Cellular Digital Modem for Verizon Networks (Ethernet Version)'
    #         },

    #     3: {'Site': '0000020 - Santa Clara University Parking Structure',
    #         'ESN Decimal': '09606789538',
    #         'ESN Hex':'606799A2',
    #         'IP Address':'166.141.190.112', 'Phone Number':'802-735-8334',
    #          'Product': 'Raven XE CDMA Cellular Digital Modem for Verizon Networks (Ethernet Version)'
    #         },

    #     #the following are all recalled modems.
    #     4: {'Site': '0001646 - G&S Hudson (West NY BOE New School, 600 55th)',
    #         'ESN Decimal': '09615253842',
    #         'ESN Hex':'60E8C152',
    #         'IP Address':'166.148.254.41', 'Phone Number':'802-735-7966',
    #          'Product': 'Raven XE CDMA Cellular Digital Modem for Verizon Networks (Ethernet Version)'
    #         },

    #     5: {'Site': '0001261 - G&S Hudson (Bayonne City Hall, 630 Ave C)',
    #         'ESN Decimal': '09615257656',
    #         'ESN Hex':'60E8D038',
    #         'IP Address':'166.148.214.206', 'Phone Number':'802-318-1977',
    #          'Product': 'Raven XT CDMA Cellular Digital Modem for Verizon Networks (Serial Version)'
    #         },

    #     6: {'Site': '0001432 - GFUSD McKee Middle School',
    #         'ESN Decimal': '09615257649',
    #         'ESN Hex':'60E8D031',
    #         'IP Address':'166.148.214.200', 'Phone Number':'802-734-3757',
    #          'Product': 'Raven XT CDMA Cellular Digital Modem for Verizon Networks (Serial Version)'
    #         },

    #     7: {'Site': '0001435 - GFUSD Middle School',
    #         'ESN Decimal': '09615257629',
    #         'ESN Hex':'60E8D01D',
    #         'IP Address':'166.148.214.204', 'Phone Number':'802-238-2377',
    #          'Product': 'Raven XT CDMA Cellular Digital Modem for Verizon Networks (Serial Version)'
    #         },

    #     8: {'Site': '0001427 - GFUSD Valle Verde Elementary',
    #         'ESN Decimal': '09615257563',
    #         'ESN Hex':'60E8CFDB',
    #         'IP Address':'166.148.214.193', 'Phone Number':'802-578-3651',
    #          'Product': 'Raven XT CDMA Cellular Digital Modem for Verizon Networks (Serial Version)'
    #         }
    #     }

    # cell_modem_dict = {
    #     0: {'Site': '0000006 - Newark Motors Solar', 'ESN Decimal': '09608995366',
    #          'ESN Hex':'60894226', 'Serial Number': '1006465880',
    #          'IP Address':'166.141.190.104', 'Phone Number':'802-338-0768',
    #          'Product': 'Raven XE CDMA Cellular Digital Modem for Verizon Networks (Ethernet Version)'
    #         },

    #     1: {'Site': '0000017 - Lundberg 1', 'ESN Decimal': '09611799293',
    #         'ESN Hex':'60B40AFD', 'Serial Number': '1048558008',
    #         'IP Address':'166.141.190.147', 'Phone Number':'802-734-9774',
    #          'Product': 'Raven XT CDMA Cellular Digital Modem for Verizon Networks (Serial Version)'
    #         },

    #     2: {'Site': '0000020 - Santa Clara University Parking Structure',
    #         'ESN Decimal': '09606790143',
    #         'ESN Hex':'60679BFF', 'Serial Number': '1010467927',
    #         'IP Address':'166.141.190.111', 'Phone Number':'802-735-8333',
    #          'Product': 'Raven XE CDMA Cellular Digital Modem for Verizon Networks (Ethernet Version)'
    #         },

    #     3: {'Site': '0000020 - Santa Clara University Parking Structure',
    #         'ESN Decimal': '09606789538',
    #         'ESN Hex':'606799A2', 'Serial Number': '1010466626',
    #         'IP Address':'166.141.190.112', 'Phone Number':'802-735-8334',
    #          'Product': 'Raven XE CDMA Cellular Digital Modem for Verizon Networks (Ethernet Version)'
    #         },

    #     #the following are all recalled modems.
    #     4: {'Site': '0001646 - G&S Hudson (West NY BOE New School, 600 55th)',
    #         'ESN Decimal': '09615253842',
    #         'ESN Hex':'60E8C152', 'Serial Number': '1235706778',
    #         'IP Address':'166.148.254.41', 'Phone Number':'802-735-7966',
    #          'Product': 'Raven XE CDMA Cellular Digital Modem for Verizon Networks (Ethernet Version)'
    #         },

    #     5: {'Site': '0001261 - G&S Hudson (Bayonne City Hall, 630 Ave C)',
    #         'ESN Decimal': '09615257656',
    #         'ESN Hex':'60E8D038', 'Serial Number': '1237734877',
    #         'IP Address':'166.148.214.206', 'Phone Number':'802-318-1977',
    #          'Product': 'Raven XT CDMA Cellular Digital Modem for Verizon Networks (Serial Version)'
    #         },

    #     6: {'Site': '0001432 - GFUSD McKee Middle School',
    #         'ESN Decimal': '09615257649',
    #         'ESN Hex':'60E8D031', 'Serial Number': '1237734869',
    #         'IP Address':'166.148.214.200', 'Phone Number':'802-734-3757',
    #          'Product': 'Raven XT CDMA Cellular Digital Modem for Verizon Networks (Serial Version)'
    #         },

    #     7: {'Site': '0001435 - GFUSD Middle School',
    #         'ESN Decimal': '09615257629',
    #         'ESN Hex':'60E8D01D', 'Serial Number': '1237735217',
    #         'IP Address':'166.148.214.204', 'Phone Number':'802-238-2377',
    #          'Product': 'Raven XT CDMA Cellular Digital Modem for Verizon Networks (Serial Version)'
    #         },

    #     8: {'Site': '0001427 - GFUSD Valle Verde Elementary',
    #         'ESN Decimal': '09615257563',
    #         'ESN Hex':'60E8CFDB', 'Serial Number': '1238712032',
    #         'IP Address':'166.148.214.193', 'Phone Number':'802-578-3651',
    #          'Product': 'Raven XT CDMA Cellular Digital Modem for Verizon Networks (Serial Version)'
    #         }
    #     }

    setupLogger(args.level, args.filename)
    logger.info(
        'Script started on: %s' % time.asctime(time.localtime(time.time()))
        )

    # sw_dict = parseCSV(args.sw_file)
    sf_dict = parseCSV(args.sf_file)

    sf_dict = formatSfdict(sf_dict)

    # cell_modem_dict = combineSwSfDict(sw_dict, sf_dict)

    # logger.debug(cell_modem_dict)

    # for row in dict(cell_modem_dict):
    #     if isModemRecalled(cell_modem_dict[row]):
    #         cell_modem_dict[row]['Recalled'] = 'Yes'
    #     else:
    #         cell_modem_dict[row]['Recalled'] = 'No'

    # logger.debug(cell_modem_dict)
    # writeCSV(args.write_file, cell_modem_dict)