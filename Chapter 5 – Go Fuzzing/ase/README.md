```bash      

┌──(root💀kali)-[~kali/Desktop/golang_fuzzing]
└─# go get github.com/arolek/ase
┌──(root💀kali)-[~kali/Desktop/golang_fuzzing]
└─# cd `go list -f '{{.Dir}}' github.com/arolek/ase`
                                                                                                                                                                                                                                             
┌──(root💀kali)-[~/…/src/github.com/arolek/ase]
└─# git reset --hard b1bf7d7a70445821722b29395f07fcd13e940f8c
HEAD is now at b1bf7d7 fixed readme conflict
                                                                                                                                                                                                                                             
┌──(root💀kali)-[~/…/src/github.com/arolek/ase]
└─# ls
ase.go  ase_test.go  block.go  color.go  group.go  README.md  samples
                                                                                                                                                                                                                                             
┌──(root💀kali)-[~/…/src/github.com/arolek/ase]
└─# nano fuzz.go
                                                                                                                                                                                                                                             
┌──(root💀kali)-[~/…/src/github.com/arolek/ase]
└─# /root/go/bin/go-fuzz-build                               
                                                                                                                                                                                                                                             
┌──(root💀kali)-[~/…/src/github.com/arolek/ase]
└─# /root/go/bin/go-fuzz      
2021/06/15 03:21:51 workers: 4, corpus: 66 (0s ago), crashers: 2, restarts: 1/0, execs: 0 (0/sec), cover: 0, uptime: 3s
2021/06/15 03:21:54 workers: 4, corpus: 67 (2s ago), crashers: 2, restarts: 1/0, execs: 0 (0/sec), cover: 346, uptime: 6s
2021/06/15 03:21:57 workers: 4, corpus: 67 (5s ago), crashers: 2, restarts: 1/140, execs: 76876 (8531/sec), cover: 346, uptime: 9s
2021/06/15 03:22:00 workers: 4, corpus: 67 (8s ago), crashers: 2, restarts: 1/91, execs: 141699 (11807/sec), cover: 346, uptime: 12s
```
