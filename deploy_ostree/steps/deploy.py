# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os
import sys
from . import DeployStep, DeployError
from ..config import Config
from ..run import run


def get_root_fs() -> str:
    with open('/proc/cmdline', 'r', encoding=sys.getfilesystemencoding()) as f:
        args = f.read()  # type: str
    for arg in (arg.strip() for arg in args.split()):
        if arg.startswith('root='):
            return arg[5:]
    return ''


class Deploy(DeployStep):
    def __init__(self, cfg: Config) -> None:
        self.cfg = cfg
        self.ref = cfg.ref
        self.remote = cfg.remote
        self.stateroot = cfg.stateroot

    @property
    def title(self) -> str:
        return 'Deploying %s:%s' % (self.remote, self.ref)

    def run(self):
        deployments_dir = os.path.join('/ostree', 'deploy', self.stateroot, 'deploy')
        elems_before_deploy = set(os.listdir(deployments_dir))
        rootfs = get_root_fs()
        run([
            'ostree',
            'admin',
            'deploy',
            '--os=%s' % self.stateroot,
            '%s:%s' % (self.remote, self.ref),
            '--karg=root=%s' % rootfs
        ], check=True)
        elems_after_deploy = set(os.listdir(deployments_dir))
        new_elems = [elem for elem in elems_after_deploy - elems_before_deploy if not elem.endswith('.origin')]
        if len(new_elems) != 1:
            raise DeployError('could not determine new deployment directory')
        self.cfg.set_deployment_name(new_elems[0])
        print('==> New deployment:', new_elems[0])
