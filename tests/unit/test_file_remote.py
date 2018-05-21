# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os
import posixpath
from unittest import mock, TestCase
from deploy_ostree.config import Config, Source
from deploy_ostree.steps.file_remote import FileRemote


class TestFileRemote(TestCase):
    @mock.patch('deploy_ostree.steps.file_remote.run')
    @mock.patch('os.path', posixpath)
    def test_should_add_ostree_remote_for_path_in_config(self, mock_run: mock.Mock):
        cfg = Config(Source.path('/srv/ostree/debian/repo'), 'debian/9/i386/desktop', remote='remote-name')

        steps = FileRemote.get_steps(cfg)
        for step in steps:
            step.run()

        mock_run.assert_called_once_with([
            'ostree',
            'remote', 'add',
            '--no-gpg-verify',
            '--if-not-exists',
            '--repo=/ostree/repo',
            'remote-name',
            'file:///srv/ostree/debian/repo'
        ], check=True)

    @mock.patch('deploy_ostree.steps.file_remote.run')
    @mock.patch('os.path', posixpath)
    def test_should_add_ostree_remote_with_absolute_path(self, mock_run: mock.Mock):
        cfg = Config(Source.path('repo'), 'debian/9/i386/desktop', remote='remote-name', base_dir='ostree')
        repo_abs_path = os.path.join(os.getcwd(), 'ostree', 'repo')

        steps = FileRemote.get_steps(cfg)
        for step in steps:
            step.run()

        mock_run.assert_called_once_with([
            'ostree',
            'remote', 'add',
            '--no-gpg-verify',
            '--if-not-exists',
            '--repo=/ostree/repo',
            'remote-name',
            'file://%s' % repo_abs_path
        ], check=True)

    def test_should_not_be_relevant_if_source_is_url(self):
        cfg = Config(Source.url('url'), 'ref')

        self.assertFalse(FileRemote.is_relevant(cfg))

    def test_should_be_relevant_if_source_is_path(self):
        cfg = Config(Source.path('path'), 'ref')

        self.assertTrue(FileRemote.is_relevant(cfg))

    def test_title_should_be_str(self):
        self.assertIsInstance(FileRemote(mock.Mock()).title, str)
