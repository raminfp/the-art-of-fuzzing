import atheris_no_libfuzzer as atheris
import sys
import vuln

def TestOnInput(data):
	if data:
		vuln.overflow(data, "hello.txt")
		return

atheris.Setup(sys.argv, TestOnInput)
atheris.Fuzz()
