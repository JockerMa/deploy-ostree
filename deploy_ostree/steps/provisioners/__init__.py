# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from typing import Sequence
from ...config import Config
from .. import DeployStep
from .builtin import BuiltinProvisioner


def get_steps(cfg: Config) -> Sequence[DeployStep]:
    return [BuiltinProvisioner(cfg, provisioner) for provisioner in cfg.default_provisioners]
