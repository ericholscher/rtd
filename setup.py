from distutils.core import setup
import codecs

setup(
    name='rtd',
    version='1.0.1',
    author='Eric Holscher',
    author_email='eric@ericholscher.com',
    url='http://github.com/ericholscher/rtd',
    scripts=['bin/rtd'],
    license='BSD',
    description='Find documentation on Read the Docs!',
    long_description=codecs.open("README.rst", "r", "utf-8").read()
)

