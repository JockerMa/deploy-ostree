# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os.path
from unittest import skip
from .. import deploy_ostree
from ..fixtures import FixtureTestCase, OSTreeFixture, OSTreeCommitFixture

TESTS_DIR = os.path.dirname(__file__)


@skip('WIP')
class TestDeployWithProvisioners(FixtureTestCase):
    FIXTURES = [OSTreeFixture(), OSTreeCommitFixture()]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        deploy_ostree([os.path.join(TESTS_DIR, 'default-provisioners.json')])

    def test_should_copy_etc_fstab_from_host(self):
        deployment = self.get_deployment()
        with open(os.path.join(deployment, 'etc', 'fstab'), 'r') as f:
            deployment_fstab = f.read()
        with open('/etc/fstab', 'r') as f:
            host_fstab = f.read()
        self.assertEqual(deployment_fstab, host_fstab)

    def test_should_create_interfaces_file_for_loopback(self):
        deployment = self.get_deployment()
        with open(os.path.join(deployment, 'etc', 'network', 'interfaces.d', 'lo'), 'r') as f:
            self.assertEqual(f.read().strip(), 'auto lo\niface lo inet loopback')

    def test_should_create_interfaces_file_for_specified_interface(self):
        deployment = self.get_deployment()
        with open(os.path.join(deployment, 'etc', 'network', 'interfaces.d', 'default'), 'r') as f:
            self.assertEqual(f.read().strip(), 'allow-hotplug enp0s3\niface enp0s3 inet dhcp')

    def get_deployment(self):
        deployments_dir = '/ostree/deploy/test-stateroot/deploy'
        elems = [elem for elem in os.listdir(deployments_dir) if not elem.endswith('.origin')]
        self.assertEqual(len(elems), 1)
        return os.path.join(deployments_dir, elems[0])
