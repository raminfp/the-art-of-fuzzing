#!/usr/bin/env python3
#
############################################################################
# Coldsnap is a "Hello World" example of a snapshot fuzzer built in python #
############################################################################
#
# Author: Evan Custodio
#
# Copyright 2020 Evan Custodio
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the Software
#  is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
import os
import subprocess
import signal
import ctypes
import random
from ptrace.debugger.child import createChild
from ptrace.debugger import PtraceDebugger
from ptrace.debugger import Breakpoint
from time import sleep
import datetime

### We define a couples ctypes structures and functions from libc
### to allow for writing and reading target process memory
class iovec(ctypes.Structure):
    _fields_=[("iov_base",ctypes.c_void_p),("iov_len",ctypes.c_int)]

### Open libc
libc = ctypes.CDLL('libc.so.6')
# read / write remote memory
readv=libc.process_vm_readv
writev=libc.process_vm_writev
# get errno for debug
get_errno_loc = libc.__errno_location
get_errno_loc.restype = ctypes.POINTER(ctypes.c_int)

# Our read process memory function, caller must provide the buffer
def read_process_memory(pid, address, size, bytes_buffer):
    local_iovec  = iovec(ctypes.cast(ctypes.byref(bytes_buffer), ctypes.c_void_p), size)
    remote_iovec = iovec(ctypes.c_void_p(address), size)
    bytes_transferred = readv(pid, ctypes.byref(local_iovec), 1, ctypes.byref(remote_iovec), 1, 0)
    #if (bytes_transferred == -1):
    #    print ("Read_Process_Memory: " + os.strerror(get_errno_loc()[0]))  
    return bytes_transferred

# Our simple read process memory function, caller need not provide a buffer
def read_bytes(pid, address, size):
    buf = ctypes.create_string_buffer(b'\x00'*(size-1))
    read_process_memory(pid, address, size, buf)
    return buf.raw

# Our write process memory function, caller must provide the buffer        
def write_process_memory(pid, address, size, bytes_buffer):
    local_iovec  = iovec(ctypes.cast(ctypes.byref(bytes_buffer), ctypes.c_void_p), size)
    remote_iovec = iovec(ctypes.c_void_p(address), size)
    bytes_transferred = writev(pid, ctypes.byref(local_iovec), 1, ctypes.byref(remote_iovec), 1, 0)
    #if (bytes_transferred == -1):
    #    print ("Write_Process_Memory: " + os.strerror(get_errno_loc()[0]))  
    return bytes_transferred

# Our simple write process memory function, caller need not provide a buffer, bytes type is OK
def write_bytes(pid, address, data):
    buf = ctypes.create_string_buffer(data)
    write_process_memory(pid, address, len(data), buf)

# Execute a command in a subshell and return its stdout    
def execute(cmd):
    out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    return out
    
# Helper function for fatals
def FATAL(msg):
    print("FATAL: " + msg)
    exit(1)

