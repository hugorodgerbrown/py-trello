#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name = "pyello",
    version = "0.1",

    description = 'Python wrapper around the Trello API',
    long_description = open('README.md').read(),
    author = 'Hugo Rodger-Brown',
    author_email = 'hugo@rodger-brown.com',
    keywords = 'python',
    license = 'BSD License',
    classifiers = [
        "Development Status :: 4 - Beta",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    install_requires = ['httplib2', ],
    packages = find_packages(),
    include_package_data = True,
)
