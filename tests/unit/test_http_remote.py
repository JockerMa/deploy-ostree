# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from unittest import mock, TestCase
from deploy_ostree.config import Config
from deploy_ostree.steps.http_remote import HttpRemote


class TestHttpRemote(TestCase):
    @mock.patch('deploy_ostree.steps.http_remote.run')
    @mock.patch('deploy_ostree.steps.http_remote.which')
    def test_should_add_ostree_remote_for_url_in_config(self, mock_which: mock.Mock, mock_run: mock.Mock):
        cfg = Config('https://deb.debian.org/ostree', 'debian/9/i386/desktop', 'remote-name')
        mock_which.return_value = '/usr/bin/ostree'

        steps = HttpRemote.get_steps(cfg)
        for step in steps:
            step.run()

        mock_run.assert_called_once_with([
            '/usr/bin/ostree',
            'remote', 'add',
            '--no-gpg-verify',
            '--if-not-exists',
            '--repo=/ostree/repo',
            'remote-name',
            'https://deb.debian.org/ostree'
        ], check=True)

    def test_should_be_relevant_if_url_is_not_none(self):
        cfg = Config('url', 'ref')

        self.assertTrue(HttpRemote.is_relevant(cfg))

    def test_should_not_be_relevant_if_url_is_none(self):
        cfg = Config(None, 'ref')

        self.assertFalse(HttpRemote.is_relevant(cfg))
