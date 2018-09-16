# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from collections import namedtuple
import os
from pathlib import PurePath
import stat


def touch(path: PurePath):
    with open(str(path), 'w'):
        pass


def files_equal(a: PurePath, b: PurePath) -> bool:
    with open(str(a)) as f:
        a_content = f.read()
    with open(str(b)) as f:
        return f.read() == a_content


class FileMode(namedtuple('_FileMode', 'uid gid mode isfile')):
    @staticmethod
    def for_path(path: PurePath) -> 'FileMode':
        st = os.stat(str(path), follow_symlinks=False)
        return FileMode(
            st.st_uid,
            st.st_gid,
            stat.S_IMODE(st.st_mode),
            stat.S_ISREG(st.st_mode)
        )

    def apply(self, path: PurePath):
        os.chown(str(path), self.uid, self.gid)
        os.chmod(str(path), self.mode)
