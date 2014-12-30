#!/usr/bin/env python
#pylint:disable=line-too-long
"""setup.py"""

import os

from codecs import open

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

with open('HISTORY.rst', 'r', 'utf-8') as f:
    history = f.read()

setup(
    name='jsonrpcclient',
    version='1.1.0',
    description='JSON-RPC 2.0 client library for Python 3.',
    long_description=readme + '\n\n' + history,
    author='Beau Barker',
    author_email='beauinmelbourne@gmail.com',
    url='https://jsonrpcclient.readthedocs.org/',
    packages=['jsonrpcclient'],
    package_data={'jsonrpcclient': ['response-schema.json']},
    include_package_data=True,
    install_requires=['requests', 'jsonschema'],
    tests_require=['nose','rednose','nose-cov','responses'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Development Status :: 5 - Production/Stable',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    )
