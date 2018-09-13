# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os.path
from deploy_ostree.run import run
from .. import deploy_ostree
from ..fixtures import FixtureTestCase, OSTreeFixture, OSTreeCommitFixture

TESTS_DIR = os.path.dirname(__file__)


class TestFailingProvisioner(FixtureTestCase):
    FIXTURES = [OSTreeFixture(), OSTreeCommitFixture()]

    def test_should_fail_and_clean_up_safely(self):
        result = deploy_ostree(
            [os.path.join(TESTS_DIR, 'failing-provisioner.json')],
            check=False,
            capture_output=True
        )

        # we expect chpasswd to try to run, but not work
        self.assertIn('chpasswd', result.stderr)
        self.assertEqual(result.exitcode, 1)
        var_mount = os.path.join(self.get_deployment_dir(), 'var')
        mount = run(['mount'], capture_output=True)
        self.assertNotIn(' %s ' % var_mount, mount.stdout)

    def get_deployment_dir(self):
        deployments_dir = os.path.join('/ostree', 'deploy', 'test-stateroot', 'deploy')
        elems = [elem for elem in os.listdir(deployments_dir) if not elem.endswith('.origin')]
        return os.path.join(deployments_dir, elems[0])
