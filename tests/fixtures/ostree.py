# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os
import shutil
import subprocess
from .fixture import Fixture
from .. import ostree


def sh(cmd, **kwargs):
    return subprocess.run(cmd, shell=True, **kwargs)


def sh_silent(cmd, **kwargs):
    return sh(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, **kwargs)


class OSTreeFixture(Fixture):
    def __init__(self, root_dir='/'):
        self.root_dir = root_dir

    @property
    def ostree(self):
        return os.path.join(self.root_dir, 'ostree')

    @property
    def boot(self):
        return os.path.join(self.root_dir, 'boot')

    def setUp(self):
        if os.path.exists(self.ostree) and len(os.listdir(self.ostree)) > 0:
            raise Exception("these tests don't work with an existing /ostree folder")
        os.makedirs(self.root_dir, mode=0o755, exist_ok=True)
        ostree(['admin', 'init-fs', self.root_dir])

    def tearDown(self):
        sh_silent('chattr -R -i %s' % self.ostree)
        sh('rm -rf %s/*' % self.ostree)
        sh('rm -rf %s' % os.path.join(self.root_dir, 'etc', 'ostree', 'remotes.d'))
        for elem in os.listdir(self.boot):
            path = os.path.join(self.boot, elem)
            if elem == 'loader':
                os.remove(path)
            elif elem == 'ostree' or elem.startswith('loader'):
                shutil.rmtree(path)
