import requests

header = {'Authorization': 'token'}
url = "https://raw.githubusercontent.com/drakerlabs/project-firmware/master/projects/p2592-01_north-high-school.CR8"

r = requests.get(url, headers=header)

# print r.status_code
print r.text