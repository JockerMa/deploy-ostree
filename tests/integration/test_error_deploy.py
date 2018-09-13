# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os.path
from unittest import TestCase
from .. import deploy_ostree

TESTS_DIR = os.path.dirname(__file__)


class TestErrorDeploy(TestCase):
    def test_should_report_process_errors_concisely(self):
        result = deploy_ostree([os.path.join(TESTS_DIR, 'error-deploy.json')], check=False, capture_output=True)

        self.assertNotIn('Traceback (most recent call last):', result.stderr)
        self.assertEqual(result.exitcode, 1)
