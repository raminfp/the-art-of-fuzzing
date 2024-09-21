# Fuzzing popular Rust library in 5 min using cargo-fuzz / libfuzzer

## Install cargo-fuzz
``` sh
cargo +nightly install cargo-fuzz
```

## Clone humantime project
``` sh
git clone https://github.com/tailhook/humantime
```

## cargo-fuzz commands
``` sh
cargo fuzz init #initialize the fuzzing folder
cargo fuzz list # list the available targets
cargo fuzz run fuzz_target_1 # Run fuzzing of fuzz/fuzz_targets/fuzz_target_1.rs 
```

