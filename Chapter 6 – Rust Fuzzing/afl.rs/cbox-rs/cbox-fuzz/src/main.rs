extern crate cbox;

use cbox::CBox;
#[macro_use]
extern crate afl;
use afl::fuzz;
fn main() {

    fuzz!(|data: &[u8]| {
	if let Ok(s) = std::str::from_utf8(data) {
		let _text = CBox::from(s);

	}
    });

//    unsafe {
        //let text = CBox::from("Hello, world!");
        //steal_print(text.unwrap());
//    }
}
