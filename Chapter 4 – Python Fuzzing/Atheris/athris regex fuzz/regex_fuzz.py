import sys, re 
import atheris
from urllib.parse import urlparse

# Our sketchy regex to be tested
OurRegex = re.compile(b"^(((([A-Za-z0-9.-]*\.)?example1\.com)|(([A-Za-z0-9.-]*\.)\?example2\.com)|(([A-Za-z0-9.-]*\.)?example3\.com)))")

# The allow list of domains the regex is trying to validate
Allowlist = [b"example1.com", b"example2.com", b"example3.com"]

# Our Fuzzing Harness
def TestOneInput(data):
    # Arbitrary, but lets get a minimum of 5 bytes of fuzz data
    if len(data) < 5:
        return
        
    # We use the first byte as a random value selector of one of the three allowed domains
    # and we append the domain to the rest of the fuzzer test data
    #
    # Test will look something like this: <FUZZ DATA>example1.com, <FUZZ DATA>example2.com, <FUZZ DATA>example3.com
    test = data[1:] + Allowlist[data[0] % len(Allowlist)]
    
    # We process our test case through the regex
    RegexResult = OurRegex.match(test)
    
    # If the regex didn't validate it as trusted there is no point in processing
    # it through urllib, just return
    if not RegexResult:
        return
    
    # We have a trusted input, lets compare it to urllib.
    # urllib will throw exception at malformed UTF-8 so
    # we place it inside a try block, return on exception
    try:
        # urlib also requires a scheme, so we give it https
        UrllibResult = urlparse(b"https://" + test)
    except:
        return

    # At this point we have results from urllib
    # lets validate that our RegEx-trusted input countains at least 1 of the trusted domains
    for domain in Allowlist:
        # For each domain in the Allowlist we result if we see any sign of it
        if domain in UrllibResult.netloc:
            return
    
    # If we got this far it means that we have an input deemed trusted by our regex
    # but urllib did not find any of the allowlist domains inside the authority string
    # of the parsed URL, raise an exception to the fuzzer
    print ("\n\n\n\n==================================================================")
    print ("(SEVERE): Found a potential bypass!")
    print ("\n         Payload: %s"% (test))
    print ("Urllib Authority: %s\n"% (UrllibResult.netloc))
    print ("Note: When parsing this input with urllib it appears that none  ")
    print ("of the allow list domains were found in the authority!")
    print ("==================================================================\n\n")
    raise RuntimeError("Fuzzer found a discrepency")
    

atheris.Setup(sys.argv, TestOneInput)
atheris.Fuzz()
