# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from . import ProvisionerTestCase


class TestCreateUser(ProvisionerTestCase):
    PROVISIONER = 'create-user'

    def test_should_have_execute_bit(self):
        self.assertTrue(self.is_executable)
