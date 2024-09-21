
//////////////////////////////// Error
//fn print(input_string: str) {
// 	println!("{}", input_string);
//}

//fn main() {
// 	let test_string = "Hello, World!";
// 	print(test_string);
//}

///////////////////////////////// OK

//fn print(input_string: String) {
// 	println!("{}", input_string);
//}
//fn main() {
//	let test_string = String::from("Hello, World!");
// 	print(test_string);
//}


////////////////////////////////// OK

//fn print(input_string: &str) {
// 	println!("{}", input_string);
//}
//fn main() {
// 	let test_string = &"Hello, World!";
// 	print(test_string);
//}

///////////////////////////////// 

//fn main() {

	//let _number: u8 = 255;
	//let _number: u8 = 256;

//	let _float: f32 = 20.6;

//}

//////////////////////////////////

//use std::collections::HashMap;

//fn main() {
//	let mut general_map: HashMap<&str, i8> = HashMap::new();
// 	general_map.insert("test", 25);
	////////////// error
 	//let outcome: i8 = general_map.get("test");
 	//println!("{}", outcome);

	////////////// ok
	//let outcome: Option<&i8> = general_map.get("test");
	//println!("here is the outcome {}", outcome.unwrap());

	///////////// ok 	
	//match general_map.get("test") {
 	//	None => println!("it failed"),
 	//	Some(result) => println!("Here is the result: {}", result)
	//}

//	match general_map.get("testing") {
// 		None => {
// 			match general_map.get("test") {
// 				None => println!("Both testing and test failed"),
// 				Some(result) => println!("testing failed but test is: {}", result)
//			}

//			},
//	       Some(result) => println!("Here is the result: {}", result)
//		}
		
//}
		

/////////////////////////////////

fn error_check(check: bool) -> Result<i8, &'static str> {
 	if check == true {
 		Err("this is an error")
 	} else {
 	Ok(1)
 	}
}

fn main() {
 	let result: i8 = error_check(false).unwrap();
 	println!("{}", result);
} 


////////////////////////////////////





