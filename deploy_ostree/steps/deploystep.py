# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from typing import Iterable, List, Type  # noqa
from ..config import Config


class DeployStep:
    @classmethod
    def is_relevant(cls, cfg: Config) -> bool:
        raise NotImplementedError

    @classmethod
    def get_steps(cls, cfg: Config) -> 'Iterable[DeployStep]':
        raise NotImplementedError

    @property
    def title(self) -> str:
        raise NotImplementedError

    def run(self):
        raise NotImplementedError
