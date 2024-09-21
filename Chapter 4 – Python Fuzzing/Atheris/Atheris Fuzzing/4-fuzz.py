import yaml
import atheris
import sys

def testing(data):
	users = [{'name': data, 'occupation': data}]

	yaml.dump(users)

def TestOneInput(data):

	testing(data)

atheris.Setup(sys.argv, TestOneInput)
atheris.Fuzz()
