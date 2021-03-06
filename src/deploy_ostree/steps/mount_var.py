# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os.path
from . import DeployStep
from ..config import Config
from ..run import run


class MountVar(DeployStep):
    def __init__(self, cfg: Config) -> None:
        self.cfg = cfg

    @property
    def title(self) -> str:
        return 'Mounting stateroot /var'

    def run(self):
        run([
            'mount', '-o', 'bind',
            self.cfg.var_dir,
            os.path.join(self.cfg.deployment_dir, 'var'),
        ], check=True)

    def cleanup(self):
        run([
            'umount', '-l',
            os.path.join(self.cfg.deployment_dir, 'var'),
        ], check=True)
