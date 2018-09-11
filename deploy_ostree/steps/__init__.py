# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from typing import Callable, Iterable, Sequence, Type
from .deploystep import DeployStep, DeployError  # noqa
from .delete_remote import DeleteRemote
from .http_remote import HttpRemote
from .file_remote import FileRemote
from .pull_ref import PullRef
from .create_stateroot import CreateStateroot
from .deploy import Deploy
from .mount_var import MountVar
from .default_provisioner import DefaultProvisioner
from ..config import Config


StepsProvider = Callable[[Config], Sequence[DeployStep]]


def step(cls: Type[DeployStep]) -> StepsProvider:
    return lambda cfg: [cls(cfg)]


class DeploySteps:
    def __init__(self, cfg: Config, steps_providers: Iterable[StepsProvider]) -> None:
        self.steps = []  # type: Sequence[DeployStep]
        for get_steps in steps_providers:
            self.steps.extend(get_steps(cfg))

    def run(self):
        for step in self.steps:
            print('==>', step.title)
            step.run()

    def cleanup(self):
        for step in reversed(self.steps):
            self.do_cleanup(step)

    def do_cleanup(self, step: DeployStep):
        try:
            step.cleanup()
        except Exception:
            pass


def get_deploy_steps(cfg: Config) -> DeploySteps:
    return DeploySteps(cfg, [
        step(DeleteRemote),
        HttpRemote.get_steps,
        FileRemote.get_steps,
        step(PullRef),
        step(CreateStateroot),
        step(Deploy),
        step(MountVar),
        DefaultProvisioner.get_steps,
    ])
