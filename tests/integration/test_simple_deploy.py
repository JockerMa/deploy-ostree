# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os.path
from .. import deploy_ostree, ostree
from ..fixtures import FixtureTestCase, OSTreeFixture, OSTreeCommitFixture

TESTS_DIR = os.path.dirname(__file__)


class TestSimpleDeploy(FixtureTestCase):
    FIXTURES = [OSTreeFixture(), OSTreeCommitFixture()]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        deploy_ostree([os.path.join(TESTS_DIR, 'simple-deploy.json')])

    def test_should_add_randomly_named_remote(self):
        remote = ostree(['remote', 'list']).stdout_str.strip()
        url = ostree(['remote', 'show-url', remote]).stdout_str.strip()
        self.assertEqual(
            'http://localhost:8000/',
            url)

    def test_should_pull_ref_from_remote(self):
        remote = ostree(['remote', 'list']).stdout_str.strip()
        refs = [ref.strip() for ref in ostree(['refs']).stdout_str.splitlines()]
        self.assertIn('%s:test-commit' % remote, refs)

    def test_should_create_randomly_named_stateroot(self):
        stateroot = os.path.join(self.get_stateroot())
        self.assertTrue(os.path.isdir(os.path.join(stateroot, 'var')))

    def test_should_deploy_commit(self):
        deployments_dir = os.path.join(self.get_stateroot(), 'deploy')
        elems = [elem for elem in os.listdir(deployments_dir) if not elem.endswith('.origin')]
        self.assertEqual(1, len(elems))
        deployment = os.path.join(deployments_dir, elems[0])
        self.assertTrue(os.path.isfile(os.path.join(deployment, 'etc', 'os-release')))

    def test_should_create_boot_loader_entry(self):
        stateroot_name = os.path.basename(self.get_stateroot())
        entry_file = os.path.join('/boot/loader/entries', 'ostree-%s-0.conf' % stateroot_name)
        self.assertTrue(os.path.isfile(entry_file))

    def get_stateroot(self):
        deploy_dir = '/ostree/deploy'
        elems = os.listdir(deploy_dir)
        return os.path.join(deploy_dir, elems[0])
