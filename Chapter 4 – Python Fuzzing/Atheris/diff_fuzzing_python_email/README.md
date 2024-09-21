## Install atheris
``` sh
# https://github.com/google/atheris
pip3 install atheris
```

## Install validators
``` sh
# https://pypi.org/project/validators/
# https://validators.readthedocs.io/en/latest/#module-validators.email
pip3 install validators
```

## Install email_validator
``` sh
# https://pypi.org/project/email-validator/
pip3 install email-validator
```

## Create a basic differential fuzzer
``` sh
# Some examples:
# https://github.com/google/atheris/tree/master/example_fuzzers
vim diff_fuzz_email_valid.py
```

``` python
import atheris
import sys

from email_validator import validate_email, EmailNotValidError
import validators

def TestOneInput(input_bytes):

    fdp = atheris.FuzzedDataProvider(input_bytes)
    #email = fdp.ConsumeUnicode(sys.maxsize)
    email = fdp.ConsumeString(25)

    # test validators package
    valid2=validators.email(email)


    try:
        # email_validator
        valid = validate_email(email)

        # first case: `validate_email` is True but `validators.email` is False
        if valid2==False:
            print(email)
            print(valid)
            print(valid2)
            raise Exception("diff validate_email true / validators.email false")

    # email_validator exception  
    except EmailNotValidError:
        # second case: `validate_email` is False (exception) but `validators.email` is True
        if valid2==True:
            print(email)
            print(valid2)
            raise Exception("diff validate_email false / validators.email true")

atheris.Setup(sys.argv, TestOneInput)
atheris.Fuzz()
```

## Run the fuzzer

``` sh
# input_email is the corpora folder
python3 diff_fuzz_email_valid.py input_email
```

## Replay differential bug
``` sh
$ python3 diff_fuzzing_email.py diff_bug_email                                                                                                              scop@scop
INFO: Configured for Python tracing with opcodes.
WARNING: Failed to find function "__sanitizer_acquire_crash_state".
WARNING: Failed to find function "__sanitizer_print_stack_trace".
WARNING: Failed to find function "__sanitizer_set_death_callback".
INFO: Seed: 3278934069
INFO: Loaded 2 modules   (1024 inline 8-bit counters): 512 [0x1a7c980, 0x1a7cb80), 512 [0x1998f30, 0x1999130), 
INFO: Loaded 2 PC tables (1024 PCs): 512 [0x1a9aaa0,0x1a9caa0), 512 [0x1a9d2c0,0x1a9f2c0), 
diff_fuzzing_email.py: Running 1 inputs 1 time(s) each.
Running: diff_bug_email
  NEW_PY_FUNC[1/2]: TestOneInput() diff_fuzzing_email.py:7
  NEW_PY_FUNC[2/2]: email() <decorator-gen-12>:1
L@33.3.SS.'
True

 === Uncaught Python exception: ===
Exception: diff validate_email false / validators.email true
Traceback (most recent call last):
  File "diff_fuzzing_email.py", line 34, in TestOneInput
    raise Exception("diff validate_email false / validators.email true")

==1028108== ERROR: libFuzzer: fuzz target exited
SUMMARY: libFuzzer: fuzz target exited
```

## Replay email_validator bug
``` sh
python3 diff_fuzz_email_valid.py UnicodeEncodeError_email_validator
INFO: Configured for Python tracing with opcodes.
WARNING: Failed to find function "__sanitizer_acquire_crash_state".
WARNING: Failed to find function "__sanitizer_print_stack_trace".
WARNING: Failed to find function "__sanitizer_set_death_callback".
INFO: Seed: 3227637293
INFO: Loaded 2 modules   (1024 inline 8-bit counters): 512 [0x19df980, 0x19dfb80), 512 [0x18fc170, 0x18fc370), 
INFO: Loaded 2 PC tables (1024 PCs): 512 [0x19fd640,0x19ff640), 512 [0x19ffe60,0x1a01e60), 
diff_fuzzing_email.py: Running 1 inputs 1 time(s) each.
Running: UnicodeEncodeError_email_validator
  NEW_PY_FUNC[1/2]: TestOneInput() diff_fuzzing_email.py:7
  NEW_PY_FUNC[2/2]: email() <decorator-gen-12>:1

 === Uncaught Python exception: ===
UnicodeEncodeError: 'utf-8' codec can't encode character '\udff8' in position 0: surrogates not allowed
Traceback (most recent call last):
  File "diff_fuzzing_email.py", line 19, in TestOneInput
    valid = validate_email(email)
  File "/home/scop/.local/lib/python3.8/site-packages/email_validator/__init__.py", line 264, in validate_email
    if len(ret.email.encode("utf8")) > EMAIL_MAX_LENGTH:

==1028028== ERROR: libFuzzer: fuzz target exited
SUMMARY: libFuzzer: fuzz target exited
```
