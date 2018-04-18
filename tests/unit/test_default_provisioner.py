# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os.path
from unittest import mock, TestCase, skip  # noqa
import deploy_ostree
from deploy_ostree.steps.default_provisioner import DefaultProvisioner
from deploy_ostree.config import Config, ProvisionerConfig


class TestDefaultProvisioner(TestCase):
    def test_should_be_relevant_if_default_provisioners_are_not_empty(self):
        cfg = Config('url', 'ref', default_provisioners=[ProvisionerConfig('name', {})])

        self.assertTrue(DefaultProvisioner.is_relevant(cfg))

    def test_should_not_be_relevant_if_no_default_provisioners(self):
        cfg = Config('url', 'ref', default_provisioners=[])

        self.assertFalse(DefaultProvisioner.is_relevant(cfg))

    def test_title_should_be_str_instance(self):
        self.assertIsInstance(DefaultProvisioner(mock.Mock(), mock.Mock()).title, str)

    @mock.patch('deploy_ostree.steps.default_provisioner.run')
    def test_should_run_provisioner_script_per_config(self, run_mock: mock.Mock):
        cfg = Config('url', 'ref', stateroot='test', default_provisioners=[
            ProvisionerConfig('name', {}),
            ProvisionerConfig('name2', {'arg': 'value'}),
        ])
        cfg.set_deployment_name('test-deploy.0')

        steps = DefaultProvisioner.get_steps(cfg)
        for step in steps:
            step.run()

        provisioners_dir = os.path.join(os.path.dirname(deploy_ostree.__file__), 'default-provisioners')
        deploy_dir = os.path.join('/', 'ostree', 'deploy', 'test', 'deploy', 'test-deploy.0')

        expected_calls = [
            mock.call(
                [os.path.join(provisioners_dir, 'name'), deploy_dir],
                check=True,
                env={}
            ),
            mock.call(
                [os.path.join(provisioners_dir, 'name2'), deploy_dir],
                check=True,
                env={'DEPLOY_OSTREE_arg': 'value'}
            )
        ]
        self.assertEqual(run_mock.mock_calls, expected_calls)
