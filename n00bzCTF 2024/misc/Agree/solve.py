#!/usr/bin/env python3
import re
import requests

flag = ''
response = requests.get('https://ctf.n00bzunit3d.xyz/tos')

flag += re.search('flag: ([A-Za-z0-9_{}]+)', response.text).group(1)

response = requests.get('https://ctf.n00bzunit3d.xyz/privacy')

flag += re.search('flag: ([A-Za-z0-9_{}]+)', response.text).group(1)

print(flag)