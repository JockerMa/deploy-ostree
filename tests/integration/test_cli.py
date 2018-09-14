# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from .. import deploy_ostree


def should_print_error_and_exit_if_called_with_no_arguments():
    result = deploy_ostree([], check=False, capture_output=True)

    assert 'the following arguments are required' in result.stderr
    assert result.exitcode == 2


def should_print_help_and_exit_if_called_with_help_flag():
    result = deploy_ostree(['--help'], capture_output=True)

    assert 'deploy-ostree' in result.stdout
    assert 'deploy and configure an OSTree commit' in result.stdout
    assert result.exitcode == 0


def should_print_help_and_exit_if_called_with_h_flag():
    result = deploy_ostree(['-h'], capture_output=True)

    assert 'deploy-ostree' in result.stdout
    assert 'deploy and configure an OSTree commit' in result.stdout
    assert result.exitcode == 0