# This class handles memory space snapshotting for given ProcessID
class SnapshotManager(object):
    # Each memory space is encapsulated in a Snapshot class
    class Snapshot(object):
        def __init__(self, pid, startaddr, endaddr, permissions, offset, device, inode, name):
            self.pid         = pid
            self.startaddr   = startaddr
            self.endaddr     = endaddr
            self.size        = self.endaddr - self.startaddr
            self.permissions = permissions
            self.offset      = offset
            self.device      = device
            self.inode       = inode
            self.name        = name
            self.localsave   = None
            self.writable    = True
            
        def locate(self, payload):
            if (self.localsave == None):
                FATAL("cannot search snapshot, no snapshot exists")

            loc = self.localsave.raw.find(payload)
            if loc == -1:
                return -1
            return self.startaddr + loc
            
        def save(self):
            # If we dont have local memory allocated for this memory, allocate it
            if (self.localsave == None):
                self.localsave = ctypes.create_string_buffer(b'\x00'*self.size)
            # cache a local copy of this memory region
            read_process_memory(self.pid, self.startaddr, self.size, self.localsave)
            
        def load(self):
            # If this was found not writeable then return
            if (not self.writable):
                return
            # If we dont have local memory allocated for this memory, error
            if (self.localsave == None):
                FATAL("cannot load snapshot, no snapshot exists")
            # push the local copy of this memory region to the remote process
            if (write_process_memory(self.pid, self.startaddr, self.size, self.localsave) == -1):
                self.writable = False
            
    def __init__(self, process):
        self._pid = process.pid
        self._process = process
        self._mappath = "/proc/%d/maps" % process.pid
        try:
            with open(self._mappath) as f:
                self._rawmap = f.read()
        except:
            FATAL("Error opening %s"%(self._mappath))
            
        self._parse()
    
    # Internal function which parses /proc/id/maps and poplulates a list of memory spaces inside the object
    def _parse(self):
        rawmap = self._rawmap
        lines = rawmap.split("\n")
        self._memspaces = []
        
        # Parse all memory maps for the target process
        for line in lines:
            if line == "":
                continue
            memspace = {}
            columns = line.split()
                
            # Populate all the fields
            startaddr   = int(columns[0].split('-')[0],16)
            endaddr     = int(columns[0].split('-')[1],16)
            permissions = columns[1]
            offset      = int(columns[2],16)
            device      = columns[3]
            inode       = int(columns[4])
            name        = None if (len(columns) < 6) else columns[5]
            
            # Create a snapshot instance and add it to the memspaces list
            self._memspaces += [SnapshotManager.Snapshot(self._pid, startaddr, endaddr, permissions, offset, device, inode, name)]
            
    ### This function returns all memory spaces in a list     
    def get_memspaces(self):
        return self._memspaces
    
    ### This function returns all memory spaces in a list that have r/w set
    def get_rw_memspaces(self):
        ret = []
        for sn in self._memspaces:
            if sn.permissions[0:2] == "rw":
                ret += [sn]
        return ret
        
    ### This function returns all memory spaces in a list that have x set
    def get_x_memspaces(self):
        ret = []
        for sn in self._memspaces:
            if sn.permissions[2] == 'x':
                ret += [sn]
        return ret

    def savestate(self):
        ### Get all memspaces that are read/write
        memspaces = self.get_rw_memspaces()
        ### For those memspaces, save a local snapshot of memory
        for sn in memspaces:
            sn.save()
        ### Also get a local snapshot of the register state
        self._regs = self._process.getregs()
        
    ### This function is used to find a payload in all read/write memory.
    ### This is useful for locating the input buffer in memory
    def locate(self, payload):
        ### Get all memspaces that are read/write
        memspaces = self.get_rw_memspaces()
        for sn in memspaces:
            pos = sn.locate(payload)
            # return the virtual address of the start of the payload
            if (pos != -1):
                return pos
        return -1

    def loadstate(self):
        ### Get all memspaces that are read/write
        memspaces = self.get_rw_memspaces()
        
        ### load their snapshot state
        for sn in memspaces:
            sn.load()
            
        ### Set the snapshot register state
        self._process.setregs(self._regs)

### Breakpoint add helper function
def add_breakpoint(process, addr):
    return process.createBreakpoint(addr)

### Breakpoint remove helper function    
def delete_breakpoint(bp):
    bp.desinstall(set_ip=True)
    
### Basically we find and return the number of breakpoints
### removed and the total number of breakpoints tracked
def GetCoverage(covbps):
    addrs = list(covbps.keys())
    total = len(addrs)
    cover = 0
    for bpaddr in addrs:
        if covbps[bpaddr] == None:
            cover += 1
    return (cover, total)

