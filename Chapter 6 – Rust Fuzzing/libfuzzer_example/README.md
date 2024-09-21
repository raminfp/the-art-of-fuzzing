### Rust fuzzing with libfuzzer


```bash
[dependencies]
libfuzzer-sys = "0.4.0"
```


```bash
#![no_main]

use libfuzzer_sys::fuzz_target;

fuzz_target!(|data: &[u8]| {
    // code to fuzz goes here
});
```

#### Building:
```bash

$ cargo +nightly rustc -- \                                                                                                               101 ⨯
    -C passes='sancov' \
    -C llvm-args='-sanitizer-coverage-level=3' \
    -C llvm-args='-sanitizer-coverage-inline-8bit-counters' \
    -Z sanitizer=address
	
$ ./target/debug/fuzzed

```
