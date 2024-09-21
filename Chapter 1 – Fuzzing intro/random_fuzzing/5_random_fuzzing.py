import os
import subprocess
import tempfile
from random import randint
import random

def fuzzer(max_length=100, char_start=32, char_range=32):
    """A string of up to `max_length` characters
       in the range [`char_start`, `char_start` + `char_range`]"""
    string_length = random.randrange(0, max_length + 1)
    out = ""
    for i in range(0, string_length):
        out += chr(random.randrange(char_start, char_start + char_range))
    return out

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


if __name__ == "__main__":
    trials = 1000
    program = "./test"
    runs = []

    for i in range(trials):
        #data = fuzzer(1000, ord('a'), 26)
        data = random_with_N_digits(random.randint(1,9))
        print("##################### Data for Fuzzing")
        print(data)
        print("###################################")
        result = subprocess.run([program, str(data)])
        runs.append((data, result))
        print(result)


