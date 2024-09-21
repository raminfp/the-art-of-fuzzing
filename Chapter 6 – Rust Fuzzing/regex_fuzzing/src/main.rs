use honggfuzz::fuzz;

//extern crate regex;
use regex::Regex;

fn main() {
    
    loop {
    
        fuzz!(|data: &[u8]| {

		// let re = Regex::new(data);	
		if let Ok(data) = std::str::from_utf8(data) {
        	let _ = Regex::new(data);
   	 }

        });
    }
}
