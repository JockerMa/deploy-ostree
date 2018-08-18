# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os
from tempfile import TemporaryDirectory
from typing import Dict, Iterable, Optional  # noqa
from unittest import TestCase
import deploy_ostree
from deploy_ostree.run import run

PROVISIONER_DIR = os.path.join(os.path.dirname(deploy_ostree.__file__), 'default-provisioners')


class ProvisionerTestCase(TestCase):
    PROVISIONER = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tmpdir = None

    def setUp(self):
        self.tmpdir = TemporaryDirectory()

    def tearDown(self):
        if self.tmpdir:
            self.tmpdir.cleanup()

    def path(self, *args: Iterable[str]) -> str:
        if not self.tmpdir:
            raise Exception('work dir not set up')
        return os.path.join(self.tmpdir.name, *args)

    def makedirs(self, *args: Iterable[str]):
        os.makedirs(self.path(*args), mode=0o755, exist_ok=True)

    def provision(self, args: Dict[str, str]={}):
        env = {'DEPLOY_OSTREE_%s' % key: value for key, value in args.items()}
        run(
            [self.provisioner_path, self.path()],
            check=True,
            env=env
        )

    @property
    def provisioner_path(self):
        return os.path.join(PROVISIONER_DIR, self.PROVISIONER)

    @property
    def is_executable(self):
        return bool(os.access(self.provisioner_path, os.X_OK))
