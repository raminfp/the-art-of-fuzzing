### Cargo-fuzz

##### Install Rust (Ubuntu):

```bash

	$ curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
	
	$ rustup toolchain install nightly
```


##### Install afl.rs :
```bash
	$ cargo install afl
	$ cargo afl build
	$ mkdir in
	$ echo "tcp://example.com/" > in/url
	$ echo "ssh://192.168.1.1" > in/url2
	$ cargo afl fuzz -i in -o out target/debug/fuzz-target
```