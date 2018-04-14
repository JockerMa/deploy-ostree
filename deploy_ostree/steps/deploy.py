# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import sys
from . import DeployStep
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
        self.ref = cfg.ref
        self.remote = cfg.remote
        self.stateroot = cfg.stateroot

    @property
    def title(self) -> str:
        return 'Deploying %s:%s' % (self.remote, self.ref)

    def run(self):
        rootfs = get_root_fs()
        run([
            'ostree',
            'admin',
            'deploy',
            '--os=%s' % self.stateroot,
            '%s:%s' % (self.remote, self.ref),
            '--karg=root=%s' % rootfs
        ], check=True)
