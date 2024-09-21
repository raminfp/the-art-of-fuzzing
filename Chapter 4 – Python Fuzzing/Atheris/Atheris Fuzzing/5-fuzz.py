from __future__ import unicode_literals
from hazm import *
import atheris
import sys
import base64

def testing(data):
	normalizer = Normalizer()
	normalizer.normalize(data)



def TestOneInput(data):
	testing(data)

atheris.Setup(sys.argv, TestOneInput)
atheris.Fuzz()
