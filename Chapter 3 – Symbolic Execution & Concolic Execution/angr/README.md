### Agnr Usage example

```bash
>>> import angr
>>> proj = angr.Project('/bin/true')
WARNING | 2021-06-06 02:28:21,316 | cle.loader | The main binary is a position-independent executable. It is being loaded with a base address of 0x400000.
>>> proj.arch
<Arch AMD64 (LE)>
>>> proj.entry
4203456
>>> proj.filename
'/bin/true'
>>> proj.loader
<Loaded true, maps [0x400000:0xa07fff]>
>>> proj.loader.main_object.execstack
False
>>> block = proj.factory.block(proj.entry)
>>> block.pp()
0x4023c0:       xor     ebp, ebp
0x4023c2:       mov     r9, rdx
0x4023c5:       pop     rsi
0x4023c6:       mov     rdx, rsp
0x4023c9:       and     rsp, 0xfffffffffffffff0
0x4023cd:       push    rax
0x4023ce:       push    rsp
0x4023cf:       lea     r8, [rip + 0x34ba]
0x4023d6:       lea     rcx, [rip + 0x3453]
0x4023dd:       lea     rdi, [rip - 0xe4]
0x4023e4:       call    qword ptr [rip + 0x7bf6]
>>> block.instructions  
11
>>> block.instruction_addrs 
[4203456, 4203458, 4203461, 4203462, 4203465, 4203469, 4203470, 4203471, 4203478, 4203485, 4203492]
>>> proj.loader.all_objects
[<ELF Object true, maps [0x400000:0x40a377]>, <ELF Object libc-2.31.so, maps [0x500000:0x6c4507]>, <ELF Object ld-2.31.so, maps [0x700000:0x72c177]>, <ExternObject Object cle##externs, maps [0x800000:0x87ffff]>, <ELFTLSObjectV2 Object cle##tls, maps [0x900000:0x91500f]>, <KernelObject Object cle##kernel, maps [0xa00000:0xa07fff]>]
>>> proj.loader.shared_objects
OrderedDict([('true', <ELF Object true, maps [0x400000:0x40a377]>), ('libc.so.6', <ELF Object libc-2.31.so, maps [0x500000:0x6c4507]>), ('ld-linux-x86-64.so.2', <ELF Object ld-2.31.so, maps [0x700000:0x72c177]>), ('extern-address space', <ExternObject Object cle##externs, maps [0x800000:0x87ffff]>), ('cle##tls', <ELFTLSObjectV2 Object cle##tls, maps [0x900000:0x91500f]>)])
>>> obj = proj.loader.main_object
>>> addr = obj.plt['strcmp']
>>> addr
4202864
>>> addr = obj.reverse_plt[addr]
>>> addr
'strcmp'
>>> 
```

