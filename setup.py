"""setup.py"""
from setuptools import setup

with open("README.md") as f:
    README = f.read()

setup(
    author="Beau Barker",
    author_email="beau@explodinglabs.com",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    description="Send JSON-RPC requests",
    include_package_data=True,
    install_requires=[],
    license="MIT",
    long_description=README,
    long_description_content_type="text/markdown",
    name="jsonrpcclient",
    # Be PEP 561 compliant
    # https://mypy.readthedocs.io/en/stable/installed_packages.html#making-pep-561-compatible-packages
    package_data={"jsonrpcclient": ["response-schema.json", "py.typed"]},
    zip_safe=False,
    packages=["jsonrpcclient"],
    url="https://github.com/explodinglabs/jsonrpcclient",
    version="4.0.1",
)
