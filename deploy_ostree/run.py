# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os
import subprocess
import sys
from typing import Dict, Optional


class ProcessResult:
    def __init__(
        self,
        args,
        exitcode: int,
        stdout: Optional[str]=None,
        stderr: Optional[str]=None
    ) -> None:
        self.args = args
        self.exitcode = exitcode
        self.stdout = stdout
        self.stderr = stderr

    @property
    def stdout_str(self) -> str:
        return self.stdout or ''

    @property
    def stderr_str(self) -> str:
        return self.stderr or ''

    @property
    def args_string(self) -> str:
        return ' '.join(self.args)


class ProcessError(RuntimeError):
    def __init__(self, result: ProcessResult) -> None:
        super().__init__("'%s' failed with status %s" % (result.args_string, result.exitcode))
        self.process_result = result


def run(
    args, *,
    capture_output: bool=False,
    encoding: str=sys.getfilesystemencoding(),
    env: Optional[Dict[str, str]]=None,
    check: bool=False
) -> ProcessResult:
    completed_process = subprocess.run(
        args,
        stdout=subprocess.PIPE if capture_output else None,
        stderr=subprocess.PIPE if capture_output else None,
        env=get_combined_env(env))
    result = convert_result(completed_process, args, encoding)
    if check and result.exitcode != 0:
        raise ProcessError(result)
    return result


def get_combined_env(env: Optional[Dict[str, str]]) -> Optional[Dict[str, str]]:
    if env is None:
        return None
    combined_env = os.environ.copy()
    combined_env.update(env)
    return combined_env


def convert_result(result: subprocess.CompletedProcess, args, encoding: str) -> ProcessResult:
    return ProcessResult(
        args,
        result.returncode,
        maybe_decode(result.stdout, encoding),
        maybe_decode(result.stderr, encoding))


def maybe_decode(value: Optional[bytes], encoding: str) -> Optional[str]:
    return value.decode(encoding) if value is not None else None
