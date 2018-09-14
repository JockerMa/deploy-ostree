# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import pytest
import os.path
from .. import deploy_ostree, ostree
from ..fixtures import FixtureTestCase, OSTreeFixture, OSTreeCommitFixture

TESTS_DIR = os.path.dirname(__file__)


@pytest.mark.needs_isolation
class TestExistingRemote(FixtureTestCase):
    FIXTURES = [OSTreeFixture(), OSTreeCommitFixture()]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        ostree(['remote', 'add', 'test-remote', 'file:/some/path'])
        deploy_ostree([os.path.join(TESTS_DIR, 'existing-remote.json')])

    def test_should_replace_remote(self):
        url = ostree(['remote', 'show-url', 'test-remote']).stdout.strip()
        self.assertEqual(
            'http://localhost:8000/',
            url
        )
