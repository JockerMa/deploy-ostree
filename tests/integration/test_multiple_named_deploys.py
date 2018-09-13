# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os.path
from .. import deploy_ostree, ostree
from ..fixtures import FixtureTestCase, OSTreeFixture, OSTreeCommitFixture

TESTS_DIR = os.path.dirname(__file__)


class TestMultipleNamedDeploys(FixtureTestCase):
    url = 'http://localhost:8000/'
    ref = 'test-commit'
    remote = 'test-remote'

    FIXTURES = [OSTreeFixture(), OSTreeCommitFixture()]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        deploy_ostree([os.path.join(TESTS_DIR, 'named-deploy.json')])
        deploy_ostree([os.path.join(TESTS_DIR, 'named-deploy.json')])

    def test_should_add_single_named_remote(self):
        url = ostree(['remote', 'show-url', self.remote]).stdout.strip()
        self.assertEqual(
            self.url,
            url)

    def test_should_pull_ref_from_remote(self):
        refs = [ref.strip() for ref in ostree(['refs']).stdout.splitlines()]
        self.assertIn('%s:%s' % (self.remote, self.ref), refs)

    def test_should_create_single_named_stateroot(self):
        self.assertTrue(os.path.isdir('/ostree/deploy/test-stateroot/var'))

    def test_should_create_boot_loader_entries(self):
        entries = os.listdir('/boot/loader/entries')
        self.assertEqual(2, len(entries))
        self.assertTrue(all('test-stateroot' in entry for entry in entries))
