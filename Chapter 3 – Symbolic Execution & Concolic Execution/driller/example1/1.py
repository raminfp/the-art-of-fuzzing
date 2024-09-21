import driller
binary_name = "./fst"
 
d = driller.Driller(binary_name, b"A" * 0x40, b"\xff" * 65535)
new_inputs = d.drill()
print(new_inputs)
