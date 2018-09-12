# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os.path
from deploy_ostree.steps.deploy import get_root_fs
from ... import deploy_ostree
from ...fixtures import FixtureTestCase, OSTreeFixture, OSTreeCommitFixture

TESTS_DIR = os.path.join(os.path.dirname(__file__), os.pardir)
BOOTENTRIES_DIR = os.path.join('/boot', 'loader', 'entries')


def get_bootloader_entry():
    entries = os.listdir(BOOTENTRIES_DIR)
    entry_file = os.path.join(BOOTENTRIES_DIR, entries[0])
    with open(entry_file, 'r') as f:
        return f.read()


class TestDefaultRootKarg(FixtureTestCase):
    FIXTURES = [OSTreeFixture(), OSTreeCommitFixture()]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        deploy_ostree([os.path.join(TESTS_DIR, 'named-deploy.json')])

    def test_should_create_bootloader_entry_with_default_root_karg(self):
        self.assertIn('root=%s' % get_root_fs(), get_bootloader_entry())


class TestRootKarg(FixtureTestCase):
    ROOT_KARG = '/dev/mapper/my-root-filesystem'
    FIXTURES = [OSTreeFixture(), OSTreeCommitFixture()]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        deploy_ostree([
            '--root-karg=%s' % cls.ROOT_KARG,
            os.path.join(TESTS_DIR, 'named-deploy.json')
        ])

    def test_should_create_bootloader_entry_with_specified_root_karg(self):
        self.assertIn('root=%s' % self.ROOT_KARG, get_bootloader_entry())
