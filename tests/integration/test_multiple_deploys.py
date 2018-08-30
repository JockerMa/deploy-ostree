# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os.path
from .. import deploy_ostree, ostree
from ..fixtures import FixtureTestCase, OSTreeFixture, OSTreeCommitFixture

TESTS_DIR = os.path.dirname(__file__)


class TestMultipleDeploys(FixtureTestCase):
    FIXTURES = [OSTreeFixture(), OSTreeCommitFixture()]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        deploy_ostree([os.path.join(TESTS_DIR, 'simple-deploy.json')])
        deploy_ostree([os.path.join(TESTS_DIR, 'simple-deploy.json')])

    def test_should_add_randomly_named_remotes(self):
        remotes = self.get_remotes()
        self.assertEqual(2, len(remotes))
        for remote in remotes:
            url = ostree(['remote', 'show-url', remote]).stdout_str.strip()
            self.assertEqual('http://localhost:8000/', url)

    def test_should_pull_ref_from_remotes(self):
        refs = [ref.strip() for ref in ostree(['refs']).stdout_str.splitlines()]
        self.assertGreaterEqual(len(refs), 2)
        for remote in self.get_remotes():
            self.assertIn('%s:test-commit' % remote, refs)

    def test_should_create_stateroots(self):
        stateroots = os.listdir('/ostree/deploy')
        self.assertEqual(2, len(stateroots))

    def test_should_create_boot_loader_entries(self):
        stateroots = os.listdir('/ostree/deploy')
        entries = os.listdir('/boot/loader/entries')
        self.assertEqual(2, len(entries))
        for stateroot in stateroots:
            self.assertTrue(any(stateroot in entry for entry in entries))

    def get_remotes(self):
        return [line.strip() for line in ostree(['remote', 'list']).stdout_str.splitlines()]
