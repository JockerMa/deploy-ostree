# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from contextlib import ExitStack
from pathlib import Path
from unittest import mock
from deploy_ostree.config import Config, Source
from deploy_ostree.steps.create_stateroot import CreateStateroot


def should_have_title_string():
    assert isinstance(CreateStateroot(mock.Mock()).title, str)


def should_create_stateroot():
    sysroot = Path('/', 'mnt', 'rootfs')
    cfg = Config(Source.url('url'), 'ref', stateroot='stateroot-name', sysroot=str(sysroot))

    with ExitStack() as stack:
        exists = stack.enter_context(mock.patch('os.path.exists', mock.Mock(return_value=False)))
        run = stack.enter_context(mock.patch('deploy_ostree.steps.create_stateroot.run'))
        CreateStateroot(cfg).run()

    exists.assert_called_once_with('/mnt/rootfs/ostree/deploy/stateroot-name')
    run.assert_called_once_with([
        'ostree', 'admin', 'os-init',
        '--sysroot=%s' % sysroot,
        'stateroot-name'
    ], check=True)


def should_not_create_stateroot_if_path_exists():
    sysroot = Path('/', 'mnt', 'rootfs')
    cfg = Config(Source.url('url'), 'ref', stateroot='stateroot-name', sysroot=str(sysroot))

    with ExitStack() as stack:
        exists = stack.enter_context(mock.patch('os.path.exists', mock.Mock(return_value=True)))
        run = stack.enter_context(mock.patch('deploy_ostree.steps.create_stateroot.run'))
        CreateStateroot(cfg).run()

    exists.assert_called_once_with('/mnt/rootfs/ostree/deploy/stateroot-name')
    run.assert_not_called()
