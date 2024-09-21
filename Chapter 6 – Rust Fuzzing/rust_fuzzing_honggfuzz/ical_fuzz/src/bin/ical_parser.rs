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
