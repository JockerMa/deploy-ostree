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
    PROVISIONER = 'netplan'

    def test_should_have_execute_bit(self):
        self.assertTrue(self.is_executable)

    def test_should_create_etc_dir_if_necessary(self):
        self.provision()

        self.assertTrue(os.path.isdir(self.path('etc', 'netplan')))

    def test_should_create_file_for_specified_interface(self):
        self.provision({'netplan_config': 'network:\n  version: 2\n  renderer: networkd\n  ethernets:\n    enp0s3:\n      dhcp4: true\n'})

        with open(self.path('etc', 'netplan', 'netplan.yaml'), 'r') as f:
            self.assertEqual(
                f.read().strip(),
                'network:\n'
                '  version: 2\n'
                '  renderer: networkd\n'
                '  ethernets:\n'
                '    enp0s3:\n'
                '      dhcp4: true')
