#!/usr/bin/env python3
from pwn import *

r = remote('24.199.110.35', 42189)

r.sendlineafter(b'answer? ', b'-1')

print(r.recv())
