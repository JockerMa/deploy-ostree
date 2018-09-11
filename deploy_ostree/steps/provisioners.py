# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from typing import Sequence
from ..config import Config
from . import DeployStep
from .default_provisioner import DefaultProvisioner


def get_steps(cfg: Config) -> Sequence[DeployStep]:
    return [DefaultProvisioner(cfg, provisioner) for provisioner in cfg.default_provisioners]
