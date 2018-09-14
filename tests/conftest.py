# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import pytest
from pathlib import Path
import tempfile
from typing import Iterator


def get_tempdir() -> Iterator[Path]:
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def tempdir():
    yield from get_tempdir()


@pytest.fixture(scope='class')
def tempdir_cls():
    yield from get_tempdir()
