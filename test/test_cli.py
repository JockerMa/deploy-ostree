# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from unittest import TestCase
from util import deploy_ostree


class TestHelp(TestCase):
    def test_should_print_help_and_exit_if_called_with_no_arguments(self):
        result = deploy_ostree([])

        self.assertIn(
            b'deploy-ostree - deploy and configure an OSTree commit',
            result.stdout)
        self.assertEqual(1, result.returncode)
