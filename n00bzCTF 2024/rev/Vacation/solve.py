#!/usr/bin/env python3
with open('./output.txt', 'r') as f:
    print(''.join(list(map(lambda x: chr(ord(x) ^ 3), f.read()))))
