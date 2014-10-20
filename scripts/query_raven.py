#!/usr/bin/env Python

''' Configure Raven XE
'''
# import urllib2
from splinter import Browser

# data = '<body><read><data id="0"/><data id="16384"/><data id="20000"/></read></body>'

# auth_handler = urllib2.HTTPBasicAuthHandler()
# auth_handler.add_password("Modem@AirLink.com", 'msci', 'user', '12345')

# opener = urllib2.build_opener(auth_handler)

# urllib2.install_opener(opener)

# urllib2.urlopen('http://192.168.14.31:8088', data)

browser = Browser('firefox')
browser.visit('http://166.161.64.248:9191')
browser.fill('password', 12345)
browser.find_by_name('Login').click()
# browser.find_by_id('btn_tpl').click()
# browser.attach_file('up.upload-file', 'C:\cygwin\home\jeastman\hardware-config\CommonConfigs\RAVEN_XE_VERIZON.xml')
# browser.find_by_name('lApply').click()
browser.find_by_id('Cont.TopM1.SecurityM1').click()
# browser.fill('3502', 2)



browser.quit()