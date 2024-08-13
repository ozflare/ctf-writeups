#!/usr/bin/env python3
from Crypto.Util.number import *
from pwn import *
import gmpy2

p = remote('third-times-the-charm.ctf.umasscybersec.org', 1337)

p.recvuntil(b'm1: ')
m1 = int(p.recvline().strip().decode())

p.recvuntil(b'N1: ')
N1 = int(p.recvline().strip().decode())

p.recvuntil(b'm2: ')
m2 = int(p.recvline().strip().decode())

p.recvuntil(b'N2: ')
N2 = int(p.recvline().strip().decode())

p.recvuntil(b'm3: ')
m3 = int(p.recvline().strip().decode())

p.recvuntil(b'N3: ')
N3 = int(p.recvline().strip().decode())

n = N1 * N2 * N3

n1 = n // N1
n2 = n // N2
n3 = n // N3

d1 = pow(n1, -1, N1)
d2 = pow(n2, -1, N2)
d3 = pow(n3, -1, N3)

x = ((m1 * n1 * d1) + (m2 * n2 * d2) + (m3 * n3 * d3)) % n
print(long_to_bytes(gmpy2.iroot(x, 3)[0]))
