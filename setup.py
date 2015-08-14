#!/usr/bin/env python3

from setuptools import setup, find_packages


setup(
    name="pristella",
    version="0.0.1",
    description="Web Cam Server as a Twitter Client",
    license="MIT",
    author="e8l",
    url="https://github.com/e8l/pristella",
    keywords="python webcam twitter",
    packages=find_packages(),
    install_requires=["python-daemon"],
    dependency_links=["git+https://github.com/litl/rauth.git#egg=rauth"],
    extras_require={"test": ["pytest"]})