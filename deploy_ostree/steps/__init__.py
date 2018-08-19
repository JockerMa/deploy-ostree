# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from typing import Iterable, List, Type  # noqa
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
        DeleteRemote,
        HttpRemote,
        FileRemote,
        PullRef,
        CreateStateroot,
        Deploy,
        MountVar,
        DefaultProvisioner,
    ])
