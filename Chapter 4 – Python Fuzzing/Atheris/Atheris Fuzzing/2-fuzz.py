from django.core.management import color
from django.utils import termcolors
import atheris
import sys


def color_style(evildata):
    if color.supports_color():
        style = color.color_style()
        style.INFO = termcolors.make_style(fg=evildata)
        style.BOLD = termcolors.make_style(opts=(evildata,))
        style.URL = termcolors.make_style(fg=evildata, opts=(evildata,))
    return style



def TestOneInput(data):

	color_style(data)

atheris.Setup(sys.argv, TestOneInput)
atheris.Fuzz()
