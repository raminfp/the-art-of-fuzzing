#!/usr/bin/env python3

import sys


def create_new(data):

	f = open("mutated.jpg", "wb+")
	f.write(data)
	f.close()

def get_bytes(filename):

	f = open(filename, "rb").read()

	return bytearray(f)

if len(sys.argv) < 2:
	print("Usage: mutate.py <valid_jpg>")

else:
	filename = sys.argv[1]
	data = get_bytes(filename)
	create_new(data)

