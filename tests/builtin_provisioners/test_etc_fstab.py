# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from . import ProvisionerTestCase


# this is now a no-op, but we still want it to not raise an error
class TestEtcFstab(ProvisionerTestCase):
    PROVISIONER = 'etc-fstab'

    def test_should_have_execute_bit(self):
        self.assertTrue(self.is_executable)
