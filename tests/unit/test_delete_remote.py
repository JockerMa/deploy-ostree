# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from unittest import mock, TestCase
from deploy_ostree.config import Config, Source
from deploy_ostree.steps.delete_remote import DeleteRemote


class TestDeleteRemote(TestCase):
    @mock.patch('deploy_ostree.steps.delete_remote.run')
    def test_should_delete_ostree_remote(self, mock_run: mock.Mock):
        cfg = Config(Source.url('url'), 'ref', remote='remote-name')

        steps = DeleteRemote.get_steps(cfg)
        for step in steps:
            step.run()

        mock_run.assert_called_once_with([
            'ostree', 'remote', 'delete',
            '--if-exists',
            'remote-name',
        ], check=True)

    def test_title_should_be_str(self):
        self.assertIsInstance(DeleteRemote(mock.Mock()).title, str)
