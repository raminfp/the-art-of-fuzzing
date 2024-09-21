#!/usr/bin/env python

from distutils.core import setup, Extension

setup(name='ipv6',
      version='1.23',
      description='Advanced IPv6 Socket Manipulation for Python',
      long_description='An extension module intended to allow more advanced manipulation of IPv6 sockets in Python (ie: flow labels). Requires a kernel with IPv6 flow label support.',
      author='Joseph Ishac',
      author_email='jishac@nasa.gov',
      url='https://github.com/nasa/ipv6_python',
      license='NASA Open Source Agreement version 1.3',
      ext_modules=[Extension('ipv6', ['src/ipv6.c'])],
      )

