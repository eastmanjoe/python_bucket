import requests
import re
import subprocess
import sys

def input_until_match(msg, re_obj, exptected_length=None):
    val = None
    while val is None:
        val = raw_input(msg)
        if exptected_length:
            if len(val) > exptected_length:
                val = None
                continue
        val = re_obj.match(val)
    return val.group()

re_mac = re.compile('([a-fA-F0-9]{2}[:|\-]?){6}')
re_rom = re.compile('([A-F0-9]{15})')

ip = raw_input("IP of the x320 (172.28.0.2): ")
if not ip:
    ip = '172.28.0.2'
url = 'http://' + ip + '/'
auth = ('admin', 'webrelay')

# ambtmp = input_until_match("Please enter ROM-ID of Ambient Temperature    : ", re_rom, 16)
# pnltmp = input_until_match("Please enter ROM-ID of Panel/Cell Temperature : ", re_rom, 16)

def pg(href):
    return url + href

def get(link):
    return requests.get(link, auth=auth)

try:
    r = get(pg('about.html'))
except:
    print "Unable to locate X320 at", url
    print "Attemping to auto configure ip of the X320..."
    mac = '00:0c:c8:02:bf:2f'
    # mac = input_until_match("Please enter the MAC address of the X-320: ", re_mac, 17)

    if sys.platform == 'Windows':
        mac = mac.replace(':', '-')
        arp = ['netsh', 'interface', 'ipv4', 'add', 'neighbors', 'Local Area Connection', ip, mac]
        ping = ['ping', '-n', '5', '-l', '102', ip]
    else:
        mac = mac.replace('-', ':')
        arp = ['sudo', 'arp', '-s', ip, mac]
        ping = ['ping', '-c', '5', '-s', '102', ip]
        print "Clearing arp cache"
        subprocess.call(['sudo', 'arp', '-d', ip])

    print "Setting arp cache"
    subprocess.call(arp)
    print "Pinging X320"
    subprocess.call(ping)

    r = get(pg('about.html'))

assert r.status_code == 200

r = get(pg('sensorSetup.html'))
assert r.status_code == 200

# if pnltmp not in r.content \
# or ambtmp not in r.content:
    # print "Looks like a temperature sensor is not plugged in"
    # print r.content
    # sys.exit(0)

print "Configuring network configuration"
print "...Setting IP to 172.28.0.2"
print "...Setting subnet mask to 255.255.255.0"
print "...Setting gateway to 172.28.0.1"
print "...Setting speed to 10 Mbps"
print "...Setting mode to Half Duplex"
r = get(pg('networkSetup.srv?dhcpEnbled=no&ip1=172&ip2=28&ip3=0&ip4=2&nm1=255&nm2=255&nm3=255&nm4=0&gw1=172&gw2=28&gw3=0&gw4=1 \
        &pdns1=0&pdns2=0&pdns3=0&pdns4=0&adns1=0&adns2=0&adns3=0&adns4=0&lP=80&nS=ten&nM=half&sA=&msp=25&sUN=&sP=&sndA= \
        &email1=&email2=&email3=&email4=&email5='))
assert r.status_code == 200

print "Setting temperature units to Celsius"
r = get(pg('aboutSetup.srv?units=c'))
assert r.status_code == 200

print "Configuring digital 1 for wind speed sensor"
print "...setting description to wind_speed"
print "...setting units to m/s"
r = get(pg('/ioSetup.srv?ioPullup=1&ioDesc=wind_speed&ioOnLbl=ON&ioOnCol=0&ioOffLbl=OFF&ioOffCol=1&ioOnbLbl=ON&ioOffbLbl=OFF&ioPbLbl=PULSE& \
    ioPT=1.50000&ioPwrState=1&cOpt=2&idp=2&resetCnt=4000000000&ioDb=5&cType=0&ctrDesc=wind_speed&ioUnit=&ioSlp=1.00000&ioOff=0.00000& \
    rateDesc=wind_speed&ioRUnit=&ioRSlp=1.00000&ioROff=0.00000&ioEmailOpt=0&ioOpt1=1&ioOpt2=1&ioRmtRlyOpt1=1&ioRmtRlyOpt2=1&ioRmtRlyOpt3=1&time=1364506276468'))
assert r.status_code == 200

print "Configuring analog 1 for irradiance sensor"
print "...setting description to irradiance"
print "...setting units to W/m2"
print "...setting decimal places to 5"
print "...setting slope multiplier to 1"
r = get(pg('/analogSetup.srv?anDesc=irradiance&anUnit=V&adp=5&anOnLbl=ON&anA1Col=1&anOffLbl=OFF&anA2Col=1&anANCol=4&difMd=1&slp=1.00000& \
    off=0.00000&anAlrm1=0.02500&anAT1=1&anAlrm2=0.00000&anAT2=0&anDBand=0.00100&anEmailOpt=0&anOAct1=1&anOAlrm1=1&ioAnOpt1=1&anOAct2=1& \
    anOAlrm2=1&ioAnOpt2=1&anRRAct1=1&anRRAlrm1=1&ioAnRROpt1=1&anRRAct2=1&anRRAlrm2=1&ioAnRROpt2=1&anRRAct3=1&anRRAlrm3=1& \
    ioAnRROpt3=1&anRmtAct=1&anRmtAlrm=1&anIoRmtAct=on&time=1364507820502'))
