#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import placidity
from setuptools import setup

def pandoc(source, from_format, to_format):
    # http://osiux.com/html-to-restructured-text-in-python-using-pandoc
    # raises OSError if pandoc is not found!
    p = subprocess.Popen(['pandoc', '--from=' + from_format, '--to=' + to_format],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE
        )
    return p.communicate(source)[0]

description = "Specification based test runner."
try:
    md = open('README.md').read()

    long_description = pandoc(md, 'markdown', 'rst')
except (IOError, OSError):
    print 'check that you have installed pandoc properly and that README.md exists!'
    long_description = description

setup(
    name = "placidity",
    version = placidity.__version__,
    url = 'https://github.com/bebraw/placidity',
    license = 'MIT',
    description = description,
    long_description = long_description,
    author = placidity.__author__,
    author_email = 'bebraw@gmail.com',
    packages = ['placidity', 'placidity.core', 'placidity.extras'],
    package_dir = {'placidity': 'placidity', },
    install_requires = ['setuptools', ],
    entry_points="""
    [console_scripts]
    placidity = placidity.application:main
    """,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing',
    ],
)
