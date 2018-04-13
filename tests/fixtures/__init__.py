# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from unittest import TestCase
from typing import List, Type  # noqa
from .fixture import Fixture  # noqa
from .ostree import OSTreeFixture

__all__ = ['FixtureTestCase', 'OSTreeFixture']


class FixtureTestCase(TestCase):
    FIXTURES = []  # type: List[Type[Fixture]]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fixtures = [fixture_cls() for fixture_cls in self.FIXTURES]

    @classmethod
    def setUpClass(cls):
        for fixture_cls in cls.FIXTURES:
            fixture_cls.setUpClass()

    @classmethod
    def tearDownClass(cls):
        for fixture_cls in reversed(cls.FIXTURES):
            fixture_cls.tearDownClass()

    def setUp(self):
        for fixture_instance in self.fixtures:
            fixture_instance.setUp()

    def tearDown(self):
        for fixture_instance in reversed(self.fixtures):
            fixture_instance.tearDown()
