# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os.path
from typing import Sequence
from . import DeployStep
from ..config import Config
from ..run import run


class FileRemote(DeployStep):
    def __init__(self, cfg: Config) -> None:
        self.remote = cfg.remote
        self.path = cfg.path

    @property
    def title(self) -> str:
        return 'Adding OSTree remote: %s' % self.path

    def run(self):
        run([
            'ostree', 'remote', 'add',
            '--no-gpg-verify',
            self.remote,
            'file://%s' % os.path.abspath(self.path)
        ], check=True)

    @classmethod
    def get_steps(cls, cfg) -> Sequence[DeployStep]:
        if cfg.path is None:
            return []
        return [cls(cfg)]


class HttpRemote(DeployStep):
    def __init__(self, cfg: Config) -> None:
        self.remote = cfg.remote
        self.url = cfg.url

    @property
    def title(self) -> str:
        return 'Adding OSTree remote: %s' % self.url

    def run(self):
        run([
            'ostree', 'remote', 'add',
            '--no-gpg-verify',
            self.remote,
            self.url
        ], check=True)

    @classmethod
    def get_steps(cls, cfg) -> Sequence[DeployStep]:
        if cfg.url is None:
            return []
        return [cls(cfg)]