assert r.status_code == 200

print "Configuring analog 3 for cell temperature sensor"
print "...setting description to cell_temperature"
print "...setting units to DegC"
print "...setting decimal places to 5"
print "...setting slope multiplier to 1"
r = get(pg('/analogSetup.srv?anDesc=cell_temperature&anUnit=degC&adp=2&anOnLbl=ON&anA1Col=1&anOffLbl=OFF&anA2Col=1&anANCol=4&difMd=0& \
    slp=1.00000&off=0.00000&anAlrm1=5.00000&anAT1=1&anAlrm2=0.00000&anAT2=0&anDBand=0.50000&anEmailOpt=0&anOAct1=1&anOAlrm1=1& \
    ioAnOpt1=1&anOAct2=1&anOAlrm2=1&ioAnOpt2=1&anRRAct1=1&anRRAlrm1=1&ioAnRROpt1=1&anRRAct2=1&anRRAlrm2=1&ioAnRROpt2=1& \
    anRRAct3=1&anRRAlrm3=1&ioAnRROpt3=1&anRmtAct=1&anRmtAlrm=1&anIoRmtAct=on&time=1364507573514'))
assert r.status_code == 200

print "Configuring analog 4 for wind direction sensor"
print "...setting description to wind_direction"
print "...setting units to deg"
print "...setting decimal places to 5"
print "...setting slope multiplier to 1"
r = get(pg('/analogSetup.srv?anDesc=wind_direction&anUnit=deg&adp=2&anOnLbl=ON&anA1Col=1&anOffLbl=OFF&anA2Col=1&anANCol=4&difMd=0& \
    slp=5.00000&off=0.00000&anAlrm1=4.00000&anAT1=1&anAlrm2=1.00000&anAT2=0&anDBand=0.50000&anEmailOpt=0&anOAct1=1&anOAlrm1=1& \
    ioAnOpt1=1&anOAct2=1&anOAlrm2=1&ioAnOpt2=1&anRRAct1=1&anRRAlrm1=1&ioAnRROpt1=1&anRRAct2=1&anRRAlrm2=1&ioAnRROpt2=1& \
    anRRAct3=1&anRRAlrm3=1&ioAnRROpt3=1&anRmtAct=1&anRmtAlrm=1&anIoRmtAct=on&time=1364507534821'))
assert r.status_code == 200

print "Configuring control page"
r = get(pg('/controlPageSetup.srv?headerTxt=X-320&autoRefresh=yes&refreshRate=1&dispCnt1=on&dispOOB1=on&dispPB1=on&dispOOB2=on&dispPB2=on& \
    dispS4=on&dispS6=on&dispS7=on&dispS8=on&time=1364507953877 '))
assert r.status_code == 200

# def get_tmp_id(content, romid):
#     tmp_id = None
#     text = content[:content.index(romid)]
#     for c in reversed(text):
#         try:
#             tmp_id = int(c)
#             break
#         except:
#             pass
#     return tmp_id

# r = get(pg('senschng.srv?sNum=1'))
# assert r.status_code == 200
# tmp_id = get_tmp_id(r.content, ambtmp)

# print "Configuring sensor 1 for Ambient Temperature"
# print "...setting sensor address", tmp_id, "->", ambtmp
# r = get(pg('sensorSetup.srv?sDesc=AmbientTemp&sensAddrS='+str(tmp_id)+'&snA1Col=0&snA2Col=1&snANCol=4&sAlrm1=-15.555&sAT1=1&sAlrm2=-17.222&sAT2=0&sDBand=0.899&sEmailOpt=0&sOAct1=1&sOAlrm1=1&sOAct2=1&sOAlrm2=1&sRRAct1=1&sRRAlrm1=1&sRRAct2=1&sRRAlrm2=1&sRRAct3=1&sRRAlrm3=1&sRmtAct=1&sRmtAlrm=1'))
# assert r.status_code == 200

# r = get(pg('senschng.srv?sNum=2'))
# assert r.status_code == 200
# tmp_id = get_tmp_id(r.content, pnltmp)

# print "Configuring sensor 2 for Panel/Cell Temperature"
# print "...setting sensor address", tmp_id, "->", pnltmp
# r = get(pg('sensorSetup.srv?sDesc=PanelTemp&sensAddrS='+str(tmp_id)+'&snA1Col=0&snA2Col=1&snANCol=4&sAlrm1=-15.555&sAT1=1&sAlrm2=-17.222&sAT2=0&sDBand=0.899&sEmailOpt=0&sOAct1=1&sOAlrm1=1&sOAct2=1&sOAlrm2=1&sRRAct1=1&sRRAlrm1=1&sRRAct2=1&sRRAlrm2=1&sRRAct3=1&sRRAlrm3=1&sRmtAct=1&sRmtAlrm=1'))
# assert r.status_code == 200

print "X-320 should now be configured!"
