from pwn import *

context.log_level = 'debug'

r = remote('34.69.226.63', 30963)

for i in range(100):
    r.recvuntil(b'test >  ')

    word = r.recvuntil(b' ').strip()

    r.sendlineafter(b'words > ', word)

r.interactive()