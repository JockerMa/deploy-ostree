# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os
from tempfile import TemporaryDirectory
from typing import Optional  # noqa
import uuid
from .fixture import Fixture
from .http_server import HttpServerFixture
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
    def __init__(self, branch: str='test-commit', mode: str='archive', http: bool=True, port: int=8000) -> None:
        self.http_server = None
        self.repo_dir = None
        self.branch = branch
        self.mode = mode
        self.http = http
        self.port = port

    def setUp(self):
        self.setup_repo()
        self.create_test_commit()
        if self.http:
            self.start_http_server()

    def tearDown(self):
        if self.http_server:
            self.http_server.tearDown()
        if self.repo_dir:
            self.repo_dir.cleanup()
            self.repo_dir = None

    def setup_repo(self):
        self.repo_dir = TemporaryDirectory()
        ostree(['init', '--repo', self.repo_dir.name, '--mode', self.mode])

    def create_test_commit(self):
        with TemporaryDirectory() as commit_dir:
            create_test_tree(commit_dir)
            ostree(['commit', '--repo', self.repo_dir.name, '--branch', self.branch, commit_dir])

    def start_http_server(self):
        self.http_server = HttpServerFixture(self.repo_dir.name, self.port)
        self.http_server.setUp()
