# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os.path
import subprocess
import sys
from . import ProvisionerTestCase


def sh(cmd: str) -> str:
    proc = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    return proc.stdout.decode(sys.getfilesystemencoding())


class TestEtcNetworkInterfaces(ProvisionerTestCase):
    PROVISIONER = 'cloud-init'

    def test_should_have_execute_bit(self):
        self.assertTrue(self.is_executable)

    def test_should_create_etc_dir_if_necessary(self):
        self.provision()

        self.assertTrue(os.path.isdir(self.path('var', 'lib', 'cloud', 'seed', 'nocloud')))

    def test_should_create_file_for_meta_data(self):
        self.provision({'meta_data': 'instance-id: some-uuid'})

        with open(self.path('var', 'lib', 'cloud', 'seed', 'nocloud', 'meta-data'), 'r') as f:
            self.assertEqual(
                f.read().strip(),
                'instance-id: some-uuid')

    def test_should_create_file_for_user_data(self):
        self.provision({'user_data': 'runcmd:\n  - [ modprobe, fuse ]'})

        with open(self.path('var', 'lib', 'cloud', 'seed', 'nocloud', 'user-data'), 'r') as f:
            self.assertEqual(
                f.read().strip(),
                'runcmd:\n'
                '  - [ modprobe, fuse ]')
