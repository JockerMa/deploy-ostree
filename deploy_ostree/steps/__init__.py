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

    def run(self):
        raise NotImplementedError


class DeploySteps:
    def __init__(self, cfg: Config, deploy_step_types: Iterable[Type[DeployStep]]) -> None:
        self.steps = []  # type: List[DeployStep]
        for cls in deploy_step_types:
            if cls.is_relevant(cfg):
                self.steps.extend(cls.get_steps(cfg))

    def run(self):
        for step in self.steps:
            step.run()


def get_deploy_steps(cfg: Config) -> DeploySteps:
    return DeploySteps(cfg, [])
