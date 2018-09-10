# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os
from typing import Sequence
import deploy_ostree
from . import DeployStep
from ..config import Config, ProvisionerConfig
from ..run import run


PROVISIONER_DIR = os.path.join(os.path.dirname(deploy_ostree.__file__), 'default-provisioners')


def shell_provisioner(name):
    exe = os.path.join(PROVISIONER_DIR, name)

    def provision(deployment_dir, args):
        env = {'DEPLOY_OSTREE_%s' % key: value for key, value in args.items()}
        run([exe, deployment_dir], check=True, env=env)

    return provision


class DefaultProvisioner(DeployStep):
    PROVISIONERS = {
        'authorized-keys': shell_provisioner('authorized-keys'),
        'create-user': shell_provisioner('create-user'),
        'etc-fstab': shell_provisioner('etc-fstab'),
        'etc-network-interfaces': shell_provisioner('etc-network-interfaces'),
        'passwordless-sudo': shell_provisioner('passwordless-sudo'),
        'root-password': shell_provisioner('root-password'),
    }

    def __init__(self, config: Config, provisioner: ProvisionerConfig) -> None:
        self.config = config
        self.provisioner = provisioner

    @property
    def title(self) -> str:
        return 'Provisioning: %s' % self.provisioner.name

    def run(self):
        self.PROVISIONERS[self.provisioner.name](self.config.deployment_dir, self.provisioner.args)

    @classmethod
    def is_relevant(cls, config: Config) -> bool:
        return bool(config.default_provisioners)

    @classmethod
    def get_steps(cls, config: Config) -> Sequence[DeployStep]:
        return [cls(config, provisioner) for provisioner in config.default_provisioners]
