# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os.path
from ... import deploy_ostree
from ...fixtures import FixtureTestCase, OSTreeFixture, OSTreeCommitFixture

TESTS_DIR = os.path.join(os.path.dirname(__file__), os.pardir)


class TestRootKarg(FixtureTestCase):
    BOOTENTRIES_DIR = os.path.join('/boot', 'loader', 'entries')
    ROOT_KARG = '/dev/mapper/my-root-filesystem'
    FIXTURES = [OSTreeFixture(), OSTreeCommitFixture()]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        deploy_ostree([
            '--root-karg=%s' % cls.ROOT_KARG,
            os.path.join(TESTS_DIR, 'named-deploy.json')
        ])

    def test_should_create_bootloader_entry_with_correct_root_karg(self):
        entries = os.listdir(self.BOOTENTRIES_DIR)
        self.assertEqual(1, len(entries))
        entry_file = os.path.join(self.BOOTENTRIES_DIR, entries[0])
        self.assert_file_contains(entry_file, 'root=/dev/mapper/my-root-filesystem')

    def assert_file_contains(self, path, expected_content):
        with open(path, 'r') as f:
            content = f.read()
        self.assertIn(expected_content, content)
