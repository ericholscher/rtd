import commands
from distutils.core import setup

setup(
    name='docs.py',
    version='1.0',
    author='Eric Holscher',
    author_email='eric@ericholscher.com',
    url='http://github.com/ericholscher/docs.py',
    scripts=['bin/docs.py'],
    license='BSD',
    description='Find documentation on Read the Docs!',
    requires=['httplib2 (==0.6.0)'],
)

