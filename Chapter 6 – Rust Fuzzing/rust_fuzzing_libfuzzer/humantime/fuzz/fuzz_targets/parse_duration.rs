#![no_main]
use libfuzzer_sys::fuzz_target;

use humantime::parse_duration;

fuzz_target!(|data: &[u8]| {
    // fuzzed code goes here
    if let Ok(s) = std::str::from_utf8(data) {
        let _ = parse_duration(s);
    };
});
