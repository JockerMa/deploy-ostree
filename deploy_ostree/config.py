# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import json
from typing import TextIO


class Config:
    def __init__(
        self,
        url: str,
        ref: str
    ) -> None:
        self.url = url
        self.ref = ref

    @classmethod
    def parse_json(cls, fobj: TextIO) -> 'Config':
        data = json.load(fobj)
        return Config(
            data['ostree_url'],
            data['ref'],
        )
