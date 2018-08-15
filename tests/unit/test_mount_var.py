# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os
from unittest import mock, TestCase
from deploy_ostree.config import Config, Source
from deploy_ostree.steps.mount_var import MountVar


class TestMountVar(TestCase):
    def test_should_not_error_if_get_steps_is_called_without_deployment_name_set(self):
        cfg = Config(Source.url('url'), 'ref', stateroot='test')

        steps = MountVar.get_steps(cfg)

        self.assertIsNotNone(steps)

    @mock.patch('deploy_ostree.steps.mount_var.run')
    def test_should_bind_mount_var_into_deployment(self, run_mock: mock.Mock):
        cfg = Config(Source.url('url'), 'ref', stateroot='test')
        cfg.set_deployment_name('test-deploy.0')

        steps = MountVar.get_steps(cfg)
        for step in steps:
            step.run()

        run_mock.assert_called_once_with([
            'mount',
            '-o', 'bind',
            os.path.join('/ostree', 'deploy', 'test', 'var'),
            os.path.join('/ostree', 'deploy', 'test', 'deploy', 'test-deploy.0', 'var'),
        ], check=True)

    def test_should_be_relevant(self):
        self.assertTrue(MountVar.is_relevant(mock.Mock()))

    def test_title_should_be_str(self):
        self.assertIsInstance(MountVar(mock.Mock()).title, str)
