# Fuzzing Python package with pythonfuzz

## Install pythonfuzz
``` sh
# https://gitlab.com/gitlab-org/security-products/analyzers/fuzzers/pythonfuzz
pip3 install pythonfuzz
```

## Install pyasn1
``` sh
# https://github.com/etingof/pyasn1
pip3 install pyasn1
pip3 install pyasn1_modules
```

## Create your fuzz target for pyasn1

``` sh
# some code example: https://www.programcreek.com/python/?code=nelenkov%2Faboot-parser%2Faboot-parser-master%2Fparse-aboot.py
vim fuzz_pyasn1.py
```

``` python
from pyasn1.codec.der.decoder import decode
from pyasn1_modules import rfc2459
from pyasn1.error import PyAsn1Error
from pythonfuzz.main import PythonFuzz

@PythonFuzz
def fuzz(buf):
    try:
    	certType = rfc2459.Certificate(); 
    	cert, rest = decode(buf, asn1Spec=certType)
    except PyAsn1Error:
        pass

if __name__ == '__main__':
    fuzz()

```

## pythonfuzz commands
``` sh
python3 fuzz_pyasn1.py # Run fuzzing of fuzz_pyasn1.py
```
