# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from shutil import which
from typing import Iterable
from . import DeployStep
from ..config import Config
from ..run import run


class HttpRemote(DeployStep):
    def __init__(self, cfg: Config) -> None:
        self.ostree = which('ostree')
        self.cfg = cfg

    def run(self):
        print('==> Adding OSTree remote:', self.cfg.url)
        run([
            self.ostree,
            'remote',
            'add',
            '--no-gpg-verify',
            '--if-not-exists',
            '--repo=/ostree/repo',
            self.cfg.remote,
            self.cfg.url
        ], check=True)

    @classmethod
    def is_relevant(cls, cfg: Config) -> bool:
        return cfg.url is not None

    @classmethod
    def get_steps(cls, cfg: Config) -> Iterable[DeployStep]:
        return [cls(cfg)]
