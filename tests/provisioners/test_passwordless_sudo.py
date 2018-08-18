# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os
import stat
from . import ProvisionerTestCase


class TestPasswordlessSudo(ProvisionerTestCase):
    PROVISIONER = 'passwordless-sudo'

    def test_should_have_execute_bit(self):
        self.assertTrue(self.is_executable)

    def test_should_fail_if_no_user_is_specified(self):
        with self.assertRaises(RuntimeError):
            self.provision()

    def test_should_create_sudoers_file_with_correct_permissions(self):
        self.provision({'user': 'testuser'})

        self.assert_file_mode(self.path('etc', 'sudoers.d'), 0o750)

        sudoers_file = self.path('etc', 'sudoers.d', 'testuser-passwordless-sudo')
        self.assert_file_mode(sudoers_file, 0o440)
        self.assert_file_content(sudoers_file, 'testuser ALL=(ALL) NOPASSWD: ALL\n')

    def assert_file_mode(self, path, mode):
        statresult = os.stat(path)
        self.assertEqual(stat.S_IMODE(statresult.st_mode), mode)

    def assert_file_content(self, path, expected_content):
        with open(path, 'r') as f:
            content = f.read()
        self.assertEqual(content, expected_content)
