# Fuzzing Rust code using honggfuzz

## Install honggfuzz-rs

link: https://github.com/rust-fuzz/honggfuzz-rs

``` sh
$ sudo apt install build-essential binutils-dev libunwind-dev libblocksruntime-dev liblzma-dev

# installs hfuzz and honggfuzz subcommands in cargo
$ cargo install honggfuzz
```

## Choose your target (ical-rs)

Link: https://crates.io/crates/ical
Doc: https://docs.rs/ical/0.7.0/ical/
Github: https://github.com/Peltoche/ical-rs

Interesting methods:
- ical::parser::ical [doc](https://docs.rs/ical/0.7.0/ical/parser/ical/index.html)
- ical::parser::vcard [doc](https://docs.rs/ical/0.7.0/ical/parser/vcard/index.html)

## Create your fuzz target

ical-rs code example: https://docs.rs/ical/0.7.0/ical/parser/ical/index.html#examples

honggfuzz-rs target example: https://github.com/rust-fuzz/honggfuzz-rs/blob/master/example/src/main.rs

`src/bin/ical_parser.rs`:
``` rust
#[macro_use]
extern crate honggfuzz;
extern crate ical;

use std::io::BufReader;

fn main() {
    loop {
        fuzz!(|data: &[u8]| {
            let buf = BufReader::new(data);
            let reader = ical::IcalParser::new(buf);

            for line in reader {
                println!("{:?}", line);
            }
        });
    }
}
```

## Run the fuzzer

``` sh
$ cargo hfuzz run ical_parser # Run fuzzing of src/bin/ical_parser
$ cargo hfuzz run vcard_parser # Run fuzzing of src/bin/vcard_parser
```

## Debug the crash

``` sh
$ cargo hfuzz run-debug ical_parser crash_ical_unwrap.input

thread 'main' panicked at 'called `Result::unwrap()` on an `Err` value: Custom { kind: InvalidData, error: "stream did not contain valid UTF-8" }', /home/scop/.cargo/registry/src/github.com-1ecc6299db9ec823/ical-0.7.0/src/line.rs:120:33
stack backtrace:
   0: rust_begin_unwind
             at /rustc/2fd73fabe469357a12c2c974c140f67e7cdd76d0/library/std/src/panicking.rs:493:5
   1: core::panicking::panic_fmt
             at /rustc/2fd73fabe469357a12c2c974c140f67e7cdd76d0/library/core/src/panicking.rs:92:14
   2: core::option::expect_none_failed
             at /rustc/2fd73fabe469357a12c2c974c140f67e7cdd76d0/library/core/src/option.rs:1300:5
   3: core::result::Result<T,E>::unwrap
             at /rustc/2fd73fabe469357a12c2c974c140f67e7cdd76d0/library/core/src/result.rs:1037:23
   4: <ical::line::LineReader<B> as ical::line::LineRead>::next_line
             at /home/scop/.cargo/registry/src/github.com-1ecc6299db9ec823/ical-0.7.0/src/line.rs:120:28
   5: <ical::line::LineReader<B> as core::iter::traits::iterator::Iterator>::next
             at /home/scop/.cargo/registry/src/github.com-1ecc6299db9ec823/ical-0.7.0/src/line.rs:163:9
   6: <ical::property::PropertyParser<B> as core::iter::traits::iterator::Iterator>::next
             at /home/scop/.cargo/registry/src/github.com-1ecc6299db9ec823/ical-0.7.0/src/property.rs:280:9
   7: ical::parser::ical::IcalParser<B>::check_header
             at /home/scop/.cargo/registry/src/github.com-1ecc6299db9ec823/ical-0.7.0/src/parser/ical/mod.rs:64:26
   8: <ical::parser::ical::IcalParser<B> as core::iter::traits::iterator::Iterator>::next
             at /home/scop/.cargo/registry/src/github.com-1ecc6299db9ec823/ical-0.7.0/src/parser/ical/mod.rs:85:15
   9: ical_parser::main::{{closure}}
             at ./src/bin/ical_parser.rs:13:25
  10: honggfuzz::fuzz
             at /home/scop/.cargo/registry/src/github.com-1ecc6299db9ec823/honggfuzz-0.5.54/src/lib.rs:316:5
  11: ical_parser::main
             at ./src/bin/ical_parser.rs:9:9
  12: core::ops::function::FnOnce::call_once
             at /rustc/2fd73fabe469357a12c2c974c140f67e7cdd76d0/library/core/src/ops/function.rs:227:5
note: Some details are omitted, run with `RUST_BACKTRACE=full` for a verbose backtrace.
f
```

Bug is here: https://github.com/Peltoche/ical-rs/blob/a8b9c8202281b2b3d7c4484bf2eda719d9e19d06/src/line.rs#L120

