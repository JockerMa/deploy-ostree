# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from unittest import TestCase
from .. import deploy_ostree


class TestHelp(TestCase):
    def test_should_print_error_and_exit_if_called_with_no_arguments(self):
        result = deploy_ostree([], check=False, capture_output=True)

        self.assertIn('the following arguments are required', result.stderr)
        self.assertEqual(2, result.exitcode)

    def test_should_print_help_and_exit_if_called_with_help_flag(self):
        result = deploy_ostree(['--help'], capture_output=True)

        self.assertIn('deploy-ostree', result.stdout)
        self.assertIn('deploy and configure an OSTree commit', result.stdout)
        self.assertEqual(0, result.exitcode)

    def test_should_print_help_and_exit_if_called_with_h_flag(self):
        result = deploy_ostree(['-h'], capture_output=True)

        self.assertIn('deploy-ostree', result.stdout)
        self.assertIn('deploy and configure an OSTree commit', result.stdout)
        self.assertEqual(0, result.exitcode)
