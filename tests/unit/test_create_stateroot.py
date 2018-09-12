# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os.path
from unittest import mock, TestCase
from deploy_ostree.config import Config, Source
from deploy_ostree.steps.create_stateroot import CreateStateroot


class TestCreateStateroot(TestCase):
    @mock.patch('deploy_ostree.steps.create_stateroot.run')
    @mock.patch('os.path.exists')
    def test_should_create_stateroot(self, exists_mock: mock.Mock, run_mock: mock.Mock):
        sysroot = os.path.join('/mnt', 'rootfs')
        cfg = Config(Source.url('url'), 'ref', stateroot='stateroot-name', sysroot=sysroot)
        exists_mock.return_value = False

        CreateStateroot(cfg).run()

        exists_mock.assert_called_once_with('/ostree/deploy/stateroot-name')
        run_mock.assert_called_once_with([
            'ostree', 'admin', 'os-init',
            '--sysroot=%s' % sysroot,
            'stateroot-name'
        ], check=True)

    @mock.patch('deploy_ostree.steps.create_stateroot.run')
    @mock.patch('os.path.exists')
    def test_should_not_create_stateroot_if_path_exists(self, exists_mock: mock.Mock, run_mock: mock.Mock):
        cfg = Config(Source.url('url'), 'ref', stateroot='stateroot-name')
        exists_mock.return_value = True

        CreateStateroot(cfg).run()

        exists_mock.assert_called_once_with('/ostree/deploy/stateroot-name')
        run_mock.assert_not_called()

    def test_title_should_be_str(self):
        self.assertIsInstance(CreateStateroot(mock.Mock()).title, str)
