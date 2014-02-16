#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import geocodio

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

version = geocodio.__version__
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
