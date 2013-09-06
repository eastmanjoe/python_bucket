import httplib
import urllib

# params = urllib.urlencode({'@number': 12524, '@type': 'issue', '@action': 'show'})
# headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
# conn = httplib.HTTPConnection("bugs.python.org")
conn = httplib.HTTPConnection(192.168.13.31)
conn.request("POST", "", params, headers)
response = conn.getresponse()

print response.status, response.reason

data = response.read()
conn.close()