from distutils.core import setup , Extension

module = Extension('vuln', sources = ['native.c'])
setup(name = 'vuln',
	version = '1.0',
	description = 'this is a package for my module',
	ext_modules = [module],
	author = "Ramin Farajpour Cami"
)
