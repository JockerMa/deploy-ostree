# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import json
import os.path
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


class Source:
    def __init__(self, type: str, value: str) -> None:
        self.type = type
        self.value = value

    @staticmethod
    def url(value: str):
        return Source('url', value)

    @staticmethod
    def path(value: str):
        return Source('path', value)

    @property
    def is_url(self):
        return self.type == 'url'

    @property
    def is_path(self):
        return self.type == 'path'


class Config:
    def __init__(
        self,
        source: Source,
        ref: str,
        *,
        base_dir: str='',
        remote: Optional[str]=None,
        stateroot: Optional[str]=None,
        kernel_args: Iterable[str]=(),
        default_provisioners: Iterable[ProvisionerConfig]=()
    ) -> None:
        self._source = source
        self.ref = ref
        self.base_dir = base_dir
        self.remote = remote or random_string()
        self.stateroot = stateroot or random_string()
        self.kernel_args = list(kernel_args)
        self.default_provisioners = list(default_provisioners)
        self.deployment_name = None  # type: Optional[str]

    @property
    def url(self) -> Optional[str]:
        return self._source.value if self._source.is_url else None

    @property
    def path(self) -> Optional[str]:
        return os.path.join(self.base_dir, self._source.value) if self._source.is_path else None

    @property
    def var_dir(self) -> str:
        return os.path.join('/ostree', 'deploy', self.stateroot, 'var')

    @property
    def deployment_dir(self) -> str:
        if self.deployment_name is None:
            raise RuntimeError('deployment name not set')
        return os.path.join('/ostree', 'deploy', self.stateroot, 'deploy', self.deployment_name)

    def set_deployment_name(self, deployment: str) -> None:
        self.deployment_name = deployment

    @classmethod
    def parse_json(cls, fobj: TextIO, *, base_dir=''):
        data = json.load(fobj)

        if 'url' in data and 'path' in data:
            raise InvalidConfigError("both 'url' and 'path' are present")
        elif 'url' in data:
            source = Source.url(data['url'])
        elif 'path' in data:
            source = Source.path(data['path'])
        else:
            raise InvalidConfigError("neither 'url' nor 'path' are present")

        try:
            return cls(
                source=source,
                ref=data['ref'],
                base_dir=base_dir,
                remote=data.get('remote'),
                stateroot=data.get('stateroot'),
                kernel_args=data.get('kernel-args', ()),
                default_provisioners=ProvisionerConfig.from_dicts(data.get('default-provisioners', ())),
            )
        except KeyError as exc:
            raise InvalidConfigError("missing key '{}'".format(exc.args[0]))
