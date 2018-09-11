# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from io import StringIO
import os
from unittest import mock, TestCase
from deploy_ostree.config import Config, Source
from deploy_ostree.steps.deploystep import DeployError
from deploy_ostree.steps.deploy import Deploy, get_root_fs


class TestDeploy(TestCase):
    @mock.patch('deploy_ostree.steps.deploy.run')
    @mock.patch('deploy_ostree.steps.deploy.get_root_fs')
    @mock.patch('os.listdir')
    def test_should_deploy_commit_and_set_deployment_folder(self, listdir_mock, get_root_fs_mock, run_mock):
        cfg = Config(Source.url('url'), 'fedora/28/x86_64/atomic-host', remote='fedora-atomic', stateroot='atomic-host')
        get_root_fs_mock.return_value = '/dev/mapper/atomic-root'
        listdir_mock.side_effect = [
            ['1234567.0', '1234567.0.origin'],
            ['1234567.0.origin', 'abcdef.1.origin', 'abcdef.1', '1234567.0'],
        ]

        Deploy(cfg).run()

        run_mock.assert_called_once_with([
                'ostree',
                'admin',
                'deploy',
                '--os=atomic-host',
                'fedora-atomic:fedora/28/x86_64/atomic-host',
                '--karg=root=/dev/mapper/atomic-root'
            ], check=True)
        self.assertEqual(cfg.deployment_dir, os.path.join('/ostree', 'deploy', 'atomic-host', 'deploy', 'abcdef.1'))

    @mock.patch('deploy_ostree.steps.deploy.run')
    @mock.patch('deploy_ostree.steps.deploy.get_root_fs')
    @mock.patch('os.listdir')
    def test_should_add_additional_kernel_args(self, listdir_mock, get_root_fs_mock, run_mock):
        cfg = Config(
            Source.url('url'),
            'ref',
            remote='remote',
            stateroot='os',
            kernel_args=['quiet', 'splash']
        )
        get_root_fs_mock.return_value = '/dev/rootfs'
        listdir_mock.side_effect = [
            [],
            ['1234567.0', '1234567.0.origin'],
        ]

        Deploy(cfg).run()

        run_mock.assert_called_once_with([
                'ostree',
                'admin',
                'deploy',
                '--os=os',
                'remote:ref',
                '--karg=root=/dev/rootfs',
                '--karg-append=quiet',
                '--karg-append=splash',
            ], check=True)

    @mock.patch('deploy_ostree.steps.deploy.run', mock.Mock())
    @mock.patch('deploy_ostree.steps.deploy.get_root_fs', mock.Mock())
    @mock.patch('os.listdir')
    def test_should_raise_exception_if_nothing_was_added_to_deployments_dir(self, listdir_mock):
        cfg = Config(Source.url('url'), 'ref')
        listdir_mock.return_value = ['abcdef.1.origin', 'abcdef.1']

        step = Deploy(cfg)
        with self.assertRaises(DeployError):
            step.run()

    @mock.patch('deploy_ostree.steps.deploy.run', mock.Mock())
    @mock.patch('deploy_ostree.steps.deploy.get_root_fs', mock.Mock())
    @mock.patch('os.listdir')
    def test_should_raise_exception_if_too_many_elements_were_added_to_deployments_dir(self, listdir_mock):
        cfg = Config(Source.url('url'), 'ref')
        listdir_mock.side_effect = [
            [],
            ['1234567.0.origin', 'abcdef.1.origin', 'abcdef.1', '1234567.0'],
        ]

        step = Deploy(cfg)
        with self.assertRaises(DeployError):
            step.run()

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
