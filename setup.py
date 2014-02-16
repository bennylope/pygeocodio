#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


with open("geocodio/__init__.py", "r") as module_file:
    for line in module_file:
        if line.startswith("__version__"):
            version_string = line.split("=")[1]
            version = version_string.strip().replace("'", "")

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='pygeocodio',
    version=version,
    description='Python wrapper for Geocod.io API',
    long_description=readme + '\n\n' + history,
    author='Ben Lopatin',
    author_email='ben@wellfire.co',
    url='https://github.com/bennylope/pygeocodio',
    packages=[
        'geocodio',
    ],
    include_package_data=True,
    install_requires=[
        'requests>=1.0.0',
    ],
    license="BSD",
    zip_safe=False,
    keywords='geocodio',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP',
    ],
    test_suite='tests',
)
