# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os.path
from .. import deploy_ostree, ostree
from ..fixtures import FixtureTestCase, OSTreeFixture

TESTS_DIR = os.path.dirname(__file__)


class TestSimpleDeploy(FixtureTestCase):
    url = 'http://mirror.centos.org/centos/7/atomic/x86_64/repo'
    ref = 'centos-atomic-host/7/x86_64/standard'

    FIXTURES = [OSTreeFixture]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        deploy_ostree([os.path.join(TESTS_DIR, 'simple-deploy.json')])

    def test_should_add_randomly_named_remote(self):
        remote = ostree(['remote', 'list']).stdout.strip()
        url = ostree(['remote', 'show-url', remote]).stdout.strip()
        self.assertEqual(
            self.url,
            url)

    def test_should_pull_ref_from_remote(self):
        remote = ostree(['remote', 'list']).stdout.strip()
        refs = [ref.strip() for ref in ostree(['refs']).stdout.splitlines()]
        self.assertIn('%s:%s' % (remote, self.ref), refs)

    def test_should_create_randomly_named_stateroot(self):
        deploy_dir = '/ostree/deploy'
        elems = os.listdir(deploy_dir)
        self.assertEqual(1, len(elems))
        stateroot = elems[0]
        self.assertTrue(os.path.isdir(os.path.join(deploy_dir, stateroot)))
