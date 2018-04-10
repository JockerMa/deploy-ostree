# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from setuptools import setup, find_packages
from os import path
import unittest


def get_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('test', pattern='test_*.py')
    return test_suite


here = path.abspath(path.dirname(__file__))
# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='deploy-ostree',
    version='0.1.0',
    description='Deploy and configure an OSTree commit',

    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Felix Krull',
    author_email='f_krull@gmx.de',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[],
    package_data={
        'deploy_ostree': ['default-provisioners'],
    },
    entry_points={
        'console_scripts': [
            'deploy-ostree=deploy_ostree:main',
        ],
    },
    test_suite='setup.get_test_suite',
)
