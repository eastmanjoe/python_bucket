###############################################################################################################################################
''' This script expects THREE parameters passed in, the temp sensor ROM-ID, X320 MAC address, and the name of the NIC

parameter 1: temp sensor ROM-ID. E.g. 78000004DA069A28
parameter 2: x320 mac address.  E.g. 00-0C-C8-02-BF-2B
parameter 3 option 1: 0     ; When '0' is passed in, the default NIC name 'Local Area Connection' is used
parameter 3 option 2: Name_Of_NIC    ;No spaces are accepted, nor you can pass in strings in quotes  e.g. 'this is a test' is not acceptable

This is how you would run the python script itself:

c:\LabVIEW\development\Projects\DAS4\Supporting Scripts\x320 configuration>X320_config.py 78000004DA069A28 00-0C-C8-02-BF-2B House_Network

And to run the executable it is the same:

c:\LabVIEW\development\Projects\DAS4\Supporting Scripts\x320 configuration\x320 exe>X320_config.exe 78000004DA069A28 00-0C-C8-02-BF-2B House_Network

The script generates a text file (log file) as an output:
c:\temp\x320_log.txt
'''
#
# Revision Log:
# 07.26.13 - Added flag settings on failure and revision log - jortiz
# 09.04.13 - Removed check of macaddrs and initial 'try' at 172.28.0.2, now config X320 whether preconfigured or not
# 09.12.13 - Added Config for Ain2, updated all configurations to match 'X-320-I configuration - version 3' document
# 09.12.13 - Corrected slope on Ain4 from 5 to 1, updated all configurations to match 'X-320-I configuration - version 4' document
# 09.13.13 - Updated control page to show pulse rate 1 and pulse count 1, changed the description of Ain1 and Ain2 to show the # symbol
# 09.17.13 - Changed arp command to match the X320 documentation: 'arp -s 11.22.33.44 00-0c-c8-01-00-XX'
# 09.19.13 - Added code to ensure that the entered X320 MACID matches the retrieved X320 MACID
# 09.27.13 - Added arp command as suggested by Thadeus B @ Austin Draker; macaddress entries will be converted to lowercase; Third input parameters is now required
# 10.17.13 - Added help file information and dynamic networking information
#
#
###############################################################################################################################################

import requests
import subprocess
import sys
import pdb
import time
import re
import os
import logging
import argparse

#---------------------------------------------------------------------------#
def setupLogger(loglevel, logfilename):
    # assuming loglevel is bound to the string value obtained from the
    # command line argument. Convert to upper case to allow the user to
    # specify --log=DEBUG or --log=debug
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)

    # configure logger
    logger.setLevel(loglevel.upper())
    handler_stream_formatter = logging.Formatter('%(levelname)s: %(message)s')
    handler_stream = logging.StreamHandler()
    handler_stream.setFormatter(handler_stream_formatter)
    handler_stream.setLevel(loglevel.upper())
    logger.addHandler(handler_stream)

    if logfilename != '':
        # handler_file = logging.FileHandler('/home/jeastman/logs/' + logfilename)
        handler_file = logging.FileHandler(logfilename)
        logger.debug('Log Filename is: %s' % (handler_file))
        handler_file_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        handler_file.setFormatter(handler_file_formatter)
        handler_file.setLevel(loglevel.upper())
        logger.addHandler(handler_file)

    logger.info('Log Level is: %s' % (loglevel))
    if logfilename != '': logger.info('Log Filename is: %s' % (logfilename))
#---------------------------------------------------------------------------#

#---------------------------------------------------------------------------#
def establishConnection(ip_address, x320_mac, lan_connection_name):
    logger.info('Attemping to establish connection to the X320...')

    logger.debug('Setting arp cache')
    arp = ['arp', '-s', ip_address, x320_mac]    #this command is what is was suggested in the manual
    #arp = ['netsh', 'interface', 'ipv4', 'add', 'neighbors', lan_connection_name, ip_address, x320_mac]    #this command is Thadeus's suggestion
    subprocess.call(arp)

    logger.debug('Pinging X320')
    ping = ['ping', '-n', '5', '-l', '102', ip_address]
    ping_response = subprocess.call(ping)
    logger.debug('Ping Response is: %d' % ping_response)

    if (ping_response == 0):
        logger.info('X320 replied succesfully to a ping')
        return True

    else:
        logger.info('X320 did not reply to a ping.')
        return False

#---------------------------------------------------------------------------#

