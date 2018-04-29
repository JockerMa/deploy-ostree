# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from . import ProvisionerTestCase


# This provisioner is really hard to test in isolation.
class TestCreateUser(ProvisionerTestCase):
    PROVISIONER = 'create-user'

    def test_should_fail_if_no_arguments_are_given(self):
        with self.assertRaises(RuntimeError):
            self.provision()

    def test_should_fail_if_no_username_argument_is_given(self):
        with self.assertRaises(RuntimeError):
            self.provision({'password': 'password'})

    def test_should_fail_if_no_password_argument_is_given(self):
        with self.assertRaises(RuntimeError):
            self.provision({'username': 'user'})
