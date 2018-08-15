# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from typing import Sequence  # noqa
from ..config import Config


class DeployError(RuntimeError):
    pass


class DeployStep:
    def __init__(self, cfg: Config) -> None:
        pass

    @classmethod
    def is_relevant(cls, cfg: Config) -> bool:
        return True

    @classmethod
    def get_steps(cls, cfg: Config) -> 'Sequence[DeployStep]':
        return [cls(cfg)]

    @property
    def title(self) -> str:
        raise NotImplementedError

    def run(self):
        raise NotImplementedError

    def cleanup(self):
        pass
