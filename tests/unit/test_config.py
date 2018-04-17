# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from io import StringIO
import os.path
from unittest import TestCase
from deploy_ostree.config import Config, ProvisionerConfig, InvalidConfigError


class TestConfig(TestCase):
    def test_should_parse_config_with_url_and_ref(self):
        json = '''{
            "url": "https://example.com/ostree",
            "ref": "fedora/28/x86_64/workstation",

            "ignored key": "ignored value"
        }'''
        cfg = Config.parse_json(StringIO(json))

        self.assertEqual('https://example.com/ostree', cfg.url)
        self.assertEqual('fedora/28/x86_64/workstation', cfg.ref)

    def test_should_parse_config_with_remote_and_stateroot_names(self):
        json = '''{
            "url": "https://example.com/ostree",
            "ref": "fedora/28/x86_64/workstation",

            "remote": "atomicws",
            "stateroot": "fedora-atomic-workstation"
        }'''
        cfg = Config.parse_json(StringIO(json))

        self.assertEqual('https://example.com/ostree', cfg.url)
        self.assertEqual('fedora/28/x86_64/workstation', cfg.ref)
        self.assertEqual('atomicws', cfg.remote)
        self.assertEqual('fedora-atomic-workstation', cfg.stateroot)

    def test_should_parse_config_with_empty_provisioners_list(self):
        json = '''{
            "url": "http://example.com",
            "ref": "ref",

            "default-provisioners": []
        }'''
        cfg = Config.parse_json(StringIO(json))

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
        cfg = Config.parse_json(StringIO(json))

        self.assertEqual(cfg.default_provisioners, [
            ProvisionerConfig('some-provisioner', {})
        ])

    def test_should_parse_config_with_multiple_provisioners_and_arguments(self):
        json = '''{
            "url": "http://example.com",
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
        cfg = Config.parse_json(StringIO(json))

        self.assertEqual(cfg.default_provisioners, [
            ProvisionerConfig('prov-1', {}),
            ProvisionerConfig('prov-3', {'arg1': 'value1', 'arg2': 5}),
            ProvisionerConfig('prov-2', {'arg': True}),
        ])

    def test_should_raise_config_exception_if_url_is_missing(self):
        json = '{"ref": "ostree/ref"}'
        with self.assertRaises(InvalidConfigError, msg="missing key 'ostree_url'"):
            Config.parse_json(StringIO(json))

    def test_should_raise_config_exception_if_ref_is_missing(self):
        json = '{"url": "http://example.com"}'
        with self.assertRaises(InvalidConfigError, msg="missing key 'ref'"):
            Config.parse_json(StringIO(json))

    def test_remote_name_should_be_randomly_generated_if_not_specified(self):
        cfg1 = Config('url', 'ref')
        cfg2 = Config('url', 'ref')

        self.assertNotEqual(cfg1.remote, cfg2.remote)

    def test_stateroot_should_be_randomly_generated_if_not_specified(self):
        cfg1 = Config('url', 'ref')
        cfg2 = Config('url', 'ref')

        self.assertNotEqual(cfg1.stateroot, cfg2.stateroot)

    def test_deployment_path_should_raise_exception_if_name_is_not_set(self):
        cfg = Config('url', 'ref')

        with self.assertRaises(RuntimeError):
            cfg.deployment_dir

    def test_deployment_path_should_return_path_after_setting_name(self):
        cfg = Config('url', 'ref', stateroot='test-stateroot')
        cfg.set_deployment_name('deployment-name')

        self.assertEqual(
            cfg.deployment_dir,
            os.path.join('/ostree', 'deploy', 'test-stateroot', 'deploy', 'deployment-name')
        )
