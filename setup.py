# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from setuptools import setup
from os import path


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

    packages=['deploy_ostree'],
    install_requires=[],
    extras_require={
        'dev': ['flake8', 'mypy'],
    },
    package_data={
        'deploy_ostree': ['default-provisioners'],
    },
    entry_points={
        'console_scripts': [
            'deploy-ostree=deploy_ostree:main',
        ],
    },
)
