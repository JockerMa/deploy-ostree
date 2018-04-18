# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from . import ProvisionerTestCase


# This provisioner is really hard to test in isolation.
class TestRootPassword(ProvisionerTestCase):
    PROVISIONER = 'root-password'

    def test_should_fail_if_no_password_argument_is_given(self):
        with self.assertRaises(RuntimeError):
            self.provision()