#---------------------------------------------------------------------------#
def x320MacCheck(auth, ip_address, x320_mac):
    logger.info('Checking the MAC ID supplied against the MAC ID queried...')

    r = requests.get('http://' + ip_address + '/about.html', auth=auth, timeout=5)
    assert r.status_code == 200

    #check to see that entered X320 MACID matches retrieved X320 MACID
    X320_MACID_retrieved = re.search('([a-fA-F0-9]{2}[:|\-]?){6}', r.text)

    #the section of code below makes sure that retrieved MACID (pmac, for 'MACID from x320 web page') matches the scanned-in MACID
    if X320_MACID_retrieved:
        page_mac = X320_MACID_retrieved.group(0)
        pmac = page_mac.replace(':', '-')

        if x320_mac.lower() == pmac.lower():
            logger.debug('MAC Address Enterned is: %s' % x320_mac)
            logger.debug('MAC Address Retrieved is: %s' % pmac)
            logger.info('MAC Addresses MATCH')
            return True

        else:
            logger.debug('MAC Address Enterned is: %s' % x320_mac)
            logger.debug('MAC Address Retrieved is: %s' % pmac)
            logger.info('MAC Addresses do NOT MATCH')
            return False

    else:
        logger.info('Could not retrieve MAC Addres from html page...')
        return False
#---------------------------------------------------------------------------#

