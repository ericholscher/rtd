import commands
from distutils.core import setup

setup(
    name='doc.py',
    version='1.0',
    author='Eric Holscher',
    author_email='eric@ericholscher.com',
    url='http://github.com/ericholscher/doc.py',
    scripts=['bin/doc.py'],
    license='BSD',
    description='Find documentation anywhere!',
    install_requires=['httplib2'],
)

