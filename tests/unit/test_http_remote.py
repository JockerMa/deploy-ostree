# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from unittest import mock, TestCase
from deploy_ostree.config import Config, Source
from deploy_ostree.steps.http_remote import HttpRemote


class TestHttpRemote(TestCase):
    def test_should_return_step_if_url_source(self):
        cfg = Config(Source.url('/'), 'ref')

        steps = HttpRemote.get_steps(cfg)

        self.assertEqual(len(steps), 1)

    def test_should_return_no_steps_ifpath_source(self):
        cfg = Config(Source.path('/'), 'ref')

        steps = HttpRemote.get_steps(cfg)

        self.assertEqual(len(steps), 0)

    @mock.patch('deploy_ostree.steps.http_remote.run')
    def test_should_add_ostree_remote_for_url_in_config(self, mock_run: mock.Mock):
        cfg = Config(Source.url('https://example.com/ostree'), 'debian/9/i386/desktop', remote='remote-name')

        steps = HttpRemote.get_steps(cfg)
        for step in steps:
            step.run()

        mock_run.assert_called_once_with([
            'ostree', 'remote', 'add',
            '--no-gpg-verify',
            'remote-name',
            'https://example.com/ostree'
        ], check=True)

    def test_title_should_be_str(self):
        self.assertIsInstance(HttpRemote(mock.Mock()).title, str)
