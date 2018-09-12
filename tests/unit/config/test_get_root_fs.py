# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from io import StringIO
from unittest import TestCase, mock
from deploy_ostree.config.get_root_fs import get_root_fs


@mock.patch('sys.getfilesystemencoding', mock.Mock(return_value='fs-encoding'))
class TestGetRootFS(TestCase):
    @mock.patch('builtins.open')
    def test_should_read_root_arg_from_proc_cmdline(self, mock_open: mock.Mock):
        mock_open.return_value = StringIO('root=/dev/sda1')

        rootfs = get_root_fs()

        mock_open.assert_called_once_with('/proc/cmdline', 'r', encoding='fs-encoding')
        self.assertEqual('/dev/sda1', rootfs)

    @mock.patch('builtins.open')
    def test_should_parse_root_arg_from_multiple(self, mock_open: mock.Mock):
        mock_open.return_value = StringIO(
            'BOOT_IMAGE=/vmlinuz-4.9.0-4-amd64 '
            'root=/dev/mapper/debian--9--vg-root '
            'ro debian-installer=en_US.UTF-8 quiet')

        rootfs = get_root_fs()

        mock_open.assert_called_once_with('/proc/cmdline', 'r', encoding='fs-encoding')
        self.assertEqual('/dev/mapper/debian--9--vg-root', rootfs)

    @mock.patch('builtins.open')
    def test_should_return_empty_string_if_no_root_arg(self, mock_open: mock.Mock):
        mock_open.return_value = StringIO(
            'BOOT_IMAGE=/vmlinuz-4.9.0-4-amd64 '
            'ro debian-installer=en_US.UTF-8 quiet')

        rootfs = get_root_fs()

        mock_open.assert_called_once_with('/proc/cmdline', 'r', encoding='fs-encoding')
        self.assertEqual('', rootfs)
