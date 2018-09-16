# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import pytest
from pathlib import Path
from ..util import files_equal, FileMode


@pytest.mark.usefixtures('ostree_setup', 'ostree_remote', 'deploy_ostree')
@pytest.mark.needs_isolation
class TestDefaultFstab:
    deploy_ostree = ['named-deploy.json']

    def should_copy_system_fstab_into_deployment(self, ostree_setup):
        fstab = ostree_setup.deployment('test-stateroot') / 'etc' / 'fstab'
        assert fstab.exists()
        assert files_equal(fstab, Path('/etc', 'fstab'))

    def should_normalize_owner_and_mode(self, ostree_setup):
        fstab = ostree_setup.deployment('test-stateroot') / 'etc' / 'fstab'
        assert FileMode.for_path(fstab) == FileMode(0, 0, 0o644, True)


@pytest.mark.usefixtures('ostree_setup', 'ostree_remote', 'deploy_ostree')
@pytest.mark.needs_isolation
class TestFstabArgument:
    deploy_ostree = ['named-deploy.json']

    @pytest.fixture(scope='class', autouse=True)
    def temp_fstab(self, tempdir_cls):
        fstab = tempdir_cls / 'fstab'
        with fstab.open('w') as f:
            f.write('test fstab')
        FileMode(1000, 1000, 0o703, True).apply(fstab)
        self.__class__.deploy_ostree.insert(0, '--fstab=%s' % fstab)
        return fstab

    def should_copy_specified_fstab_into_deployment_with_correct_mode_bits(self, temp_fstab, ostree_setup):
        fstab = ostree_setup.deployment('test-stateroot') / 'etc' / 'fstab'
        assert fstab.exists()
        assert files_equal(fstab, temp_fstab)

    @pytest.mark.xfail
    def should_normalize_owner_and_mode(self, ostree_setup):
        fstab = ostree_setup.deployment('test-stateroot') / 'etc' / 'fstab'
        assert FileMode.for_path(fstab) == FileMode(0, 0, 0o644, True)
