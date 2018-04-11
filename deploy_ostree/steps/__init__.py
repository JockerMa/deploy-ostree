# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from ..config import Config


class DeployStep:
    pass


class DeploySteps:
    def run(self):
        pass

    @classmethod
    def get(cls, config: Config):
        return cls()
