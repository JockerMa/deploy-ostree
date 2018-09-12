# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os.path
from unittest import mock, TestCase, skip  # noqa
import deploy_ostree
from deploy_ostree.steps.provisioners.builtin import BuiltinProvisioner
from deploy_ostree.config import Config, ProvisionerConfig, Source


PROVISIONERS_DIR = os.path.join(os.path.dirname(deploy_ostree.__file__), 'builtin-provisioners')


class TestBuiltinProvisioner(TestCase):
    cfg = Config(Source.url('url'), 'ref', stateroot='test')
    cfg.set_deployment_name('test-deploy.0')
    deploy_dir = os.path.join('/', 'ostree', 'deploy', 'test', 'deploy', 'test-deploy.0')

    def test_title_should_be_str_instance(self):
        self.assertIsInstance(BuiltinProvisioner(mock.Mock(), mock.Mock()).title, str)

    @mock.patch('deploy_ostree.steps.provisioners.builtin.run')
    def test_should_run_provisioner_script_with_no_arguments(self, run_mock: mock.Mock):
        provisioner = ProvisionerConfig('etc-fstab', {})

        BuiltinProvisioner(self.cfg, provisioner).run()

        run_mock.assert_called_once_with(
            [os.path.join(PROVISIONERS_DIR, 'etc-fstab'), self.deploy_dir],
            check=True,
            env={}
        )

    @mock.patch('deploy_ostree.steps.provisioners.builtin.run')
    def test_should_run_provisioner_script_with_specified_sysroot(self, run_mock: mock.Mock):
        sysroot = os.path.join('/mnt', 'rootfs')
        cfg = Config(Source.url('url'), 'ref', stateroot='test', sysroot=sysroot)
        cfg.set_deployment_name('test-deploy.0')
        provisioner = ProvisionerConfig('etc-fstab', {})

        BuiltinProvisioner(cfg, provisioner).run()

        run_mock.assert_called_once_with([
            os.path.join(PROVISIONERS_DIR, 'etc-fstab'),
            os.path.join(sysroot, 'ostree', 'deploy', 'test', 'deploy', 'test-deploy.0')
        ], check=True, env={})

    @mock.patch('deploy_ostree.steps.provisioners.builtin.run')
    def test_should_run_provisioner_script_with_arguments(self, run_mock: mock.Mock):
        provisioner = ProvisionerConfig('create-user', {'username': 'user', 'password': 'pwd'})

        BuiltinProvisioner(self.cfg, provisioner).run()

        run_mock.assert_called_once_with(
            [os.path.join(PROVISIONERS_DIR, 'create-user'), self.deploy_dir],
            check=True,
            env={'DEPLOY_OSTREE_username': 'user', 'DEPLOY_OSTREE_password': 'pwd'}
        )
