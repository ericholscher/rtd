import codecs
try:
    from setuptools import setup
    extra_setup = dict(
        zip_safe = True,
        install_requires = ['httplib2'],
        )
except ImportError:
    from distutils.core import setup
    extra_setup = {}

setup(
    name='rtd',
    version='1.1',
    author='Eric Holscher',
    author_email='eric@ericholscher.com',
    url='http://github.com/ericholscher/rtd',
    scripts=['bin/rtd'],
    license='BSD',
    description='Find documentation on Read the Docs!',
    long_description=codecs.open("README.rst", "r", "utf-8").read(),
    **extra_setup
)
