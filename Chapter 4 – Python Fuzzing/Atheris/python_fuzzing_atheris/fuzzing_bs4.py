import atheris
import sys
from bs4 import BeautifulSoup

def TestOneInput(data):
  soup = BeautifulSoup(data, 'html.parser')
  soup.prettify()

atheris.Setup(sys.argv, TestOneInput)
atheris.Fuzz()