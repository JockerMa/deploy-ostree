# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os.path
from unittest import mock, TestCase, skip  # noqa
import deploy_ostree
from deploy_ostree.steps.default_provisioner import DefaultProvisioner
from deploy_ostree.config import Config, ProvisionerConfig, Source


PROVISIONERS_DIR = os.path.join(os.path.dirname(deploy_ostree.__file__), 'default-provisioners')


class TestDefaultProvisioner(TestCase):
    cfg = Config(Source.url('url'), 'ref', stateroot='test')
    cfg.set_deployment_name('test-deploy.0')
    deploy_dir = os.path.join('/', 'ostree', 'deploy', 'test', 'deploy', 'test-deploy.0')

    def test_title_should_be_str_instance(self):
        self.assertIsInstance(DefaultProvisioner(mock.Mock(), mock.Mock()).title, str)

    @mock.patch('deploy_ostree.steps.default_provisioner.run')
    def test_should_run_provisioner_script_with_no_arguments(self, run_mock: mock.Mock):
        provisioner = ProvisionerConfig('etc-fstab', {})

        DefaultProvisioner(self.cfg, provisioner).run()

        run_mock.assert_called_once_with(
            [os.path.join(PROVISIONERS_DIR, 'etc-fstab'), self.deploy_dir],
            check=True,
            env={}
        )

    @mock.patch('deploy_ostree.steps.default_provisioner.run')
    def test_should_run_provisioner_script_with_arguments(self, run_mock: mock.Mock):
        provisioner = ProvisionerConfig('create-user', {'username': 'user', 'password': 'pwd'})

        DefaultProvisioner(self.cfg, provisioner).run()

        run_mock.assert_called_once_with(
            [os.path.join(PROVISIONERS_DIR, 'create-user'), self.deploy_dir],
            check=True,
            env={'DEPLOY_OSTREE_username': 'user', 'DEPLOY_OSTREE_password': 'pwd'}
        )
