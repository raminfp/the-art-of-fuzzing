#### Intro KLEE


```bash
$ git clone https://github.com/klee/klee.git
$ cd klee
$ docker build -t klee/klee .
$ docker run --rm -ti --ulimit='stack=-1:-1' klee/klee
```

```bash
$ clang -emit-llvm -O0 -c -g first_exm.c
$ llvm-dis ./test.bc
$ vim test.ll
$ klee test.bc

$ ls klee-out-0/*.err
$ $ ktest-tool klee-last/test000621.ktest 

```


https://mukulrathi.co.uk/create-your-own-programming-language/llvm-ir-cpp-api-tutorial/ <br />
https://egorbo.com/opt-for-llvm-guide.html <br />
https://godbolt.org/z/3D2jmd <br />
https://0xpat.github.io/Malware_development_part_6/ <br />
https://releases.llvm.org/2.5/docs/tutorial/JITTutorial2.html <br />
https://www.politoinc.com/post/2020/03/02/Automated-Obfuscation-of-Windows-MalwareExploits-Using-O-LLVM <br />
https://blog.gopheracademy.com/advent-2018/llvm-ir-and-go/ <br />
