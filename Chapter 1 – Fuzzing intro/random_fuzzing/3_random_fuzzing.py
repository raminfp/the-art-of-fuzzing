import os
import tempfile

if __name__ == "__main__":
    basename = "input.txt"
    tempdir = tempfile.mkdtemp()
    FILE = os.path.join(tempdir, basename)
    print(FILE)
