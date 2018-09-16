# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import pytest
import os
from pathlib import Path
import stat


def files_equal(a: Path, b: Path) -> bool:
    with a.open() as f:
        a_content = f.read()
    with b.open() as f:
        return f.read() == a_content


def assert_has_owner_and_mode(path: Path, uid: int, gid: int, mode: int) -> None:
    st = os.stat(str(path), follow_symlinks=False)
    assert st.st_uid == 0
    assert st.st_gid == 0
    assert stat.S_ISREG(st.st_mode)
    assert stat.S_IMODE(st.st_mode) == 0o644


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
        assert_has_owner_and_mode(fstab, 0, 0, 0o644)


@pytest.mark.usefixtures('ostree_setup', 'ostree_remote', 'deploy_ostree')
@pytest.mark.needs_isolation
class TestFstabArgument:
    deploy_ostree = ['named-deploy.json']

    @pytest.fixture(scope='class', autouse=True)
    def temp_fstab(self, tempdir_cls):
        fstab = tempdir_cls / 'fstab'
        with fstab.open('w') as f:
            f.write('test fstab')
        os.chown(str(fstab), 1000, 1000)
        os.chmod(str(fstab), 0o703)
        self.__class__.deploy_ostree.insert(0, '--fstab=%s' % fstab)
        return fstab

    def should_copy_specified_fstab_into_deployment_with_correct_mode_bits(self, temp_fstab, ostree_setup):
        fstab = ostree_setup.deployment('test-stateroot') / 'etc' / 'fstab'
        assert fstab.exists()
        assert files_equal(fstab, temp_fstab)

    @pytest.mark.xfail
    def should_normalize_owner_and_mode(self, ostree_setup):
        fstab = ostree_setup.deployment('test-stateroot') / 'etc' / 'fstab'
        assert_has_owner_and_mode(fstab, 0, 0, 0o644)
