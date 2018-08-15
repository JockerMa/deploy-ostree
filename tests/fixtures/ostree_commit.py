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
    os.makedirs(os.path.join(commit_dir, 'var'), mode=0o755)

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
    def __init__(self, branch: str='test-commit', port: int=8000) -> None:
        self.http_server = None
        self.repo_dir = None
        self.branch = branch
        self.port = port

    def setUp(self):
        self.setup_repo()
        self.create_test_commit()
        self.start_http_server()

    def tearDown(self):
        if self.http_server:
            self.http_server.kill()
            self.http_server = None
        if self.repo_dir:
            self.repo_dir.cleanup()
            self.repo_dir = None

    def setup_repo(self):
        self.repo_dir = TemporaryDirectory()
        ostree(['init', '--repo', self.repo_dir.name, '--mode=archive-z2'])

    def create_test_commit(self):
        with TemporaryDirectory() as commit_dir:
            create_test_tree(commit_dir)
            ostree(['commit', '--repo', self.repo_dir.name, '--branch', self.branch, commit_dir])

    def start_http_server(self):
        self.http_server = subprocess.Popen(
            [sys.executable, '-mhttp.server', str(self.port), '--bind', '127.0.0.1'],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            cwd=self.repo_dir.name)
