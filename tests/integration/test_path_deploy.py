# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import pytest
import os.path
import shutil
from .. import deploy_ostree, ostree
from ..fixtures import FixtureTestCase, OSTreeFixture, OSTreeCommitFixture

TESTS_DIR = os.path.dirname(__file__)


@pytest.mark.needs_isolation
class TestPathDeploy(FixtureTestCase):
    ref = 'test-commit'
    remote = 'test-remote'

    commit_fixture = OSTreeCommitFixture()
    FIXTURES = [OSTreeFixture(), commit_fixture]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        deploy_config = os.path.join(cls.commit_fixture.repo_dir.name, 'deploy.json')
        shutil.copy(os.path.join(TESTS_DIR, 'path-deploy.json'), deploy_config)
        deploy_ostree([deploy_config])

    def test_should_add_named_remote(self):
        url = ostree(['remote', 'show-url', self.remote]).stdout.strip()
        self.assertEqual(url, 'file://%s' % self.commit_fixture.repo_dir.name)

    def test_should_pull_ref_from_remote(self):
        refs = [ref.strip() for ref in ostree(['refs']).stdout.splitlines()]
        self.assertIn('%s:%s' % (self.remote, self.ref), refs)

    def test_should_create_named_stateroot(self):
        self.assertTrue(os.path.isdir('/ostree/deploy/test-stateroot/var'))

    def test_should_deploy_commit(self):
        deployments_dir = '/ostree/deploy/test-stateroot/deploy'
        elems = [elem for elem in os.listdir(deployments_dir) if not elem.endswith('.origin')]
        self.assertEqual(1, len(elems))
        deployment = os.path.join(deployments_dir, elems[0])
        self.assertTrue(os.path.isfile(os.path.join(deployment, 'etc', 'os-release')))
