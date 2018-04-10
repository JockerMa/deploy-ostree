# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os.path
from shutil import which
import subprocess
import sys
from typing import List, Iterable, Dict, Any, Optional


SOURCE_PATH = os.path.join(os.path.dirname(__file__), os.pardir, 'src')


def env_with_pythonpath(pythonpath: Iterable[str]) -> Dict[str, Any]:
    env = dict(os.environ)
    env['PYTHONPATH'] = os.pathsep.join(pythonpath)
    return env


def get_merged_env() -> Dict[str, Any]:
    source_path = SOURCE_PATH
    return env_with_pythonpath([source_path])


def maybe_decode(arg: Optional[bytes]) -> str:
    return arg.decode(sys.getfilesystemencoding()) if arg else ''


class ProcessResult:
    def __init__(self, result: subprocess.CompletedProcess) -> None:
        self.returncode = result.returncode
        self.stdout = maybe_decode(result.stdout)
        self.stderr = maybe_decode(result.stderr)


def run(*args, **kwargs) -> ProcessResult:
    return ProcessResult(subprocess.run(*args, **kwargs))


def deploy_ostree(extra_args: List[str]) -> ProcessResult:
    return run(
        [sys.executable, '-mdeploy_ostree'] + extra_args,
        env=get_merged_env(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)


def ostree(extra_args: List[str]) -> ProcessResult:
    try:
        return run(
            [which('ostree')] + extra_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=True)
    except subprocess.CalledProcessError as exc:
        print(maybe_decode(exc.stdout))
        raise


__all__ = ['deploy_ostree', 'ostree', 'ProcessResult']
