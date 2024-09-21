#[macro_use]
extern crate afl;
use afl::fuzz;

fn main() {
    fuzz!(|data: &[u8]| {
	if let Ok(s) = std::str::from_utf8(data) {
		parse_duration::parse(s);
	}
    });
}
