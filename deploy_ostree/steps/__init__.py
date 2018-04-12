# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from typing import Iterable, List, Type  # noqa
from .deploystep import DeployStep
from .http_remote import HttpRemote
from .create_stateroot import CreateStateroot
from ..config import Config


class DeploySteps:
    def __init__(self, cfg: Config, deploy_step_types: Iterable[Type[DeployStep]]) -> None:
        self.steps = []  # type: List[DeployStep]
        for cls in deploy_step_types:
            if cls.is_relevant(cfg):
                self.steps.extend(cls.get_steps(cfg))

    def run(self):
        for step in self.steps:
            print('==>', step.title)
            step.run()


def get_deploy_steps(cfg: Config) -> DeploySteps:
    return DeploySteps(cfg, [HttpRemote, CreateStateroot])
