# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from datetime import datetime
from setuptools import setup, find_packages
import os.path
import re


timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
here = os.path.abspath(os.path.dirname(__file__))


# get the long description from the readme
def long_description():
    with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        return f.read()


# get the version from the changelog
def get_version():
    with open(os.path.join(here, 'CHANGELOG.md'), encoding='utf-8') as f:
        has_unreleased = False
        for line in f:
            match = re.match(r'## (\S+)\s+', line)
            if not match:
                continue
            if match.group(1) == '[Unreleased]':
                has_unreleased = True
            elif has_unreleased:
                return '%s.post%s.dev1' % (match.group(1), timestamp)
            else:
                return match.group(1)
    return '0.0.0.dev%s' % timestamp


setup(
    name='deploy-ostree',
    version=get_version(),
    description='Deploy and configure an OSTree commit',

    long_description=long_description(),
    long_description_content_type='text/markdown',
    author='Felix Krull',
    author_email='f_krull@gmx.de',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Topic :: System :: Boot',
        'Topic :: System :: Operating System',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    packages=find_packages(exclude=['tests', 'tests.*']),
    zip_safe=False,
    install_requires=[],
    extras_require={
        'dev': ['flake8', 'mypy'],
    },
    package_data={
        'deploy_ostree': ['default-provisioners/*'],
    },
    entry_points={
        'console_scripts': [
            'deploy-ostree=deploy_ostree:main',
        ],
    },
)
