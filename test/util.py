# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os.path
import subprocess
import sys
from typing import List, Iterable, Dict, Any


SOURCE_PATH = os.path.join(os.path.dirname(__file__), os.pardir, 'src')


def env_with_pythonpath(pythonpath: Iterable[str]) -> Dict[str, Any]:
    env = dict(os.environ)
    env['PYTHONPATH'] = os.pathsep.join(pythonpath)
    return env


def get_merged_env() -> Dict[str, Any]:
    source_path = SOURCE_PATH
    return env_with_pythonpath([source_path])


def deploy_ostree(extra_args: List[str]) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, '-mdeploy_ostree'] + extra_args,
            env=get_merged_env(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)


__all__ = ['deploy_ostree']
