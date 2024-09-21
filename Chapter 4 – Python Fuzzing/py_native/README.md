### Fuzzing python native code

### How to build :
```bash
CC="/usr/bin/clang" \ 
	CFLAGS="-fsanitize=address" \
	LDSHARED="clang -shared" \
	python3.9 ./setup.py install
```

### LibFuzzer.so Path :
```bash 
LD_PRELOAD="$(python3.9 -c "import atheris; import os; print(os.path.dirname(atheris.path()))")/asan_with_fuzzer.so" python3.9
```


### Sampel:
```bash
import vuln

vuln.overflow(b"AAAAAAAAAAA","hello.txt")
```