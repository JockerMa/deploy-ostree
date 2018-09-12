# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os.path
from . import DeployStep
from ..config import Config
from ..run import run


class CreateStateroot(DeployStep):
    DEPLOY_DIR = '/ostree/deploy/'

    def __init__(self, cfg: Config) -> None:
        self.stateroot = cfg.stateroot
        self.sysroot = cfg.sysroot

    @property
    def title(self) -> str:
        return 'Creating stateroot: %s' % self.stateroot

    def run(self):
        if os.path.exists(self.DEPLOY_DIR + self.stateroot):
            print("already exists, skipping")
            return
        run([
            'ostree', 'admin', 'os-init',
            '--sysroot=%s' % self.sysroot,
            self.stateroot
        ], check=True)
