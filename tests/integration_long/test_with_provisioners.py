# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import crypt
import os
import stat
from typing import Iterator
from .. import deploy_ostree
from ..fixtures import FixtureTestCase, OSTreeFixture

TESTS_DIR = os.path.dirname(__file__)


class PasswdEntry:
    def __init__(self, line: str) -> None:
        parts = line.split(':')
        self.name = parts[0]
        self.pwd = parts[1]
        self.uid = int(parts[2])
        self.gid = int(parts[3])
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
        with open('/authorized_keys', 'w') as f:
            f.write('authorized keys file')
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

    def test_should_create_test_user(self):
        pwd_entry = self.get_pwd('testuser')
        shadow_entry = self.get_shadow('testuser')
        self.assertIsNotNone(pwd_entry)
        self.assertTrue(shadow_entry.password_is('testpw'))

    def test_should_create_test_user_with_default_shell(self):
        testuser = self.get_pwd('testuser')
        self.assertEqual(testuser.shell, '')

    def test_should_create_user_with_custom_shell(self):
        pwd = self.get_pwd('shell-user')
        self.assertEqual(pwd.shell, '/my/custom/shell')

    def test_should_create_home_directories(self):
        homedir = os.path.join('/ostree', 'deploy', 'test-stateroot', 'var', 'home')
        self.assertTrue(os.path.isfile(os.path.join(homedir, 'testuser', '.bashrc')))
        self.assertTrue(os.path.isfile(os.path.join(homedir, 'shell-user', '.bashrc')))

    def test_should_copy_authorized_keys_file(self):
        ssh_dir = os.path.join('/ostree', 'deploy', 'test-stateroot', 'var', 'home', 'testuser', '.ssh')
        pwd = self.get_pwd('testuser')

        ssh_dir_stat = os.stat(ssh_dir)
        self.assertTrue(stat.S_ISDIR(ssh_dir_stat.st_mode))
        self.assertEqual(stat.S_IMODE(ssh_dir_stat.st_mode), 0o700)
        self.assertEqual(ssh_dir_stat.st_uid, pwd.uid)
        self.assertEqual(ssh_dir_stat.st_gid, pwd.gid)

        keysfile_stat = os.stat(os.path.join(ssh_dir, 'authorized_keys'))
        self.assertTrue(stat.S_ISREG(keysfile_stat.st_mode))
        self.assertEqual(stat.S_IMODE(keysfile_stat.st_mode), 0o600)
        self.assertEqual(keysfile_stat.st_uid, pwd.uid)
        self.assertEqual(keysfile_stat.st_gid, pwd.gid)

    def get_pwd(self, name) -> PasswdEntry:
        for pwd in passwd(self.get_deployment()):
            if pwd.name == name:
                return pwd
        self.fail('no passwd entry for %s' % name)

    def get_shadow(self, name) -> ShadowEntry:
        for spwd in shadow(self.get_deployment()):
            if spwd.name == name:
                return spwd
        self.fail('no shadow entry for %s' % name)

    def get_deployment(self):
        deployments_dir = '/ostree/deploy/test-stateroot/deploy'
        elems = [elem for elem in os.listdir(deployments_dir) if not elem.endswith('.origin')]
        self.assertEqual(len(elems), 1)
        return os.path.join(deployments_dir, elems[0])
