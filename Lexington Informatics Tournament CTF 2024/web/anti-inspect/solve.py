#!/usr/bin/env python3
import re
import requests

response = requests.get('http://litctf.org:31779/')

print(re.search('LITCTF{.+}', response.text).group(0).replace('%c', ''))
