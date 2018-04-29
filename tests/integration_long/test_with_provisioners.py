# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import crypt
import os.path
from typing import Iterator
from unittest import skip
from .. import deploy_ostree
from ..fixtures import FixtureTestCase, OSTreeFixture

TESTS_DIR = os.path.dirname(__file__)


class PasswdEntry:
    def __init__(self, line: str) -> None:
        parts = line.split(':')
        self.name = parts[0]
        self.pwd = parts[1]
        self.uid = parts[2]
        self.gid = parts[3]
        self.home = parts[5]
        self.shell = parts[6]


class ShadowEntry:
    def __init__(self, line: str) -> None:
        parts = line.split(':')
        self.name = parts[0]
        self.pwd = parts[1]

    def password_is(self, password: str) -> bool:
        crypted = crypt.crypt(password, self.pwd)
        return crypted == self.pwd


def passwd(deployment_dir: str) -> Iterator[PasswdEntry]:
    with open(os.path.join(deployment_dir, 'etc', 'passwd')) as f:
        for line in f:
            yield PasswdEntry(line.strip())


def shadow(deployment_dir: str) -> Iterator[ShadowEntry]:
    with open(os.path.join(deployment_dir, 'etc', 'shadow')) as f:
        for line in f:
            yield ShadowEntry(line.strip())


class TestDeployWithProvisioners(FixtureTestCase):
    FIXTURES = [OSTreeFixture()]

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

    def test_should_set_root_password(self):
        deployment = self.get_deployment()
        for spwd in shadow(deployment):
            if spwd.name == 'root':
                self.assertTrue(spwd.password_is('rootpw'))

    @skip('TBD')
    def test_should_create_user(self):
        deployment = self.get_deployment()
        pwd_entry = None
        shadow_entry = None

        for pwd in passwd(deployment):
            if pwd.name == 'testuser':
                pwd_entry = pwd
        for spwd in shadow(deployment):
            if spwd.name == 'testuser':
                shadow_entry = spwd

        self.assertIsNotNone(pwd_entry)
        self.assertIsNotNone(shadow_entry)
        self.assertTrue(shadow_entry.password_is('testpw'))

    def get_deployment(self):
        deployments_dir = '/ostree/deploy/test-stateroot/deploy'
        elems = [elem for elem in os.listdir(deployments_dir) if not elem.endswith('.origin')]
        self.assertEqual(len(elems), 1)
        return os.path.join(deployments_dir, elems[0])
