# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import subprocess
import sys
from .fixture import Fixture


class HttpServerFixture(Fixture):
    def __init__(self, directory: str, port: int) -> None:
        self.http_server = None
        self.directory = directory
        self.port = port

    def setUp(self):
        self.http_server = subprocess.Popen(
            [sys.executable, '-mhttp.server', str(self.port), '--bind', '127.0.0.1'],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            cwd=self.directory)

    def tearDown(self):
        if self.http_server:
            self.http_server.kill()
            self.http_server = None
