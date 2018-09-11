# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from unittest import TestCase
from deploy_ostree.config import Config, Source, ProvisionerConfig
from deploy_ostree.steps.provisioners import get_steps
from deploy_ostree.steps.provisioners.builtin import BuiltinProvisioner


class TestGetProvisionerSteps(TestCase):
    def test_should_return_no_steps_if_no_default_provisioners(self):
        cfg = Config(Source.url('url'), 'ref', default_provisioners=[])

        steps = get_steps(cfg)

        self.assertEqual(len(steps), 0)

    def test_should_return_BuiltinProvisioner_per_configured_provisioner(self):
        cfg = Config(Source.url('url'), 'ref', stateroot='test', default_provisioners=[
            ProvisionerConfig('create-user', {}),
            ProvisionerConfig('etc-fstab', {'arg': 'value'}),
        ])

        steps = get_steps(cfg)

        self.assertEqual(len(steps), 2)
        self.assertIsInstance(steps[0], BuiltinProvisioner)
        self.assertIsInstance(steps[1], BuiltinProvisioner)
