#!/usr/bin/env python3
import random

random.seed(1337)

flag = []
ops = [
    lambda x: x - 3,
    lambda x: x + 3,
    lambda x: x // 3,
    lambda x: x ^ 3,
]

with open('out.txt', 'r') as f:
    ct = eval(f.readline())

    for c in ct:
        flag.append(chr(random.choice(ops)(c)))

    print(''.join(flag))
