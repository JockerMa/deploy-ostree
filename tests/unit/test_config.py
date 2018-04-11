# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from unittest import TestCase
from deploy_ostree import config


class TestConfig(TestCase):
    def test_fails(self):
        config.Config()
        self.fail()
