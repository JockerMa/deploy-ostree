# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import pytest
from pathlib import Path
from deploy_ostree.config import Config, Source
from deploy_ostree.steps import Fstab


@pytest.fixture
def deploy_config():
    return Config(Source.url('url'), 'ref')


def should_have_title_string(deploy_config):
    assert isinstance(Fstab(deploy_config).title, str)


def should_copy_fstab_into_deployment(tempdir: Path):
    with (tempdir / 'fstab').open('w') as f:
        f.write('test fstab')
    config = Config(Source.url('url'), 'ref', stateroot='stateroot', sysroot=str(tempdir), fstab=tempdir / 'fstab')
    config.set_deployment_name('deployment')
    Path(config.deployment_dir, 'etc').mkdir(parents=True)

    Fstab(config).run()

    fstab = Path(config.deployment_dir, 'etc', 'fstab')
    assert fstab.exists and fstab.is_file()
    with fstab.open() as f:
        assert f.read() == 'test fstab'
