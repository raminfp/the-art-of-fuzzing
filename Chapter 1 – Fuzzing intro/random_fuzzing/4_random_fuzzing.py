import os
import subprocess
import tempfile


if __name__ == "__main__":
    basename = "input.txt"
    tempdir = tempfile.mkdtemp()
    FILE = os.path.join(tempdir, basename)
    print(FILE)

    program = "test"
    with open(FILE, "w") as f:
        f.write("2 + 2\n")
    result = subprocess.run([program, FILE],
                            stdin=subprocess.DEVNULL,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True)  # Will be "text" in Python 3.7


if __name__ == "__main__":
    print(result.stdout)
