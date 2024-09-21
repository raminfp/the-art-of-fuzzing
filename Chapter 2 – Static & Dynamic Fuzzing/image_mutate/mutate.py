#!/usr/bin/env python3

import sys

def get_bytes(filename):

	f = open(filename, "rb").read()

	return bytearray(f)

if len(sys.argv) < 2:
	print("Usage: mutate.py <valid_jpg>")

else:
	filename = sys.argv[1]
	data = get_bytes(filename)
	counter = 0
	for x in data:
		if counter < 10:
			print(x)
		counter += 1

