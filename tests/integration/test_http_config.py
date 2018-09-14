# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os
import time
from .. import deploy_ostree
from ..fixtures import FixtureTestCase, OSTreeFixture, OSTreeCommitFixture, HttpServerFixture

TESTS_DIR = os.path.dirname(__file__)


class TestHttpConfig(FixtureTestCase):
    FIXTURES = [
        OSTreeFixture(),
        OSTreeCommitFixture(),
        HttpServerFixture(TESTS_DIR, 10000)
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # wait a bit to give the HTTP server a chance to start up
        time.sleep(5)
        deploy_ostree(['http://127.0.0.1:10000/named-deploy.json'])

    def test_should_create_named_stateroot(self):
        self.assertTrue(os.path.isdir('/ostree/deploy/test-stateroot/var'))

    def test_should_deploy_commit(self):
        deploydir_contents = os.listdir('/ostree/deploy/test-stateroot/deploy')
        self.assertEqual(len(deploydir_contents), 2)
