# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from . import DeployStep
from ..config import Config
from ..run import run


class PullRef(DeployStep):
    def __init__(self, cfg: Config) -> None:
        self.remote = cfg.remote
        self.ref = cfg.ref

    @property
    def title(self) -> str:
        return 'Pulling: %s:%s' % (self.remote, self.ref)

    def run(self):
        run(['ostree', 'pull', self.remote, self.ref], check=True)
