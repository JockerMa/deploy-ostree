# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os
import shutil
import subprocess
from .fixture import Fixture
from .. import ostree


def sh_silent(cmd):
    return subprocess.run(
        cmd,
        shell=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


class OSTreeFixture(Fixture):
    def setUp(self):
        if os.path.exists('/ostree') and len(os.listdir('/ostree')) > 0:
            raise Exception("these tests don't work with an existing /ostree folder")
        ostree(['admin', 'init-fs', '/'])

    def tearDown(self):
        sh_silent('chattr -R -i /ostree')
        sh_silent('rm -rf /ostree/*')
        shutil.rmtree('/etc/ostree/remotes.d')
        for elem in os.listdir('/boot'):
            path = os.path.join('/boot', elem)
            if elem == 'loader':
                os.remove(path)
            elif elem == 'ostree' or elem.startswith('loader'):
                shutil.rmtree(path)
