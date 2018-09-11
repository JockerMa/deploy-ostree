# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os
from unittest import mock, TestCase
from deploy_ostree.config import Config, Source
from deploy_ostree.steps.mount_var import MountVar


class TestMountVar(TestCase):
    def test_should_not_error_if_instance_is_created_without_deployment_name_set(self):
        cfg = Config(Source.url('url'), 'ref', stateroot='test')

        step = MountVar(cfg)

        self.assertIsNotNone(step)

    @mock.patch('deploy_ostree.steps.mount_var.run')
    def test_should_bind_mount_var_into_deployment(self, run_mock: mock.Mock):
        cfg = Config(Source.url('url'), 'ref', stateroot='test')
        cfg.set_deployment_name('test-deploy.0')

        MountVar(cfg).run()

        run_mock.assert_called_once_with([
            'mount',
            '-o', 'bind',
            os.path.join('/ostree', 'deploy', 'test', 'var'),
            os.path.join('/ostree', 'deploy', 'test', 'deploy', 'test-deploy.0', 'var'),
        ], check=True)

    @mock.patch('deploy_ostree.steps.mount_var.run')
    def test_should_unmount_on_cleanup(self, run_mock: mock.Mock):
        cfg = Config(Source.url('url'), 'ref', stateroot='test')
        cfg.set_deployment_name('test-deploy.0')

        MountVar(cfg).cleanup()

        run_mock.assert_called_once_with([
            'umount',
            '--lazy',
            os.path.join('/ostree', 'deploy', 'test', 'deploy', 'test-deploy.0', 'var'),
        ], check=True)

    def test_title_should_be_str(self):
        self.assertIsInstance(MountVar(mock.Mock()).title, str)
