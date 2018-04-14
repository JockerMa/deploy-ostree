# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os
import subprocess
import sys
from tempfile import TemporaryDirectory
from typing import Optional  # noqa
import uuid
from .fixture import Fixture
from .. import ostree


def touch(path):
    with open(path, 'w'):
        pass


def create_test_tree(commit_dir: str):
    kern_dir = os.path.join(commit_dir, 'usr', 'lib', 'modules', '4.8')
    os.makedirs(kern_dir)
    touch(os.path.join(kern_dir, 'vmlinuz'))
    touch(os.path.join(kern_dir, 'initrd'))

    etc_dir = os.path.join(commit_dir, 'usr', 'etc')
    os.makedirs(etc_dir)
    with open(os.path.join(etc_dir, 'os-release'), 'w', encoding='ascii') as f:
        f.write('ID=')
        f.write(uuid.uuid4().hex)


class OSTreeCommitFixture(Fixture):
    BRANCH = 'test-commit'
    PORT = 8000

    http_server = None  # type: Optional[subprocess.Popen]
    repo_dir = None  # type: Optional[TemporaryDirectory]

    @classmethod
    def setUpClass(cls):
        cls.repo_dir = TemporaryDirectory()
        ostree(['init', '--repo', cls.repo_dir.name, '--mode=archive-z2'])
        with TemporaryDirectory() as commit_dir:
            create_test_tree(commit_dir)
            ostree(['commit', '--repo', cls.repo_dir.name, '--branch', cls.BRANCH, commit_dir])
        cls.http_server = subprocess.Popen(
            [sys.executable, '-mhttp.server', str(cls.PORT), '--bind', '127.0.0.1'],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            cwd=cls.repo_dir.name)

    @classmethod
    def tearDownClass(cls):
        if cls.repo_dir:
            cls.repo_dir.cleanup()
            cls.repo_dir = None
        if cls.http_server:
            cls.http_server.kill()
            cls.http_server = None
