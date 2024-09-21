use honggfuzz::fuzz;
extern crate libinjection;

use libinjection::{sqli};

fn main() {

	loop {

 		fuzz!(|data: &[u8]| {
        		if let Ok(s) = std::str::from_utf8(data) {
                //let data = object!{
                //"foo" => s,
                //};
                //let _is_xss_2 = xss(s).unwrap();
                let _is_sql = sqli(s).unwrap();
        	}
    	});



    }

}
