# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from io import StringIO
from unittest import mock, TestCase
from deploy_ostree.config import Config
from deploy_ostree.steps.deploy import Deploy, get_root_fs


class TestDeploy(TestCase):
    @mock.patch('deploy_ostree.steps.deploy.run')
    @mock.patch('deploy_ostree.steps.deploy.get_root_fs')
    def test_should_deploy_commit(self, get_root_fs_mock: mock.Mock, run_mock: mock.Mock):
        cfg = Config('url', 'fedora/28/x86_64/atomic-host', remote='fedora-atomic', stateroot='atomic-host')
        get_root_fs_mock.return_value = '/dev/mapper/atomic-root'

        steps = Deploy.get_steps(cfg)
        for step in steps:
            step.run()

        run_mock.assert_called_once_with([
                'ostree',
                'admin',
                'deploy',
                '--os=atomic-host',
                'fedora-atomic:fedora/28/x86_64/atomic-host',
                '--karg=root=/dev/mapper/atomic-root'
            ], check=True)

    def test_should_be_relevant(self):
        self.assertTrue(Deploy.is_relevant(mock.Mock()))

    def test_title_should_be_str(self):
        self.assertIsInstance(Deploy(mock.Mock()).title, str)


class TestGetRootFS(TestCase):
    @mock.patch('deploy_ostree.steps.deploy.open')
    @mock.patch('sys.getfilesystemencoding')
    def test_should_read_root_arg_from_proc_cmdline(self, encoding_mock: mock.Mock, mock_open: mock.Mock):
        mock_open.return_value = StringIO('root=/dev/sda1')
        encoding_mock.return_value = 'fs-encoding'

        rootfs = get_root_fs()

        mock_open.assert_called_once_with('/proc/cmdline', 'r', encoding='fs-encoding')
        self.assertEqual('/dev/sda1', rootfs)

    @mock.patch('deploy_ostree.steps.deploy.open')
    @mock.patch('sys.getfilesystemencoding')
    def test_should_parse_root_arg_from_multiple(self, encoding_mock: mock.Mock, mock_open: mock.Mock):
        mock_open.return_value = StringIO(
            'BOOT_IMAGE=/vmlinuz-4.9.0-4-amd64 '
            'root=/dev/mapper/debian--9--vg-root '
            'ro debian-installer=en_US.UTF-8 quiet')
        encoding_mock.return_value = 'fs-encoding'

        rootfs = get_root_fs()

        mock_open.assert_called_once_with('/proc/cmdline', 'r', encoding='fs-encoding')
        self.assertEqual('/dev/mapper/debian--9--vg-root', rootfs)

    @mock.patch('deploy_ostree.steps.deploy.open')
    @mock.patch('sys.getfilesystemencoding')
    def test_should_return_empty_string_if_no_root_arg(self, encoding_mock: mock.Mock, mock_open: mock.Mock):
        mock_open.return_value = StringIO(
            'BOOT_IMAGE=/vmlinuz-4.9.0-4-amd64 '
            'ro debian-installer=en_US.UTF-8 quiet')
        encoding_mock.return_value = 'fs-encoding'

        rootfs = get_root_fs()

        mock_open.assert_called_once_with('/proc/cmdline', 'r', encoding='fs-encoding')
        self.assertEqual('', rootfs)
