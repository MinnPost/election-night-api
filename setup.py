#!/usr/bin/env python

import sys
from setuptools import setup

# Get dependencies from requirements.txt
with open('requirements.txt') as f:
    required = f.read().splitlines()

# Package ingo
setup(
    name = 'election-night-api',
    version = '0.0.1',
    author = 'Alan Palazzolo (MinnPost), Tom Nehil (MinnPost)',
    author_email = 'apalazzolo@minnpost.com, tnehil@minnpost.com',
    packages = ['ena'],
    scripts = ['bin/ena'],
    url = 'https://github.com/MinnPost/election-night-api',
    license = 'MIT',
    description = 'A set of utlities and instructions for running an election night API.',
    long_description = open('README.md').read(),
    install_requires = required,
)
