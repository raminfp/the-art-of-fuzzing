#![no_main]

use libfuzzer_sys::fuzz_target;
use rustc_demangle::demangle;

fuzz_target!(|data: &[u8]| {
   
	 // code to fuzz goes here
	if let Ok(data) = std::str::from_utf8(data) {
        	let _ = demangle(data).to_string();
   	 }

});
