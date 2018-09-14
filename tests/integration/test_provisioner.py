# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import pytest
import os.path
from .. import deploy_ostree
from ..fixtures import FixtureTestCase, OSTreeFixture, OSTreeCommitFixture

TESTS_DIR = os.path.dirname(__file__)


@pytest.mark.needs_isolation
class TestProvisioner(FixtureTestCase):
    FIXTURES = [OSTreeFixture(), OSTreeCommitFixture()]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        deploy_ostree([os.path.join(TESTS_DIR, 'provisioner.json')])

    def test_should_run_provisioner_and_create_lo_config(self):
        path = self.deployment('etc', 'network', 'interfaces.d', 'lo')
        self.assertTrue(os.path.isfile(path))
        self.assert_file_contains(path, 'iface lo inet loopback')

    def test_should_run_provisioner_and_create_iface_config(self):
        path = self.deployment('etc', 'network', 'interfaces.d', 'enp0s3')
        self.assertTrue(os.path.isfile(path))
        self.assert_file_contains(path, 'iface enp0s3 inet dhcp')

    def deployment(self, *args):
        deployments_dir = '/ostree/deploy/test-stateroot/deploy'
        elems = [elem for elem in os.listdir(deployments_dir) if not elem.endswith('.origin')]
        self.assertEqual(len(elems), 1)
        deployment = os.path.join(deployments_dir, elems[0])
        return os.path.join(deployment, *args)

    def assert_file_contains(self, path, expected_content):
        with open(path, 'r') as f:
            content = f.read()
        self.assertIn(expected_content, content)
