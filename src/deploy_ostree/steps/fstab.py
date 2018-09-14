# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import shutil
from pathlib import Path
from . import DeployStep


class Fstab(DeployStep):
    @property
    def title(self) -> str:
        return 'copying %s into deployment' % self.config.fstab

    def run(self):
        fstab = Path(self.config.deployment_dir, 'etc', 'fstab')
        shutil.copy(str(self.config.fstab), str(fstab))
