"""setup.py"""

from setuptools import setup
from codecs import open as codecs_open

with codecs_open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()

with codecs_open('HISTORY.rst', 'r', 'utf-8') as f:
    history = f.read()

setup(
    name='jsonrpcclient',
    version='2.1.0',
    description='Send JSON-RPC requests',
    long_description=readme + '\n\n' + history,
    author='Beau Barker',
    author_email='beauinmelbourne@gmail.com',
    url='https://jsonrpcclient.readthedocs.org/',
    license='MIT',
    packages=['jsonrpcclient'],
    package_data={'jsonrpcclient': ['response-schema.json']},
    include_package_data=True,
    install_requires=['future', 'jsonschema'],
    tests_require=['tox'],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
