"""setup.py"""
#pylint:disable=line-too-long

import sys
from setuptools.command.test import test as TestCommand
from codecs import open as codecs_open

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup #pylint:disable=import-error,no-name-in-module

with codecs_open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

with codecs_open('HISTORY.rst', 'r', 'utf-8') as f:
    history = f.read()

class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = '-v'
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        import shlex
        errno = tox.cmdline(args=shlex.split(self.tox_args))
        sys.exit(errno)

setup(
    name='jsonrpcclient',
    version='1.1.5',
    description='JSON-RPC client library.',
    long_description=readme + '\n\n' + history,
    author='Beau Barker',
    author_email='beauinmelbourne@gmail.com',
    url='https://jsonrpcclient.readthedocs.org/',
    packages=['jsonrpcclient'],
    package_data={'jsonrpcclient': ['response-schema.json']},
    include_package_data=True,
    install_requires=['requests', 'jsonschema'],
    tests_require=['tox'],
    cmdclass = {'test': Tox},
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent'
        ],
    )
