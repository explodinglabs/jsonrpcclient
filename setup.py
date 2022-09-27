"""setup.py"""
from setuptools import setup

with open("README.md", encoding="utf-8") as f:
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
    extras_require={
        "test": [
            "pytest",
            "pytest-cov",
            "tox",
        ],
    },
    include_package_data=True,
    license="MIT",
    long_description=README,
    long_description_content_type="text/markdown",
    name="jsonrpcclient",
    packages=["jsonrpcclient"],
    url="https://github.com/explodinglabs/jsonrpcclient",
    version="4.0.2",
    # Be PEP 561 compliant
    # https://mypy.readthedocs.io/en/stable/installed_packages.html#making-pep-561-compatible-packages
    zip_safe=False,
)