#---------------------------------------------------------------------------#
def configX320(auth, ip_address, subnet, gateway, ambient_temp_id):
    logger.info('Configuring the X-320-I...')

    url = 'http://' + ip_address + '/'
    ip_address_fields = ip_address.split('.')
    subnet_fields = subnet.split('.')
    gateway_fields = gateway.split('.')

    #config temp units
    # logger.debug( '-----------------------------------------------------------')
    # logger.debug( 'Setting temperature units to C')
    # logger.debug( '-----------------------------------------------------------')
    r = requests.get(url + 'aboutSetup.srv?units=c', auth=auth)
    assert r.status_code == 200

    #config nwtwork
    # logger.debug('-----------------------------------------------------------')
    # logger.debug('Setting network configuration')
    # logger.debug('-----------------------------------------------------------')
    setting_string = 'networkSetup.srv?dhcpEnbled=no&ip1=' + ip_address_fields[0] + '&ip2=' \
        + ip_address_fields[1] + '&ip3=' + ip_address_fields[2] + '&ip4=' + ip_address_fields[3] \
        + '&nm1=' + subnet_fields[0] + '&nm2=' + subnet_fields[1] + '&nm3=' + subnet_fields[2] + \
        '&nm4=' + subnet_fields[3] + '&gw1=' + gateway_fields[0] + '&gw2=' + gateway_fields[1] + \
        '&gw3=' + gateway_fields[2] + '&gw4=' + gateway_fields[3] + '&pdns1=0&pdns2=0&pdns3=0' \
        '&pdns4=0&adns1=0&adns2=0&adns3=0&adns4=0&lP=80&nS=ten&nM=half&sA=&msp=25&sUN=&sP=' \
        '&sndA=&email1=&email2=&email3=&email4=&email5=&eCType=0'
    logger.debug('Network Configuration: %s' % setting_string)

    r = requests.get(url + setting_string, auth=auth)
    assert r.status_code == 200

    #config analog input 1
    # logger.debug('-----------------------------------------------------------')
    # logger.debug('Configuring analog input 1 as Single-Ended')
    # logger.debug('-----------------------------------------------------------')
    setting_string = 'analogSetup.srv?anDesc=Irradiance%20%231&anUnit=V&adp=5&anOnLbl=ON&anA1Col=0' \
        '&anOffLbl=OFF&anA2Col=1&anANCol=4&difMd=0&slp=1.00000&off=0.00000&anAlrm1=4.00000' \
        '&anAT1=1&anAlrm2=1.00000&anAT2=0&anDBand=0.50000&anEmailOpt=0&anOAct1=1&anOAlrm1=1' \
        '&ioAnOpt1=1&anOAct2=1&anOAlrm2=1&ioAnOpt2=1&anRRAct1=1&anRRAlrm1=1&ioAnRROpt1=1&anRRAct2=1' \
        '&anRRAlrm2=1&ioAnRROpt2=1&anRRAct3=1&anRRAlrm3=1&ioAnRROpt3=1&anRmtAct=1&anRmtAlrm=1&anIoRmtAct=on'
    logger.debug('Analog Input 1: %s' % setting_string)

    r = requests.get(url + setting_string, auth=auth)
    r = requests.get(url + 'anachng.srv?aNum=1&anMd=0', auth=auth)

    assert r.status_code == 200
    time.sleep(1)

    #config analog input 2
    # logger.debug('-----------------------------------------------------------')
    # logger.debug('Configuring analog input 2 as Single-Ended')
    # logger.debug('-----------------------------------------------------------')
    setting_string = 'analogSetup.srv?anDesc=Irradiance%20%232&anUnit=V&adp=5&anOnLbl=ON&anA1Col=0' \
        '&anOffLbl=OFF&anA2Col=1&anANCol=4&difMd=0&slp=1.00000&off=0.00000&anAlrm1=4.00000' \
        '&anAT1=1&anAlrm2=1.00000&anAT2=0&anDBand=0.50000&anEmailOpt=0&anOAct1=1&anOAlrm1=1' \
        '&ioAnOpt1=1&anOAct2=1&anOAlrm2=1&ioAnOpt2=1&anRRAct1=1&anRRAlrm1=1&ioAnRROpt1=1' \
        '&anRRAct2=1&anRRAlrm2=1&ioAnRROpt2=1&anRRAct3=1&anRRAlrm3=1&ioAnRROpt3=1&anRmtAct=1' \
        '&anRmtAlrm=1&anIoRmtAct=on'
    logger.debug('Analog Input 2: %s' % setting_string)

    r = requests.get(url + 'anachng.srv?aNum=2&anMd=0', auth=auth)
    r = requests.get(url + setting_string, auth=auth)

    assert r.status_code == 200
    time.sleep(1)

    #config analog input 3
    # logger.debug('-----------------------------------------------------------')
    # logger.debug('Configuring analog input 3')
    # logger.debug('-----------------------------------------------------------')
    setting_string = 'analogSetup.srv?anDesc=Cell%20Temp&anUnit=V&adp=2&anOnLbl=ON&anA1Col=1&anOffLbl=OFF' \
        '&anA2Col=1&anANCol=4&difMd=0&slp=1.00000&off=0.00000&anAlrm1=5.00000&anAT1=1&anAlrm2=0.00000' \
        '&anAT2=0&anDBand=0.50000&anEmailOpt=0&anOAct1=1&anOAlrm1=1&ioAnOpt1=1&anOAct2=1&anOAlrm2=1' \
        '&ioAnOpt2=1&anRRAct1=1&anRRAlrm1=1&ioAnRROpt1=1&anRRAct2=1&anRRAlrm2=1&ioAnRROpt2=1&anRRAct3=1' \
        '&anRRAlrm3=1&ioAnRROpt3=1&anRmtAct=1&anRmtAlrm=1&anIoRmtAct=on'
    logger.debug('Analog Input 3: %s' % setting_string)

    r = requests.get(url + 'anachng.srv?aNum=3&anMd=0', auth=auth)
    r = requests.get(url + setting_string, auth=auth)

    assert r.status_code == 200
    time.sleep(1)

    #config analog input 4
    # logger.debug('-----------------------------------------------------------')
    # logger.debug('Configuring analog input 4')
    # logger.debug('-----------------------------------------------------------')
    setting_string = 'analogSetup.srv?anDesc=Wind%20Direction&anUnit=V&adp=2&anOnLbl=ON&anA1Col=1&anOffLbl=OFF' \
        '&anA2Col=1&anANCol=4&difMd=0&slp=1.00000&off=0.00000&anAlrm1=4.00000&anAT1=1&anAlrm2=1.00000' \
        '&anAT2=0&anDBand=0.50000&anEmailOpt=0&anOAct1=1&anOAlrm1=1&ioAnOpt1=1&anOAct2=1&anOAlrm2=1' \
        '&ioAnOpt2=1&anRRAct1=1&anRRAlrm1=1&ioAnRROpt1=1&anRRAct2=1&anRRAlrm2=1&ioAnRROpt2=1&anRRAct3=1' \
        '&anRRAlrm3=1&ioAnRROpt3=1&anRmtAct=1&anRmtAlrm=1&anIoRmtAct=on'
    logger.debug('Analog Input 4: %s' % setting_string)

    r = requests.get(url + 'anachng.srv?aNum=4&anMd=0', auth=auth)
    r = requests.get(url + setting_string, auth=auth)

    assert r.status_code == 200
    time.sleep(1)

    #config DIO1
    # logger.debug('-----------------------------------------------------------')
    # logger.debug('Configuring digital input 1')
    # logger.debug('-----------------------------------------------------------')
    setting_string = 'ioSetup.srv?ioPullup=1&ioDesc=Anemometer&ioOnLbl=ON&ioOnCol=0&ioOffLbl=OFF&ioOffCol=1' \
        '&ioOnbLbl=ON&ioOffbLbl=OFF&ioPbLbl=PULSE&ioPT=1.50000&ioPwrState=1&cOpt=2&idp=2&resetCnt=4000000000' \
        '&ioDb=5&cType=0&ctrDesc=Wind%20Speed&ioUnit=&ioSlp=1.00000&ioOff=0.00000&rateDesc=Frequency&ioRUnit=Hz' \
        '&ioRSlp=1.00000&ioROff=0.00000&ioEmailOpt=0&ioOpt1=1&ioOpt2=1&ioRmtRlyOpt1=1&ioRmtRlyOpt2=1&ioRmtRlyOpt3=1'
    logger.debug('Digital Input 1: %s' % setting_string)

    r = requests.get(url + 'iochng.srv?ioNum=1&ioMd=0', auth=auth)
    r = requests.get(url + setting_string, auth=auth)

    assert r.status_code == 200
    time.sleep(1)

    #config Ambient temp sensor
    # logger.debug('-----------------------------------------------------------')
    # logger.debug('Configuring sensor 1 for Ambient Temperature')
    # logger.debug('-----------------------------------------------------------')
    setting_string = 'sensorSetup.srv?sDesc=Ambient%20Temp&sensAddrS=' + ambient_temp_id + '%s&snA1Col=1&snA2Col=1&snANCol=4&sOff=0.00000' \
        '&sAlrm1=125.00000&sAT1=1&sAlrm2=-55.00000&sAT2=0&sDBand=0.50000&sEmailOpt=0&sOAct1=1&sOAlrm1=1' \
        '&sOAct2=1&sOAlrm2=1&sRRAct1=1&sRRAlrm1=1&sRRAct2=1&sRRAlrm2=1&sRRAct3=1&sRRAlrm3=1&sRmtAct=1&sRmtAlrm=1'
    logger.debug('Digital Input 1: %s' % setting_string)

    r = requests.get(url + 'sensorSetup.html?', auth=auth)
    r = requests.get(url + setting_string, auth=auth)
    assert r.status_code == 200
    time.sleep(1)

    #config control page
    # logger.debug('-----------------------------------------------------------')
    # logger.debug('Configuring control page')
    # logger.debug('-----------------------------------------------------------')
    setting_string = 'controlPageSetup.srv?headerTxt=Draker%20Configured%20X-320&autoRefresh=yes&refreshRate=1&' \
        'dispCnt1=on&dispRRst1=on&dispOOB1=on&dispPB1=on&dispOOB2=on&dispPB2=on&dispS4=on&dispS5=on&dispS6=on' \
        '&dispS7=on&dispS8=on&dispVin=on'
    logger.debug('Control Page: %s' % setting_string)

    r = requests.get(url + setting_string, auth=auth)
    assert r.status_code == 200
    time.sleep(1)

    return True
