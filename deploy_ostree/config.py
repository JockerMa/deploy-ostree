# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import json
from typing import Optional, TextIO
from uuid import uuid4


class InvalidConfigError(RuntimeError):
    pass


def random_string() -> str:
    return uuid4().hex[:12]


class Config:
    def __init__(
        self,
        url: str,
        ref: str,
        remote: Optional[str]=None,
    ) -> None:
        self.url = url
        self.ref = ref
        self.remote = remote if remote else random_string()

    @classmethod
    def parse_json(cls, fobj: TextIO):
        data = json.load(fobj)
        try:
            return cls(
                data['ostree_url'],
                data['ref'],
            )
        except KeyError as exc:
            raise InvalidConfigError("missing key '{}'".format(exc.args))
