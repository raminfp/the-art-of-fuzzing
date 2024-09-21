# Fuzzing Python package with Atheris

## Install atheris
``` sh
# https://github.com/google/atheris
pip3 install atheris
```

## Install beautifulsoup4
``` sh
# https://www.crummy.com/software/BeautifulSoup/
# https://pypi.org/project/beautifulsoup4/
pip3 install beautifulsoup4
```

## Create your fuzz target for beautifulsoup4

``` sh
# Some examples:
# https://github.com/google/atheris/tree/master/example_fuzzers
vim fuzz_bs4.py
```

``` python
import atheris
import sys
from bs4 import BeautifulSoup

def TestOneInput(data):
  soup = BeautifulSoup(data, 'html.parser')
  soup.prettify()

atheris.Setup(sys.argv, TestOneInput)
atheris.Fuzz()
```

## Run the fuzzer

``` sh
python3 fuzzing_bs4.py
INFO: Seed: 107776927
INFO: Loaded 2 modules   (1024 inline 8-bit counters): 512 [0x164c800, 0x164ca00), 512 [0x170dfc0, 0x170e1c0), 
INFO: Loaded 2 PC tables (1024 PCs): 512 [0x175d6a0,0x175f6a0), 512 [0x175fec0,0x1761ec0), 
INFO: -max_len is not provided; libFuzzer will not generate inputs larger than 4096 bytes
	NEW_PY_FUNC[1/2]: TestOneInput() fuzzing_bs4.py:5
	NEW_PY_FUNC[2/2]: __init__() /home/scop/.local/lib/python3.8/site-packages/bs4/__init__.py:115
INFO: A corpus is not provided, starting from an empty corpus
	NEW_PY_FUNC[1/2]: <module>() /usr/lib/python3.8/encodings/ascii.py:1
```

## Crashes
``` sh
python3 fuzzing_bs4.py crash-0509de677541be3160ddbcb6cd567c94e35cd7ee
INFO: Configured for Python tracing with opcodes.
WARNING: Failed to find function "__sanitizer_acquire_crash_state".
WARNING: Failed to find function "__sanitizer_print_stack_trace".
WARNING: Failed to find function "__sanitizer_set_death_callback".
INFO: Seed: 166633809
INFO: Loaded 2 modules   (1024 inline 8-bit counters): 512 [0x100cb40, 0x100cd40), 512 [0x10ce300, 0x10ce500), 
INFO: Loaded 2 PC tables (1024 PCs): 512 [0x111d9e0,0x111f9e0), 512 [0x1120200,0x1122200), 
fuzzing_bs4.py: Running 1 inputs 1 time(s) each.
Running: crash-0509de677541be3160ddbcb6cd567c94e35cd7ee
	NEW_PY_FUNC[1/2]: TestOneInput() fuzzing_bs4.py:5
	NEW_PY_FUNC[2/2]: __init__() /home/scop/.local/lib/python3.8/site-packages/bs4/__init__.py:115
Some characters could not be decoded, and were replaced with REPLACEMENT CHARACTER.
/home/scop/.local/lib/python3.8/site-packages/bs4/builder/_htmlparser.py:102: UserWarning: expected name token at '<![�'
  warnings.warn(msg)

 === Uncaught Python exception: ===
TypeError: cannot unpack non-iterable NoneType object
Traceback (most recent call last):
  File "fuzzing_bs4.py", line 6, in TestOneInput
    soup = BeautifulSoup(data, 'html.parser')
  File "/home/scop/.local/lib/python3.8/site-packages/bs4/__init__.py", line 348, in __init__
    self._feed()
  File "/home/scop/.local/lib/python3.8/site-packages/bs4/__init__.py", line 434, in _feed
    self.builder.feed(self.markup)
  File "/home/scop/.local/lib/python3.8/site-packages/bs4/builder/_htmlparser.py", line 377, in feed
    parser.feed(markup)
  File "/usr/lib/python3.8/html/parser.py", line 111, in feed
    self.goahead(0)
  File "/usr/lib/python3.8/html/parser.py", line 179, in goahead
    k = self.parse_html_declaration(i)
  File "/usr/lib/python3.8/html/parser.py", line 264, in parse_html_declaration
    return self.parse_marked_section(i)
  File "/usr/lib/python3.8/_markupbase.py", line 149, in parse_marked_section
    sectName, j = self._scan_name( i+3, i )

==2270404== ERROR: libFuzzer: fuzz target exited
SUMMARY: libFuzzer: fuzz target exited

```

## Learn more about Atheris

API - https://github.com/google/atheris#api
FuzzedDataProvider - https://github.com/google/atheris#fuzzeddataprovider
