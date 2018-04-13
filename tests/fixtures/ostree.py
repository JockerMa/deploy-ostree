# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os
import shutil
from .fixture import Fixture
from .. import ostree


class OSTreeFixture(Fixture):
    @classmethod
    def setUpClass(cls):
        os.makedirs('/ostree/repo', mode=0o755)
        ostree(['init', '--repo=/ostree/repo'])

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree('/ostree')
        shutil.rmtree('/etc/ostree/remotes.d')
