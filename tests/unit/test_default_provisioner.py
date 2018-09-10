# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os.path
from unittest import mock, TestCase, skip  # noqa
import deploy_ostree
from deploy_ostree.steps.default_provisioner import DefaultProvisioner
from deploy_ostree.config import Config, ProvisionerConfig, Source


class TestDefaultProvisioner(TestCase):
    def test_should_return_no_steps_if_no_default_provisioners(self):
        cfg = Config(Source.url('url'), 'ref', default_provisioners=[])

        steps = DefaultProvisioner.get_steps(cfg)

        self.assertEqual(len(steps), 0)

    def test_title_should_be_str_instance(self):
        self.assertIsInstance(DefaultProvisioner(mock.Mock(), mock.Mock()).title, str)

    @mock.patch('deploy_ostree.steps.default_provisioner.run')
    def test_should_run_provisioner_script_per_config(self, run_mock: mock.Mock):
        cfg = Config(Source.url('url'), 'ref', stateroot='test', default_provisioners=[
            ProvisionerConfig('create-user', {}),
            ProvisionerConfig('etc-fstab', {'arg': 'value'}),
        ])
        cfg.set_deployment_name('test-deploy.0')

        steps = DefaultProvisioner.get_steps(cfg)
        for step in steps:
            step.run()

        provisioners_dir = os.path.join(os.path.dirname(deploy_ostree.__file__), 'default-provisioners')
        deploy_dir = os.path.join('/', 'ostree', 'deploy', 'test', 'deploy', 'test-deploy.0')

        expected_calls = [
            mock.call(
                [os.path.join(provisioners_dir, 'create-user'), deploy_dir],
                check=True,
                env={}
            ),
            mock.call(
                [os.path.join(provisioners_dir, 'etc-fstab'), deploy_dir],
                check=True,
                env={'DEPLOY_OSTREE_arg': 'value'}
            )
        ]
        self.assertEqual(run_mock.mock_calls, expected_calls)
