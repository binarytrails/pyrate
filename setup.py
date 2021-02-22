#!/usr/bin/env python

# @author Vsevolod Ivanov <seva@binarytrails.net>

from setuptools import setup, find_packages, Extension

setup(
    name='pyrate',
    version='0.1',
    description='pyrate - simple pentest tools',
    url='https://github.com/binarytrails/pyrate',
    author='vsevolod ivanov',
    author_email='seva@binarytrails.net',
    license='GPLv3+',
    keywords='pyrate simple pentest pentesting tools',
    platforms='any',
    packages=['pyrate'],
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Pentesting :: Automation',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
    ],
    entry_points={
        'console_scripts': [ 'pyrate=pyrate.main:main']
    }
)
