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
        self.assert_files_equal('/etc/fstab', self.deployment('etc', 'fstab'))

    def test_should_create_interfaces_file_for_loopback(self):
        self.assert_file_content(
            self.deployment('etc', 'network', 'interfaces.d', 'lo'),
            'auto lo\niface lo inet loopback\n'
        )

    def test_should_create_interfaces_file_for_specified_interface(self):
        self.assert_file_content(
            self.deployment('etc', 'network', 'interfaces.d', 'default'),
            'allow-hotplug enp0s3\niface enp0s3 inet dhcp\n'
        )

    def test_should_set_root_password(self):
        self.assertTrue(self.get_shadow('root').password_is('rootpw'))

    def test_should_create_test_user(self):
        self.assertIsNotNone(self.get_pwd('testuser'))
        self.assertTrue(self.get_shadow('testuser').password_is('testpw'))

    def test_should_create_test_user_with_default_shell(self):
        self.assertEqual(self.get_pwd('testuser').shell, '')

    def test_should_create_user_with_custom_shell(self):
        self.assertEqual(self.get_pwd('shell-user').shell, '/my/custom/shell')

    def test_should_create_home_directories(self):
        self.assertTrue(os.path.isfile(self.var('home', 'testuser', '.bashrc')))
        self.assertTrue(os.path.isfile(self.var('home', 'shell-user', '.bashrc')))

    def test_should_copy_authorized_keys_file(self):
        ssh_dir = self.var('home', 'testuser', '.ssh')
        auth_keys = os.path.join(ssh_dir, 'authorized_keys')
        pwd = self.get_pwd('testuser')

        self.assert_file_mode(ssh_dir, pwd.uid, 0o700)
        self.assert_file_mode(auth_keys, pwd.uid, 0o600)
        self.assert_file_content(auth_keys, 'authorized keys file')

    def test_should_create_sudoers_file(self):
        sudoers_file = self.deployment('etc', 'sudoers.d', 'testuser-passwordless-sudo')
        self.assert_file_mode(sudoers_file, 0, 0o440)
        self.assert_file_content(sudoers_file, 'testuser ALL=(ALL) NOPASSWD: ALL\n')

    # helper functions
    def get_pwd(self, name) -> PasswdEntry:
        for pwd in passwd(self.deployment()):
            if pwd.name == name:
                return pwd
        self.fail('no passwd entry for %s' % name)

    def get_shadow(self, name) -> ShadowEntry:
        for spwd in shadow(self.deployment()):
            if spwd.name == name:
                return spwd
        self.fail('no shadow entry for %s' % name)

    def var(self, *args):
        return os.path.join('/ostree', 'deploy', 'test-stateroot', 'var', *args)

    def deployment(self, *args):
        deployments_dir = '/ostree/deploy/test-stateroot/deploy'
        elems = [elem for elem in os.listdir(deployments_dir) if not elem.endswith('.origin')]
        self.assertEqual(len(elems), 1)
        deployment = os.path.join(deployments_dir, elems[0])
        return os.path.join(deployment, *args)

    # helper asserts
    def assert_file_content(self, path, expected_content):
        with open(path, 'r') as f:
            file_content = f.read()
        self.assertEqual(file_content, expected_content)

    def assert_files_equal(self, path1, path2):
        with open(path1, 'r') as f:
            self.assert_file_content(path2, f.read())

    def assert_file_mode(self, path, owner, mode):
        statresult = os.stat(path)
        self.assertEqual(stat.S_IMODE(statresult.st_mode), mode)
        self.assertEqual(statresult.st_uid, owner)
        self.assertEqual(statresult.st_gid, owner)