def SetupTarget():
    ### Let step up our debugger, fork our target
    ### and attach the debugger to the target
    dbg = PtraceDebugger()
    print("Forking the target...")
    pid = createChild(target.targetArgs, no_stdout=True)
    print("Attaching to the target process %d" % pid)
    process = dbg.addProcess(pid, True)
    return process

    
def CreateInitialState(process, snapshot):
    
    ### Find the first executable memory space (we are assuming its .text)
    textmem = None
    for memspace in snapshot.get_x_memspaces():
        if target.name in memspace.name:
            textmem = memspace
    if textmem == None:
        FATAL("cannot find executable memory space")
    
    ### Next lets find out snapshot start and end points
    try:
        startpoint = int(execute("nm ./%s | grep %s"%(target.name, target.startpoint)).split()[0],16)
        endpoint   = int(execute("nm ./%s | grep %s"%(target.name, target.endpoint)).split()[0],16)
    except:
        FATAL("Error finding the snapshot start/end addresses")
    
    ### Lets replace the symbolic start / end points with their virtual addresses
    target.startpoint = startpoint - textmem.offset + textmem.startaddr
    target.endpoint = endpoint - textmem.offset + textmem.startaddr
    
    ### Next we disassmble .text to look for all valid breakpoint locations
    output = execute("objdump  -d -j .text %s"%(target.name)).decode()
    lines = output[output.find(".text:")+6:].replace('\n\n','\n').split('\n')
    
    ### This is a bit of a hacky way to parse out breakpoint locations (sorry!)
    for line in lines:
        if line == "": continue
        if line[-1] == ":": continue
        items = line.split()
        bpaddr = int(items[0][0:-1],16) - textmem.offset + textmem.startaddr
        ### Add potential breakpoints to our coverage
        target.coverage_bps[bpaddr] = None

    ### Add gratuitous breakpoint across all of .text
    for bpaddr in list(target.coverage_bps.keys()):
        target.coverage_bps[bpaddr] = add_breakpoint(process, bpaddr)
        
    print("Applied %s breakpoints for coverage guidance"%(len(list(target.coverage_bps.keys()))))
    
    ### Next we run our process to the startpoint breakpoint
    ### Remove any other breakpoints along the way
    while (1):
        process.cont()
        ### Catch the next event
        event = process.waitEvent()
        inst = process.getInstrPointer()
        if (event.name != "SIGTRAP"):
            FATAL("Expecting SIGTRAP but got %s @ 0x%x"%(event.name, inst))
            
        ### We hit a breakpoint, remove it
        delete_breakpoint(target.coverage_bps[inst-1])
        target.coverage_bps[inst-1] = None
        
        ### We finally made it to startpoint! break out the loop
        if ((inst-1) == target.startpoint):
            break

    ### Save program state
    snapshot.savestate()
    
    ### Search for the payload address across the entire target memory space
    ptr = snapshot.locate(target.payload)
    if ptr == -1:
        FATAL("cannot find payload in target memory")

    ### Keep note of the memory location for the payload
    target.payloadptr = ptr
    
def Fuzz(process):
    ### Select a random corpus and mutate it
    if (len(target.corpus)):
        corpus = bytearray(random.choice(target.corpus))
    else:
        # Or start with a blank slate if no corpus exists
        corpus = bytearray(b" "*16)
    
    ### Lets do 2 byte flips
    index0 = random.randint(0,len(corpus)-1)
    byte0 = random.randint(0,255)
    index1 = random.randint(0,len(corpus)-1)
    byte1 = random.randint(0,255)

    ### Mutate!
    corpus[index0] = byte0
    corpus[index1] = byte1
    
    ### keep record of the mutation
    target.mutation = bytes(corpus)
    
    ### Insert the fuzz case into target memory
    write_bytes(process.pid, target.payloadptr, target.mutation)

    ### Run Proccess from the startpoint address to process the fuzz case
    process.cont()
    
    
