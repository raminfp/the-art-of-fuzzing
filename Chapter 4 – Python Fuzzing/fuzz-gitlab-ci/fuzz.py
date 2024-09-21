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

    print(input_bytes)

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
