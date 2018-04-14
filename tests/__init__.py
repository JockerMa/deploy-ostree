# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import sys
from typing import List
from deploy_ostree.run import run, ProcessResult, ProcessError


def deploy_ostree(extra_args: List[str]) -> ProcessResult:
    result = run(
        [sys.executable, '-mdeploy_ostree'] + extra_args,
        capture_output=True)
    print(result.stdout)
    print(result.stderr)
    return result


def ostree(extra_args: List[str]) -> ProcessResult:
    try:
        return run(
            ['ostree'] + extra_args,
            capture_output=True,
            check=True)
    except ProcessError as exc:
        print(exc.process_result.stderr)
        raise


__all__ = ['deploy_ostree', 'ostree']