#---------------------------------------------------------------------------#

if __name__ == '__main__':
    # sys.stdout.write('argv is: %s\n\r' % (sys.argv[1:]))
    parser = argparse.ArgumentParser()
    parser.add_argument('-l','--level', help='defines the logger level to be dispayed to the screen and writen to logger file', default='info')
    parser.add_argument('-lf','--log_filename', help='defines the filename of the logger file', default='c:\\temp\\x320_log.txt')
    parser.add_argument('--ip_address', help='defines the ip address', default='172.28.0.2')
    parser.add_argument('--subnet', help='defines the subnet mask', default='255.255.255.0')
    parser.add_argument('--gateway', help='defines the default gateway', default='172.28.0.1')
    parser.add_argument('--lan_connection_name', help='defines the Network Connection to use', default='Local Area Connection')
    parser.add_argument('ambient_temp_id', help='defines the default gateway', default='78000004DA069A28')
    parser.add_argument('x320_mac', help='defines the default gateway', default='')
    args = parser.parse_args()
    # sys.stdout.write('args is: %s\n\r' % (args))

    # start-up logger
    logger = logging.getLogger('config_X320')

    # setupLogger('debug', 'modbus_log.logger')
    setupLogger(args.level, args.log_filename)

    #timestamp
    localtime = time.asctime(time.localtime(time.time()) )
    logger.info('Script was started on: %s' % localtime)

    logger.info('Using NIC: %s' % args.lan_connection_name)
    logger.info('Assigning IP Address of %s to X-320-I' % args.ip_address)
    logger.info('Assigning Subnet Mask of %s to X-320-I' % args.subnet)
    logger.info('Assigning Default Gateway of %s to X-320-I' % args.gateway)

    # Properly format the MAC Address
    x320_mac = args.x320_mac.replace(':', '-')
    x320_mac = x320_mac.upper()
    logger.info('X320 INPUT MACID: %s', args.x320_mac)

    logger.info('Temp Sensor ROM-ID: %s' % args.ambient_temp_id)

    auth = ('admin', 'webrelay')

    if not establishConnection(args.ip_address, x320_mac, args.lan_connection_name):
        logger.info('Failed to establish connection')
        logger.info('exiting the program')
        sys.exit()

    if not x320MacCheck(auth, args.ip_address, x320_mac):
        logger.info('Failed to MAC Address check')
        logger.info('exiting the program')
        sys.exit()

    if not configX320(auth, args.ip_address, args.subnet, args.gateway, args.ambient_temp_id):
        logger.info('Failed to configure X-320-I')
        logger.info('exiting the program')
    else:
        logger.info('Successfully configured X-320-I')
        logger.info('exiting the program')

    sys.exit()
