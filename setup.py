"""setup.py"""
from setuptools import setup

with open("README.md") as readme_file:
    README = readme_file.read()

test_requirements = ["mock", "pytest", "responses", "testfixtures", "requests", "pyzmq"]
# Async requirements
test_requirements.extend(["pytest-asyncio", "aiohttp", "tornado", "websockets"])

setup(
    author="Beau Barker",
    author_email="beauinmelbourne@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Send JSON-RPC requests",
    entry_points={"console_scripts": ["jsonrpc = jsonrpcclient.__main__:main"]},
    extras_require={
        "aiohttp": ["aiohttp>=3"],
        "requests": ["requests"],
        "requests_security": ["requests[security]"],
        "tornado": ["tornado"],
        "unittest": test_requirements,
        "websockets": ["websockets"],
        "zmq": ["pyzmq"],
    },
    include_package_data=True,
    install_requires=["apply_defaults<1", "click<8", "jsonschema<4"],
    license="MIT",
    long_description=README,
    long_description_content_type="text/markdown",
    name="jsonrpcclient",
    # Be PEP 561 compliant
    # https://mypy.readthedocs.io/en/stable/installed_packages.html#making-pep-561-compatible-packages
    package_data={"jsonrpcclient": ["response-schema.json", "py.typed"]},
    zip_safe=False,
    packages=["jsonrpcclient", "jsonrpcclient.clients"],
    url="https://github.com/bcb/jsonrpcclient",
    version="3.3.6",
)
