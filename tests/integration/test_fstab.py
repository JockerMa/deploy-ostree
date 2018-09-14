# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import pytest
from pathlib import Path


def files_equal(a: Path, b: Path) -> bool:
    with a.open() as f:
        a_content = f.read()
    with b.open() as f:
        return f.read() == a_content


@pytest.mark.usefixtures('ostree_setup', 'ostree_remote', 'deploy_ostree')
@pytest.mark.needs_isolation
class TestDefaultFstab:
    deploy_ostree = ['named-deploy.json']

    def should_copy_system_fstab_into_deployment(self, ostree_setup):
        fstab = ostree_setup.deployment('test-stateroot') / 'etc' / 'fstab'

        assert fstab.exists()
        assert files_equal(fstab, Path('/etc', 'fstab'))
