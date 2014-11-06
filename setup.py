#!/usr/bin/env python
"""setup.py"""
#pylint:disable=line-too-long

from distutils.core import setup

setup(
    name='jsonrpcclient',
    packages=['jsonrpcclient'],
    package_data={'jsonrpcclient': ['response-schema.json']},
    install_requires=['requests', 'jsonschema'],
    version='1.0.2',
    description='JSON-RPC 2.0 client library',
    author='Beau Barker',
    author_email='beauinmelbourne@gmail.com',
    url='https://bitbucket.org/beau-barker/jsonrpcclient',
    keywords=['json-rpc', 'json', 'api'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    )
