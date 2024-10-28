#!/usr/bin/env python3
import re

with open('freezingprogram.txt') as f:
    flag = re.findall('holds "(.)"', f.read())

print(''.join(flag))
