# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os.path
import shutil
from unittest import TestCase, skip
from .. import deploy_ostree, ostree

TESTS_DIR = os.path.dirname(__file__)


@skip('not implemented yet')
class TestSimpleDeploy(TestCase):
    @classmethod
    def setUpClass(cls):
        os.makedirs('/ostree/repo', mode=0o755)
        ostree(['init', '--repo=/ostree/repo'])
        deploy_ostree([os.path.join(TESTS_DIR, 'simple-deploy.json')])

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree('/ostree')

    def test_should_add_randomly_named_remote(self):
        remote = ostree(['remote', 'list']).stdout.strip()
        url = ostree(['remote', 'show-url', remote]).stdout.strip()
        self.assertEqual(
            'https://kojipkgs.fedoraproject.org/atomic/repo/',
            url)