def CheckFuzzResult(process):
    #print ("enter")
    while 1:
        ### Catch the next event
        event = process.waitEvent()

        if (event.name == "SIGTRAP"):
            # Grab the break location (RIP is always 1 byte past it)
            bpAddr = process.getInstrPointer()-1
            
            # If we hit a non endpoint bp, update coverage
            if (bpAddr != target.endpoint):
                # Remove the breakpoint
                delete_breakpoint(target.coverage_bps[bpAddr])
                target.coverage_bps[bpAddr] = None

                # Add this mutation to the corpus pool if it doesn't already exist
                if target.mutation not in target.corpus:
                    target.corpus += [target.mutation]
                    # Print our mutation each time we hit new coverage and expanded corpus
                    print ("New Corpus: " + str(target.mutation))
                
                # Loop to the next event in hopes to reach the endpoint
                process.cont()
                continue
            else:
                # OK, we are at the endpoint. Nothing to do, 
                # lets break out and return to the main fuzz loop
                break
        else:
            # Potential Crash, grab the RIP
            rip = process.getInstrPointer()
            # If we seen this crash before break out to the main fuzz loop
            if rip in target.crashes:
                break
            # Otherwise, this is a new unique crash, make record of it
            target.crashes += [rip]
                
            print("\nCRASH! (%s @ 0x%x) - Payload: %s\n"%(event.name, rip, target.mutation))    
            
            # Did we find all 2 crashes in target? exit if so (target specific)
            if len(target.crashes) >= 2:
                target.endtime = datetime.datetime.now()
                print(f'{"Total Fuzz Cases:": <32}%d' % (target.cases))
                delta = target.endtime - target.starttime
                print(f'{"Duration:": <32}%s seconds' % (delta.total_seconds() ))
                cov = GetCoverage(target.coverage_bps)
                print(f'{"Instructions Covered:": <32}%d / %d (%0.1f%%)' % (cov[0],cov[1],(cov[0]/cov[1])*100))
                print(f'{"Fuzz Cases per Second:": <32}%F' % (target.cases/delta.total_seconds() ))
                exit(0)
            
            # There are still more crashes to find
            print("Continuing to fuzz...")
            break


### This global structure is target specific, It contains the start and end points
### of our snapshot fuzzer, our target location and arguments, our coverage and
### corpus cache   
class target:
    startpoint   = "startf"  # our symbol name for startpoint (will get replaced with virtual address)
    endpoint     = "endf"    # our symbol name for endpoint (will get replaced with virtual address)
    name         = "target"  # our target name
    payload      = b'----------------'
    targetArgs   = [b'./'+name.encode() ,payload]
    payloadptr   = 0x0
    mutation     = b'----------------'
    corpus       = []
    cases        = 0
    starttime    = None
    endtime      = None
    crashes      = []
    coverage_bps = {}
    
if __name__ == "__main__":

    print ("coldsnap.py - A python-based snapshot-based ptrace-based fuzzer example")
    print ("Author      - @defparam (Evan Custodio)\n")

    ### We fork our target using ptrace
    process = SetupTarget()
    
    ### Next we prepare our Snapshot Manager
    snapshot = SnapshotManager(process)
    
    ### Next we apply breakpoints for coverage,
    ### run the target to the startpoint,
    ### and create a snapshot
    CreateInitialState(process, snapshot)
    
    ### At this point CreateInitialState places the
    ### target process in a halted state at startpoint
    ### with program and register state saved
   
    print ("\nStarting Snapshot Fuzzer...\n")
    target.starttime = datetime.datetime.now()
    print ("Corpus discovery coverage growth:")
    
    ### Behold, our "tight" fuzzer loop
    while (1):
        ### Track our fuzz case
        target.cases += 1
    
        ### Fuzz the target with a mutated payload
        Fuzz(process)
        
        ### Check the status of fuzz event and update coverage
        CheckFuzzResult(process)
        
        ### Rewind state back to the start point
        snapshot.loadstate()
   
