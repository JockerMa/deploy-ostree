# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from io import StringIO
import os.path
from pathlib import Path
from unittest import TestCase, mock
from deploy_ostree.config import Config, ProvisionerConfig, InvalidConfigError, Source


@mock.patch('deploy_ostree.config.get_root_fs', mock.Mock(return_value='/dev/sda1'))
class TestConfig(TestCase):
    def test_should_parse_config_with_url_and_ref(self):
        json = '''{
            "url": "https://example.com/ostree",
            "ref": "fedora/28/x86_64/workstation",

            "ignored key": "ignored value"
        }'''
        cfg = Config.parse_yaml(StringIO(json))

        self.assertEqual('https://example.com/ostree', cfg.url)
        self.assertIsNone(cfg.path)
        self.assertEqual('fedora/28/x86_64/workstation', cfg.ref)

    def test_should_parse_config_with_path_and_ref(self):
        json = '''{
            "path": "/srv/ostree",
            "ref": "fedora/28/x86_64/workstation"
        }'''
        cfg = Config.parse_yaml(StringIO(json))

        self.assertEqual('/srv/ostree', cfg.path)
        self.assertIsNone(cfg.url)
        self.assertEqual('fedora/28/x86_64/workstation', cfg.ref)

    def test_should_raise_config_exception_if_both_url_and_path_are_present(self):
        json = '''{
            "url": "https://example.com/ostree",
            "path": "/srv/ostree",
            "ref": "fedora/28/x86_64/workstation"
        }'''
        with self.assertRaises(InvalidConfigError):
            Config.parse_yaml(StringIO(json))

    def test_should_parse_config_with_remote_and_stateroot_names(self):
        json = '''{
            "url": "https://example.com/ostree",
            "ref": "fedora/28/x86_64/workstation",

            "remote": "atomicws",
            "stateroot": "fedora-atomic-workstation"
        }'''
        cfg = Config.parse_yaml(StringIO(json))

        self.assertEqual('https://example.com/ostree', cfg.url)
        self.assertEqual('fedora/28/x86_64/workstation', cfg.ref)
        self.assertEqual('atomicws', cfg.remote)
        self.assertEqual('fedora-atomic-workstation', cfg.stateroot)

    def test_should_parse_config_with_empty_provisioners_list(self):
        json = '''{
            "path": "/srv/ostree",
            "ref": "ref",

            "default-provisioners": []
        }'''
        cfg = Config.parse_yaml(StringIO(json))

        self.assertEqual(cfg.default_provisioners, [])

    def test_should_parse_config_with_one_default_provisioner(self):
        json = '''{
            "url": "http://example.com",
            "ref": "ref",

            "default-provisioners": [
                {
                    "provisioner": "some-provisioner"
                }
            ]
        }'''
        cfg = Config.parse_yaml(StringIO(json))

        self.assertEqual(cfg.default_provisioners, [
            ProvisionerConfig('some-provisioner', {})
        ])

    def test_should_parse_config_with_multiple_provisioners_and_arguments(self):
        json = '''{
            "path": "/srv/ostree",
            "ref": "ref",

            "default-provisioners": [
                {
                    "provisioner": "prov-1"
                },
                {
                    "arg1": "value1",
                    "arg2": 5,
                    "provisioner": "prov-3"
                },
                {
                    "provisioner": "prov-2",
                    "arg": true
                }
            ]
        }'''
        cfg = Config.parse_yaml(StringIO(json))

        self.assertEqual(cfg.default_provisioners, [
            ProvisionerConfig('prov-1', {}),
            ProvisionerConfig('prov-3', {'arg1': 'value1', 'arg2': 5}),
            ProvisionerConfig('prov-2', {'arg': True}),
        ])

    def test_kernel_args_should_be_empty_if_not_specified(self):
        json = '''{
            "path": "/srv/ostree",
            "ref": "ref"
        }'''
        cfg = Config.parse_yaml(StringIO(json))

        self.assertEqual(cfg.kernel_args, [])

    def test_should_parse_config_with_kernel_args(self):
        json = '''{
            "path": "/srv/ostree",
            "ref": "ref",
            "kernel-args": [
                "arg1",
                "arg2",
                "arg3"
            ]
        }'''
        cfg = Config.parse_yaml(StringIO(json))

        self.assertEqual(cfg.kernel_args, ['arg1', 'arg2', 'arg3'])

    def test_should_parse_config_with_empty_kernel_args(self):
        json = '''{
            "path": "/srv/ostree",
            "ref": "ref",
            "kernel-args": []
        }'''
        cfg = Config.parse_yaml(StringIO(json))

        self.assertEqual(cfg.kernel_args, [])

    def test_should_take_base_dir_from_argument(self):
        json = '{"path": "repo", "ref": "ref"}'
        cfg = Config.parse_yaml(StringIO(json), base_dir='/home/user/ostree')

        self.assertEqual(cfg.base_dir, '/home/user/ostree')

    def test_default_base_dir_should_be_empty(self):
        json = '{"path": "repo", "ref": "ref"}'
        cfg = Config.parse_yaml(StringIO(json))

        self.assertEqual(cfg.base_dir, '')

    def test_path_should_include_base_dir(self):
        json = '{"path": "repo", "ref": "ref"}'
        cfg = Config.parse_yaml(StringIO(json), base_dir='ostree')

        self.assertEqual(cfg.path, os.path.join('ostree', 'repo'))

    def test_path_should_not_specifically_include_base_dir_if_default(self):
        json = '{"path": "repo/path", "ref": "ref"}'
        cfg = Config.parse_yaml(StringIO(json))

        self.assertEqual(cfg.path, 'repo/path')

    def test_path_should_not_include_base_dir_if_absolute(self):
        json = '{"path": "/srv/ostree", "ref": "ref"}'
        cfg = Config.parse_yaml(StringIO(json), base_dir='/home/user/')

        self.assertEqual(cfg.path, '/srv/ostree')

    def test_should_raise_config_exception_if_neither_url_nor_path_is_present(self):
        json = '{"ref": "ostree/ref"}'
        with self.assertRaises(InvalidConfigError):
            Config.parse_yaml(StringIO(json))

    def test_should_raise_config_exception_if_url_is_present_and_ref_is_missing(self):
        json = '{"url": "http://example.com"}'
        with self.assertRaises(InvalidConfigError):
            Config.parse_yaml(StringIO(json))

    def test_should_raise_config_exception_if_path_is_present_and_ref_is_missing(self):
        json = '{"path": "/os/tree"}'
        with self.assertRaises(InvalidConfigError):
            Config.parse_yaml(StringIO(json))

    def test_remote_name_should_be_randomly_generated_if_not_specified(self):
        cfg1 = Config(Source.url('url'), 'ref')
        cfg2 = Config(Source.url('url'), 'ref')

        self.assertNotEqual(cfg1.remote, cfg2.remote)

    def test_stateroot_should_be_randomly_generated_if_not_specified(self):
        cfg1 = Config(Source.url('url'), 'ref')
        cfg2 = Config(Source.url('url'), 'ref')

        self.assertNotEqual(cfg1.stateroot, cfg2.stateroot)

    def test_deployment_path_should_raise_exception_if_name_is_not_set(self):
        cfg = Config(Source.url('url'), 'ref')

        with self.assertRaises(RuntimeError):
            cfg.deployment_dir

    def test_deployment_path_should_return_path_after_setting_name(self):
        cfg = Config(Source.url('url'), 'ref', stateroot='test-stateroot')
        cfg.set_deployment_name('deployment-name')

        self.assertEqual(
            cfg.deployment_dir,
            os.path.join('/ostree', 'deploy', 'test-stateroot', 'deploy', 'deployment-name')
        )

    def test_var_dir_should_be_path_to_stateroot_var(self):
        cfg = Config(Source.url('url'), 'ref', stateroot='test-stateroot')

        self.assertEqual(
            cfg.var_dir,
            os.path.join('/ostree', 'deploy', 'test-stateroot', 'var')
        )

    def test_var_dir_should_be_path_to_stateroot_var_for_randomly_generated_stateroot(self):
        cfg = Config(Source.url('url'), 'ref')

        self.assertEqual(
            cfg.var_dir,
            os.path.join('/ostree', 'deploy', cfg.stateroot, 'var')
        )

    def test_default_sysroot_should_be_system_root(self):
        json = '{"url": "http://example.com", "ref": "ref"}'
        cfg = Config.parse_yaml(StringIO(json))

        self.assertEqual(cfg.sysroot, '/')

    def test_should_pass_sysroot_to_config(self):
        json = '{"url": "http://example.com", "ref": "ref"}'
        cfg = Config.parse_yaml(StringIO(json), sysroot='/mnt/rootfs')

        self.assertEqual(cfg.sysroot, '/mnt/rootfs')

    def test_var_dir_should_include_sysroot(self):
        sysroot = os.path.join('/mnt', 'rootfs')
        cfg = Config(Source.url('url'), 'ref', sysroot=sysroot)

        self.assertEqual(
            cfg.var_dir,
            os.path.join(sysroot, 'ostree', 'deploy', cfg.stateroot, 'var')
        )

    def test_deployment_dir_should_include_sysroot(self):
        sysroot = os.path.join('/mnt', 'rootfs')
        cfg = Config(Source.url('url'), 'ref', sysroot=sysroot)
        cfg.set_deployment_name('0123deployment.0')

        self.assertEqual(
            cfg.deployment_dir,
            os.path.join(sysroot, 'ostree', 'deploy', cfg.stateroot, 'deploy', '0123deployment.0')
        )

    def test_repo_dir_should_default_to_system_ostree_repo(self):
        cfg = Config(Source.url('url'), 'ref')

        self.assertEqual(cfg.ostree_repo, os.path.join('/ostree', 'repo'))

    def test_repo_dir_should_include_sysroot(self):
        sysroot = os.path.join('/mnt', 'rootfs')
        cfg = Config(Source.url('url'), 'ref', sysroot=sysroot)

        self.assertEqual(cfg.ostree_repo, os.path.join(sysroot, 'ostree', 'repo'))

    def test_default_root_filesystem_should_be_determined_by_get_root_fs(self):
        cfg = Config(Source.url('url'), 'ref')

        self.assertEqual(cfg.root_filesystem, '/dev/sda1')

    def test_should_pass_root_filesystem_to_config(self):
        json = '{"url": "http://example.com", "ref": "ref"}'
        cfg = Config.parse_yaml(StringIO(json), root_filesystem='/dev/mapper/custom-root')

        self.assertEqual(cfg.root_filesystem, '/dev/mapper/custom-root')


def test_fstab_should_default_to_system_fstab():
    cfg = Config(Source.url('url'), 'ref')

    assert cfg.fstab == Path('/', 'etc', 'fstab')
