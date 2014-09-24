import requests

header = {'Authorization': 'token ded311305ca64ca0d45c649573b84f43a88da3cc'}
url = "https://raw.githubusercontent.com/drakerlabs/project-firmware/master/projects/p2592-01_north-high-school.CR8"

r = requests.get(url, headers=header)

# print r.status_code
print r.text