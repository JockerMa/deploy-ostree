# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from datetime import datetime
from setuptools import setup, find_packages
import os.path
import os
import re


timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
here = os.path.abspath(os.path.dirname(__file__))
release_version = os.getenv('RELEASE_VERSION')


# get the long description from the readme
def long_description():
    with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        return f.read()


# get the version from the changelog
def get_changelog_version():
    with open(os.path.join(here, 'CHANGELOG.md'), encoding='utf-8') as f:
        for line in f:
            match = re.match(r'## (\S+)\s+', line)
            if match:
                return match.group(1)
    raise Exception('no version in changelog')


def get_dev_version(base_version):
    return '%s.dev%s' % (base_version, timestamp)


def get_version():
    changelog_version = get_changelog_version()
    if not release_version:
        return get_dev_version(changelog_version)
    elif release_version == changelog_version:
        return changelog_version
    else:
        raise Exception('expected version %s, got %s' %
                        (release_version, changelog_version))


setup(
    name='deploy-ostree',
    version=get_version(),
    description='Deploy and configure an OSTree commit',

    long_description=long_description(),
    long_description_content_type='text/markdown',
    author='Felix Krull',
    author_email='f_krull@gmx.de',
    url='https://gitlab.com/fkrull/deploy-ostree',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
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

    package_dir={'': 'src'},
    packages=find_packages('src', exclude=['tests', 'tests.*']),
    zip_safe=False,
    install_requires=[],
    extras_require={
        'dev': ['flake8', 'mypy', 'pytest', 'twine>=1.12'],
        'test': ['pytest'],
    },
    package_data={
        'deploy_ostree': ['builtin-provisioners/*'],
    },
    entry_points={
        'console_scripts': [
            'deploy-ostree=deploy_ostree:main',
        ],
    },
)
