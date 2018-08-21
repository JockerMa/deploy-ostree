# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from unittest import TestCase
from typing import List, Type  # noqa
from .fixture import Fixture  # noqa
from .ostree import OSTreeFixture
from .ostree_commit import OSTreeCommitFixture
from .http_server import HttpServerFixture

__all__ = [
    'FixtureTestCase',
    'OSTreeFixture',
    'OSTreeCommitFixture',
    'HttpServerFixture',
]


class FixtureTestCase(TestCase):
    FIXTURES = []  # type: List[Fixture]

    @classmethod
    def setUpClass(cls):
        for fixture in cls.FIXTURES:
            fixture.setUp()

    @classmethod
    def tearDownClass(cls):
        for fixture in reversed(cls.FIXTURES):
            fixture.tearDown()
