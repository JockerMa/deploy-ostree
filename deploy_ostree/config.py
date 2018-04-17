# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import json
from typing import Any, Iterable, Mapping, Optional, TextIO
from uuid import uuid4


class InvalidConfigError(RuntimeError):
    pass


def random_string() -> str:
    return uuid4().hex[:12]


class ProvisionerConfig:
    def __init__(self, name: str, args: Mapping[str, Any]) -> None:
        self.name = name
        self.args = args

    def __eq__(self, other: Any):
        return (isinstance(other, ProvisionerConfig)
                and self.name == other.name
                and self.args == other.args)

    @classmethod
    def from_dicts(cls, data: Iterable[Mapping[str, Any]]):
        return [cls.from_dict(elem) for elem in data]

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]):
        name = data['provisioner']
        args = {key: value for key, value in data.items() if key != 'provisioner'}
        return cls(name, args)

    def __repr__(self):
        return 'ProvisionerConfig(name=%r, args=%r)' % (self.name, self.args)


class Config:
    def __init__(
        self,
        url: str,
        ref: str,
        remote: Optional[str]=None,
        stateroot: Optional[str]=None,
        default_provisioners: Iterable[ProvisionerConfig]=(),
    ) -> None:
        self.url = url
        self.ref = ref
        self.remote = remote or random_string()
        self.stateroot = stateroot or random_string()
        self.default_provisioners = list(default_provisioners)

    @classmethod
    def parse_json(cls, fobj: TextIO):
        data = json.load(fobj)
        try:
            return cls(
                url=data['url'],
                ref=data['ref'],
                remote=data.get('remote'),
                stateroot=data.get('stateroot'),
                default_provisioners=ProvisionerConfig.from_dicts(data.get('default-provisioners', ())),
            )
        except KeyError as exc:
            raise InvalidConfigError("missing key '{}'".format(exc.args[0]))
