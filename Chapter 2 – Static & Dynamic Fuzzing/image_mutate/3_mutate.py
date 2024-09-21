#!/usr/bin/env python3
# python3.9 3_mutate.py Canon_40D.jpg > te

import sys
import random

def create_new(data):

	f = open("mutated.jpg", "wb+")
	f.write(data)
	f.close()

def get_bytes(filename):

	f = open(filename, "rb").read()

	return bytearray(f)

def bit_flip(data):

	num_of_flips = int((len(data) - 4) * .01)

	indexes = range(4, (len(data) - 4))

	chosen_indexes = []

	# iterate selecting indexes until we've hit our num_of_flips number
	counter = 0
	while counter < num_of_flips:
		chosen_indexes.append(random.choice(indexes))
		counter += 1

	for x in chosen_indexes:
		current = data[x]
		current = (bin(current).replace("0b",""))
		current = "0" * (8 - len(current)) + current
		print(current)

if len(sys.argv) < 2:
	print("Usage: mutate.py <valid_jpg>")

else:
	filename = sys.argv[1]
	data = get_bytes(filename)
	#create_new(data)
	bit_flip(data)
