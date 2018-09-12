# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os
import posixpath
from unittest import mock, TestCase
from deploy_ostree.config import Config, Source
from deploy_ostree.steps.remote import get_steps, FileRemote, HttpRemote


class TestGetRemoteStep(TestCase):
    def test_should_return_HttpRemote_if_url_source(self):
        cfg = Config(Source.url('http://example.com/ostree'), 'ref')

        steps = get_steps(cfg)

        self.assertEqual(len(steps), 1)
        self.assertIsInstance(steps[0], HttpRemote)

    def test_should_return_FileRemote_if_path_source(self):
        cfg = Config(Source.path('/ostree/repo'), 'ref')

        steps = get_steps(cfg)

        self.assertEqual(len(steps), 1)
        self.assertIsInstance(steps[0], FileRemote)


class TestFileRemote(TestCase):
    @mock.patch('deploy_ostree.steps.remote.run')
    @mock.patch('os.path', posixpath)
    def test_should_add_ostree_remote_for_path_in_config(self, mock_run: mock.Mock):
        cfg = Config(Source.path('/srv/ostree/debian/repo'), 'debian/9/i386/desktop', remote='remote-name')

        FileRemote(cfg).run()

        mock_run.assert_called_once_with([
            'ostree', 'remote', 'add',
            '--repo=%s' % os.path.join('/ostree', 'repo'),
            '--no-gpg-verify',
            'remote-name',
            'file:///srv/ostree/debian/repo'
        ], check=True)

    @mock.patch('deploy_ostree.steps.remote.run')
    @mock.patch('os.path', posixpath)
    def test_should_add_ostree_remote_with_absolute_path(self, mock_run: mock.Mock):
        cfg = Config(Source.path('repo'), 'debian/9/i386/desktop', remote='remote-name', base_dir='ostree')
        repo_abs_path = os.path.join(os.getcwd(), 'ostree', 'repo')

        FileRemote(cfg).run()

        mock_run.assert_called_once_with([
            'ostree', 'remote', 'add',
            '--repo=%s' % os.path.join('/ostree', 'repo'),
            '--no-gpg-verify',
            'remote-name',
            'file://%s' % repo_abs_path
        ], check=True)

    def test_title_should_be_str(self):
        self.assertIsInstance(FileRemote(mock.Mock()).title, str)


class TestHttpRemote(TestCase):
    @mock.patch('deploy_ostree.steps.remote.run')
    def test_should_add_ostree_remote_for_url_in_config(self, mock_run: mock.Mock):
        cfg = Config(Source.url('https://example.com/ostree'), 'debian/9/i386/desktop', remote='remote-name')

        HttpRemote(cfg).run()

        mock_run.assert_called_once_with([
            'ostree', 'remote', 'add',
            '--repo=%s' % os.path.join('/ostree', 'repo'),
            '--no-gpg-verify',
            'remote-name',
            'https://example.com/ostree'
        ], check=True)

    def test_title_should_be_str(self):
        self.assertIsInstance(HttpRemote(mock.Mock()).title, str)
