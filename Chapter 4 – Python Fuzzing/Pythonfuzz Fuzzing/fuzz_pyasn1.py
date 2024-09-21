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
