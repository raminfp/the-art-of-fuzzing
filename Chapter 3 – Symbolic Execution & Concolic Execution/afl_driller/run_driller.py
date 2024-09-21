#!/usr/bin/env python

import errno
import os
import os.path
import sys
import time

from driller import Driller


def save_input(content, dest_dir, count):
    """Saves a new input to a file where AFL can find it.

    File will be named id:XXXXXX,driller (where XXXXXX is the current value of
    count) and placed in dest_dir.
    """
    name = 'id:%06d,driller' % count
    with open(os.path.join(dest_dir, name), 'wb') as destfile:
        destfile.write(content)


def main():
    if len(sys.argv) != 3:
        print('Usage: %s <binary> <fuzzer_output_dir>' % sys.argv[0])
        sys.exit(1)

    _, binary, fuzzer_dir = sys.argv

    # Figure out directories and inputs
    with open(os.path.join(fuzzer_dir, 'fuzz_bitmap'), 'rb') as bitmap_file:
        fuzzer_bitmap = bitmap_file.read()
    source_dir = os.path.join(fuzzer_dir, 'queue')
    dest_dir = os.path.join(fuzzer_dir, '..', 'driller', 'queue')

    # Make sure destination exists
    try:
        os.makedirs(dest_dir)
    except os.error as e:
        if e.errno != errno.EEXIST:
            raise

    seen = set()  # Keeps track of source files already drilled
    count = len(os.listdir(dest_dir))  # Helps us name outputs correctly

    # Repeat forever in case AFL finds something new
    while True:
        # Go through all of the files AFL has generated, but only once each
        for source_name in os.listdir(source_dir):
            if source_name in seen or not source_name.startswith('id:'):
                continue
            seen.add(source_name)
            with open(os.path.join(source_dir, source_name), 'rb') as seedfile:
                seed = seedfile.read()

            print('Drilling input: %s' % seed)
            for _, new_input in Driller(binary, seed, fuzzer_bitmap).drill_generator():
                save_input(new_input, dest_dir, count)
                count += 1

            # Try a larger input too because Driller won't do it for you
            seed = seed + b'0000'
            print('Drilling input: %s' % seed)
            for _, new_input in Driller(binary, seed, fuzzer_bitmap).drill_generator():
                save_input(new_input, dest_dir, count)
                count += 1
        time.sleep(10)

if __name__ == '__main__':
    main()