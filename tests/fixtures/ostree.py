# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os
import shutil
from .fixture import Fixture
from .. import ostree


class OSTreeFixture(Fixture):
    def setUp(self):
        if os.path.exists('/ostree'):
            raise Exception("these tests don't work with an existing /ostree folder")
        ostree(['admin', 'init-fs', '/'])

    def tearDown(self):
        shutil.rmtree('/ostree')
        shutil.rmtree('/etc/ostree/remotes.d')
        for elem in os.listdir('/boot'):
            path = os.path.join('/boot', elem)
            if elem == 'loader':
                os.remove(path)
            elif elem == 'ostree' or elem.startswith('loader'):
                shutil.rmtree(path)
