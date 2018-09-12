# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os
from unittest import mock, TestCase
from deploy_ostree.config import Config, Source
from deploy_ostree.steps.deploystep import DeployError
from deploy_ostree.steps.deploy import Deploy


class TestDeploy(TestCase):
    @mock.patch('deploy_ostree.steps.deploy.run')
    @mock.patch('os.listdir')
    def test_should_deploy_commit_and_set_deployment_folder(self, listdir_mock, run_mock):
        cfg = Config(
            Source.url('url'),
            'fedora/28/x86_64/atomic-host',
            remote='fedora-atomic',
            stateroot='atomic-host',
            root_karg='/dev/mapper/atomic-root',
        )
        listdir_mock.side_effect = [
            ['1234567.0', '1234567.0.origin'],
            ['1234567.0.origin', 'abcdef.1.origin', 'abcdef.1', '1234567.0'],
        ]

        Deploy(cfg).run()

        run_mock.assert_called_once_with([
            'ostree', 'admin', 'deploy',
            '--sysroot=/',
            '--os=atomic-host',
            'fedora-atomic:fedora/28/x86_64/atomic-host',
            '--karg=root=/dev/mapper/atomic-root'
        ], check=True)
        self.assertEqual(cfg.deployment_dir, os.path.join('/ostree', 'deploy', 'atomic-host', 'deploy', 'abcdef.1'))

    @mock.patch('deploy_ostree.steps.deploy.run')
    @mock.patch('os.listdir')
    def test_should_add_additional_kernel_args(self, listdir_mock, run_mock):
        cfg = Config(
            Source.url('url'),
            'ref',
            remote='remote',
            stateroot='os',
            kernel_args=['quiet', 'splash'],
            root_karg='/dev/rootfs',
        )
        listdir_mock.side_effect = [
            [],
            ['1234567.0', '1234567.0.origin'],
        ]

        Deploy(cfg).run()

        run_mock.assert_called_once_with([
            'ostree', 'admin', 'deploy',
            '--sysroot=/',
            '--os=os',
            'remote:ref',
            '--karg=root=/dev/rootfs',
            '--karg-append=quiet',
            '--karg-append=splash',
        ], check=True)

    @mock.patch('deploy_ostree.steps.deploy.run')
    @mock.patch('os.listdir')
    def test_should_deploy_into_specified_sysroot(self, listdir_mock, run_mock):
        sysroot = os.path.join('/mnt', 'rootfs')
        cfg = Config(
            Source.url('url'),
            'ref',
            remote='remote',
            stateroot='test-stateroot',
            sysroot=sysroot,
            root_karg='/dev/mapper/atomic-root'
        )
        listdir_mock.side_effect = [[], ['deploy', 'deploy.origin']]

        Deploy(cfg).run()

        listdir_mock.assert_called_with(os.path.join(sysroot, 'ostree', 'deploy', 'test-stateroot', 'deploy'))
        run_mock.assert_called_once_with([
            'ostree', 'admin', 'deploy',
            '--sysroot=%s' % sysroot,
            '--os=test-stateroot',
            'remote:ref',
            '--karg=root=/dev/mapper/atomic-root'
        ], check=True)

    @mock.patch('deploy_ostree.steps.deploy.run', mock.Mock())
    @mock.patch('os.listdir')
    def test_should_raise_exception_if_nothing_was_added_to_deployments_dir(self, listdir_mock):
        cfg = Config(Source.url('url'), 'ref')
        listdir_mock.return_value = ['abcdef.1.origin', 'abcdef.1']

        step = Deploy(cfg)
        with self.assertRaises(DeployError):
            step.run()

    @mock.patch('deploy_ostree.steps.deploy.run', mock.Mock())
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
