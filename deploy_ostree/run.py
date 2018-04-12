# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import subprocess
import sys
from typing import Optional


class ProcessResult:
    def __init__(
        self,
        exitcode: int,
        stdout: Optional[str]=None,
        stderr: Optional[str]=None
    ) -> None:
        self.exitcode = exitcode
        self.stdout = stdout
        self.stderr = stderr


class ProcessError(RuntimeError):
    def __init__(self, result: ProcessResult) -> None:
        super().__init__('process returned status %s' % result.exitcode)
        self.process_result = result


def run(
    args, *,
    capture_output: bool=False,
    encoding: str=sys.getfilesystemencoding(),
    check: bool=False
) -> ProcessResult:
    completed_process = subprocess.run(
        args,
        stdout=subprocess.PIPE if capture_output else None,
        stderr=subprocess.PIPE if capture_output else None)
    result = convert_result(completed_process, encoding)
    if check and result.exitcode != 0:
        raise ProcessError(result)
    return result


def convert_result(result: subprocess.CompletedProcess, encoding: str) -> ProcessResult:
    return ProcessResult(
        result.returncode,
        maybe_decode(result.stdout, encoding),
        maybe_decode(result.stderr, encoding))


def maybe_decode(value: Optional[bytes], encoding: str) -> Optional[str]:
    return value.decode(encoding) if value is not None else None
