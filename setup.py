"""setup.py"""

from codecs import open as codecs_open
from setuptools import setup

with codecs_open('README.rst', 'r', 'utf-8') as f:
    __README = f.read()
with codecs_open('HISTORY.rst', 'r', 'utf-8') as f:
    __HISTORY = f.read()

setup(
    name='jsonrpcclient',
    version='2.4.1',
    description='Send JSON-RPC requests',
    long_description=__README+'\n\n'+__HISTORY,
    author='Beau Barker',
    author_email='beauinmelbourne@gmail.com',
    url='https://jsonrpcclient.readthedocs.io/',
    license='MIT',
    packages=['jsonrpcclient'],
    package_data={'jsonrpcclient': ['response-schema.json']},
    include_package_data=True,
    install_requires=['future', 'jsonschema'],
    extras_require={
        'aiohttp': ['aiohttp'],
        'requests': ['requests'],
        'requests_security': ['requests[security]'],
        'tornado': ['tornado'],
        'unittest': ['requests', 'pyzmq', 'tornado', 'responses', \
            'testfixtures', 'mock'],
        'websockets': ['websockets'],
        'zmq': ['pyzmq'],
    },
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
)
