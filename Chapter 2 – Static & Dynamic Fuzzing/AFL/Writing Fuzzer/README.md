# Fuzzing process


1- Start target binary, but break on first instruction before anything runs

2- Set breakpoints on a ‘start’ and ‘end’ location (start will be after the program reads in bytes from the file on disk, end will be the address of exit())

3- Run the program until it hits the ‘start’ breakpoint

4- Collect all writable memory sections of the process in a buffer

5- Capture all register states

6- Insert our fuzzcase into the heap overwriting the bytes that the program read in from file on disk

7- Resume target binary until it reaches ‘end’ breakpoint

8- Rewind process state to where it was at ‘start’

9- Repeat from step 6



Ref : https://h0mbre.github.io/Fuzzing-Like-A-Caveman-4/#
