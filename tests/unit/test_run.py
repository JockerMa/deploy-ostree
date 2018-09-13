# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import subprocess
from unittest import mock, TestCase
import sys
from deploy_ostree.run import run, ProcessError


class TestRun(TestCase):
    @mock.patch('subprocess.run')
    def test_should_invoke_subprocess(self, mock_run: mock.Mock):
        args = ['ostree', 'remote', 'list']
        mock_run.return_value = subprocess.CompletedProcess([], 32)

        result = run(args)

        mock_run.assert_called_once_with(args, stdout=None, stderr=None, env=None)
        self.assertEqual(32, result.exitcode)
        self.assertIsNone(result.stdout)
        self.assertEqual(result.stdout, '')
        self.assertIsNone(result.stderr)
        self.assertEqual(result.stderr, '')

    @mock.patch('subprocess.run')
    def test_should_capture_and_decode_process_output_using_provided_encoding(self, mock_run: mock.Mock):
        args = [sys.executable, '-mdeploy_ostree']
        mock_run.return_value = subprocess.CompletedProcess(
            [],
            0,
            'stdout'.encode('utf-16'),
            'stderr'.encode('utf-16'))

        result = run(args, capture_output=True, encoding='utf-16')

        mock_run.assert_called_once_with(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=None)
        self.assertEqual(0, result.exitcode)
        self.assertEqual('stdout', result.stdout)
        self.assertEqual('stderr', result.stderr)

    @mock.patch('subprocess.run')
    def test_result_should_contain_process_args(self, mock_run: mock.Mock):
        args = ['mount', '-o', 'bind', '/', '/subdir']
        mock_run.return_value = subprocess.CompletedProcess([], 0)

        result = run(args)

        self.assertEqual(result.args, args)
        self.assertEqual(result.args_string, 'mount -o bind / /subdir')

    @mock.patch('subprocess.run')
    def test_should_not_raise_if_check_is_true_and_exitcode_is_zero(self, mock_run: mock.Mock):
        args = ['mount']
        mock_run.return_value = subprocess.CompletedProcess([], 0)

        result = run(args, check=True)

        self.assertEqual(0, result.exitcode)

    @mock.patch('subprocess.run')
    def test_should_raise_exception_if_check_is_true_and_exitcode_is_nonzero(self, mock_run: mock.Mock):
        args = ['mount', '-o', 'bind', '/', '/subdir']
        mock_run.return_value = subprocess.CompletedProcess([], -1)

        with self.assertRaises(ProcessError) as cm:
            run(args, check=True)
        self.assertEqual(str(cm.exception), "'mount -o bind / /subdir' failed with status -1")

    @mock.patch('subprocess.run')
    @mock.patch('os.environ', {'HOME': '/home/user', 'USER': 'user'})
    def test_should_extend_os_environ_with_given_environment(self, mock_run: mock.Mock):
        args = ['/usr/bin/python3', '-m', 'http.server']

        run(
            args,
            env={'extra1': 'value1', 'extra2': 'value2', 'USER': 'test'},
        )

        mock_run.assert_called_once_with(
            args,
            stdout=None,
            stderr=None,
            env={
                'HOME': '/home/user',
                'USER': 'test',
                'extra1': 'value1',
                'extra2': 'value2',
            })
