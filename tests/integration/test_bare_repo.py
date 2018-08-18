# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os.path
import shutil
from .. import deploy_ostree, ostree
from ..fixtures import FixtureTestCase, OSTreeFixture, OSTreeCommitFixture

TESTS_DIR = os.path.dirname(__file__)


class TestBareRepo(FixtureTestCase):
    ref = 'test-commit'
    remote = 'test-remote'

    commit_fixture = OSTreeCommitFixture(mode='bare-user', http=False)
    FIXTURES = [OSTreeFixture(), commit_fixture]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        deploy_config = os.path.join(cls.commit_fixture.repo_dir.name, 'deploy.json')
        shutil.copy(os.path.join(TESTS_DIR, 'bare-repo.json'), deploy_config)
        deploy_ostree([deploy_config])

    def test_should_pull_ref_from_remote(self):
        refs = [ref.strip() for ref in ostree(['refs']).stdout_str.splitlines()]
        self.assertIn('%s:%s' % (self.remote, self.ref), refs)
