import codecs
try:
    from setuptools import setup, find_packages
    extra_setup = dict(
        zip_safe = True,
        install_requires = ['httplib2', 'argparse'],
        )
except ImportError:
    from distutils.core import setup
    extra_setup = {}

setup(
    name='rtd',
    version='1.2',
    author='Eric Holscher',
    author_email='eric@ericholscher.com',
    url='http://github.com/ericholscher/rtd',
    license='BSD',
    description='Find documentation on Read the Docs!',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    long_description=codecs.open("README.rst", "r", "utf-8").read(),
    entry_points={
        'console_scripts': [
            'rtd=rtd:main',
            'rtfd=rtd:main'
            ]
        },
    **extra_setup
)
