# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import pytest
import os
from pathlib import Path
from typing import Sequence
from .. import deploy_ostree as deploy_ostree_helper
from ..fixtures import OSTreeFixture, OSTreeCommitFixture


class OSTreeSetup:
    def __init__(self, sysroot: Path=Path('/')) -> None:
        self._fixture = OSTreeFixture(sysroot=str(sysroot))
        self.sysroot = sysroot
        self._fixture.setUp()

    def _cleanup(self):
        self._fixture.tearDown()

    def deployments(self, stateroot: str) -> Sequence[Path]:
        deploy_path = self / 'deploy' / stateroot / 'deploy'  # type: Path
        return [
            elem for elem
            in deploy_path.iterdir()
            if not elem.name.endswith('.origin')
        ]

    def deployment(self, stateroot: str) -> Path:
        deployments = self.deployments(stateroot)
        assert len(deployments) == 1
        return deployments[0]

    def __truediv__(self, other) -> Path:
        return self.sysroot / 'ostree' / other


@pytest.fixture(scope='class')
def ostree_setup(request):
    sysroot = getattr(request.cls, 'sysroot', Path('/'))
    fixture = OSTreeSetup(sysroot=sysroot)
    yield fixture
    fixture._cleanup()


@pytest.fixture(scope='class')
def ostree_commit(request):
    fixture = OSTreeCommitFixture()
    fixture.setUp()
    yield fixture
    fixture.tearDown()


@pytest.fixture(scope='class')
def testdata_dir():
    oldpwd = os.getcwd()
    os.chdir(os.path.dirname(__file__))
    yield
    os.chdir(oldpwd)


@pytest.fixture(scope='class')
def deploy_ostree(request, testdata_dir):
    args = getattr(request.cls, 'deploy_ostree', [])
    deploy_ostree_helper(args)
