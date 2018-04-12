# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import json
from typing import TextIO


class InvalidConfigError(RuntimeError):
    pass


class Config:
    def __init__(
        self,
        url: str,
        ref: str,
        remote: str='deploy-ostree-remote',
    ) -> None:
        self.url = url
        self.ref = ref
        self.remote = remote

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
