from pythonfuzz.main import PythonFuzz
# import target library here

@PythonFuzz
def fuzz(buf):
    try:
    	# fuzz code here
    except Error: # handle expected errors here
        pass

if __name__ == '__main__':
    fuzz()
