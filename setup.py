#!/usr/bin/env python

from setuptools import setup
import sys
from setuptools.command.test import test as TestCommand

__version__ = None
with open('blockstack/version.py') as f:
    exec(f.read())


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ["blockstack/test"]

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='blockstack',
    version=__version__,
    packages=[
        'blockstack',
    ],
    url='https://cryptocorp.co/api',
    license='http://opensource.org/licenses/MIT',
    author='devrandom',
    author_email='info@cryptocorp.co',
    cmdclass={'test': PyTest},
    entry_points={
        'console_scripts':
            [
            ]
    },
    description='The CryptoCorp blockstack API',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    install_requires=[
        'pycoin',
        'requests',
        'urllib3',
        'python-dateutil'
    ],
    tests_require=[
        'httmock',
        'mock',
        'pytest'
    ],
    test_suite='blockstack.test',
)
