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
    PROVISIONER = 'systemd-networkd'

    def test_should_have_execute_bit(self):
        self.assertTrue(self.is_executable)

    def test_should_create_etc_dir_if_necessary(self):
        self.provision()

        self.assertTrue(os.path.isdir(self.path('etc', 'systemd', 'network')))

    def test_should_create_file_for_default_interface(self):
        iface = sh('sed -n 2p /proc/net/route | cut -f1').strip()

        self.provision()

        with open(self.path('etc', 'systemd', 'network', "{0}.network".format(iface)), 'r') as f:
            self.assertEqual(
                f.read().strip(),
                '[Match]\n'
                'Name=%(iface)s\n'
                '[Network]\n'
                'DHCP=yes' % {'iface': iface})

    def test_should_create_file_for_specified_interface(self):
        self.provision({'interface': 'test-interface'})

        with open(self.path('etc', 'systemd', 'network', 'test-interface.network'), 'r') as f:
            self.assertEqual(
                f.read().strip(),
                '[Match]\n'
                'Name=test-interface\n'
                '[Network]\n'
                'DHCP=yes')
