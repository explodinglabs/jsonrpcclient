"""setup.py"""

from codecs import open as codecs_open
from setuptools import setup

with codecs_open('README.md', 'r', 'utf-8') as f:
    __README = f.read()
with codecs_open('HISTORY.md', 'r', 'utf-8') as f:
    __HISTORY = f.read()

setup(
    author='Beau Barker',
    author_email='beauinmelbourne@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    description='Send JSON-RPC requests',
    entry_points={'console_scripts': ['jsonrpc = jsonrpcclient.__main__:main']},
    extras_require={
        'aiohttp': ['aiohttp'],
        'requests': ['requests'],
        'requests_security': ['requests[security]'],
        'tornado': ['tornado'],
        'unittest': ['requests', 'pyzmq', 'tornado', 'responses',
                     'testfixtures', 'mock'],
        'websockets': ['websockets'],
        'zmq': ['pyzmq'],
    },
    include_package_data=True,
    install_requires=['future==0.16.0', 'jsonschema==2.6.0', 'click==6.7'],
    license='MIT',
    long_description=__README+'\n\n'+__HISTORY,
    name='jsonrpcclient',
    package_data={'jsonrpcclient': ['response-schema.json']},
    packages=['jsonrpcclient'],
    url='https://github.com/bcb/jsonrpcclient',
    version='2.5.2'
)
