import urllib2

data = '<body><read><data id="0"/><data id="16384"/><data id="20000"/></read></body>'

auth_handler = urllib2.HTTPBasicAuthHandler()
auth_handler.add_password("Modem@AirLink.com", 'msci', 'user', '12345')

opener = urllib2.build_opener(auth_handler)

urllib2.install_opener(opener)

urllib2.urlopen('http://192.168.14.31:8088', data)