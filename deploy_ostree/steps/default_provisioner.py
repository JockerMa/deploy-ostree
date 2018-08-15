# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os
from typing import Sequence
import deploy_ostree
from . import DeployStep
from ..config import Config, ProvisionerConfig
from ..run import run


PROVISIONER_DIR = os.path.join(os.path.dirname(deploy_ostree.__file__), 'default-provisioners')


class DefaultProvisioner(DeployStep):
    def __init__(self, config: Config, provisioner: ProvisionerConfig) -> None:
        self.config = config
        self.provisioner = provisioner

    @property
    def title(self) -> str:
        return 'Provisioning: %s' % self.provisioner.name

    def run(self):
        env = {'DEPLOY_OSTREE_%s' % key: value for key, value in self.provisioner.args.items()}
        exe = os.path.join(PROVISIONER_DIR, self.provisioner.name)
        run([exe, self.config.deployment_dir], check=True, env=env)

    @classmethod
    def is_relevant(cls, config: Config) -> bool:
        return bool(config.default_provisioners)

    @classmethod
    def get_steps(cls, config: Config) -> Sequence[DeployStep]:
        return [cls(config, provisioner) for provisioner in config.default_provisioners]
