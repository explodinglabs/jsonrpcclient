"""setup.py"""
from codecs import open as codecs_open
from setuptools import setup

with codecs_open("README.md", "r", "utf-8") as f:
    README = f.read()

setup(
    author="Beau Barker",
    author_email="beauinmelbourne@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="Send JSON-RPC requests",
    entry_points={"console_scripts": ["jsonrpc = jsonrpcclient.__main__:main"]},
    extras_require={
        "aiohttp": ["aiohttp"],
        "requests": ["requests"],
        "requests_security": ["requests[security]"],
        "tornado": ["tornado"],
        "unittest": [
            "requests",
            "pyzmq",
            "tornado",
            "responses",
            "testfixtures",
            "mock",
        ],
        "websockets": ["websockets"],
        "zmq": ["pyzmq"],
    },
    include_package_data=True,
    install_requires=["jsonschema>2,<3", "click>6,<7"],
    license="MIT",
    long_description=README,
    long_description_content_type="text/markdown",
    name="jsonrpcclient",
    package_data={"jsonrpcclient": ["response-schema.json"]},
    packages=["jsonrpcclient", "jsonrpcclient.clients"],
    url="https://github.com/bcb/jsonrpcclient",
    version="3.0.0rc3",
)
