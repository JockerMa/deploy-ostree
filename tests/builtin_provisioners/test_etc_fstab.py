# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os
from . import ProvisionerTestCase


class TestEtcFstab(ProvisionerTestCase):
    PROVISIONER = 'etc-fstab'

    def test_should_have_execute_bit(self):
        self.assertTrue(self.is_executable)

    def test_should_copy_fstab_from_host(self):
        self.makedirs('etc')

        self.provision()

        self.should_have_copied_fstab()

    def test_should_create_etc_dir_if_necessary(self):
        self.provision()

        self.assertTrue(os.path.isdir(self.path('etc')))
        self.should_have_copied_fstab()

    def test_should_replace_file_if_it_exists(self):
        self.makedirs('etc')
        with open(self.path('etc', 'fstab'), 'w') as f:
            f.write('test')

        self.provision()

        self.should_have_copied_fstab()

    def should_have_copied_fstab(self):
        with open('/etc/fstab', 'r') as f:
            host_fstab = f.read()
        with open(self.path('etc', 'fstab'), 'r') as f:
            target_fstab = f.read()
        self.assertEqual(target_fstab, host_fstab)
