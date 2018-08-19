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
    PROVISIONER = 'etc-network-interfaces'

    def test_should_have_execute_bit(self):
        self.assertTrue(self.is_executable)

    def test_should_create_lo_file(self):
        self.makedirs('etc', 'network', 'interfaces.d')

        self.provision()

        with open(self.path('etc', 'network', 'interfaces.d', 'lo'), 'r') as f:
            self.assertEqual(
                f.read().strip(),
                'auto lo\n'
                'iface lo inet loopback')

    def test_should_create_etc_dir_if_necessary(self):
        self.provision()

        self.assertTrue(os.path.isdir(self.path('etc', 'network', 'interfaces.d')))

    def test_should_create_file_for_default_interface(self):
        iface = sh('sed -n 2p /proc/net/route | cut -f1').strip()

        self.provision()

        with open(self.path('etc', 'network', 'interfaces.d', iface), 'r') as f:
            self.assertEqual(
                f.read().strip(),
                'allow-hotplug %(iface)s\n'
                'iface %(iface)s inet dhcp' % {'iface': iface})

    def test_should_create_file_for_specified_interface(self):
        self.provision({'interface': 'test-interface'})

        with open(self.path('etc', 'network', 'interfaces.d', 'test-interface'), 'r') as f:
            self.assertEqual(
                f.read().strip(),
                'allow-hotplug test-interface\n'
                'iface test-interface inet dhcp')
