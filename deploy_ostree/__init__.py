# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import argparse
from io import TextIOWrapper
import os.path
import sys
from urllib.parse import urlparse
from urllib.request import urlopen

from .config import Config
from .run import ProcessError
from .steps import get_deploy_steps


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='deploy-ostree',
        description='deploy and configure an OSTree commit'
    )

    parser.add_argument(
        '--sysroot',
        metavar='SYSROOT',
        dest='sysroot',
        type=str,
        help='root directory to work in'
    )
    parser.add_argument(
        '--root-karg',
        metavar='ROOT',
        dest='root_karg',
        type=str,
        help='root partition to pass to the kernel (default: autodetect)'
    )
    parser.add_argument(
        'config',
        metavar='CONFIG',
        type=str,
        help='the path to the configuration file'
    )

    return parser


def parse_config(filename_or_url, sysroot=None, root_karg=None) -> Config:
    parsed_url = urlparse(filename_or_url)
    if parsed_url.scheme in ['http', 'https']:
        with urlopen(filename_or_url) as req:
            return Config.parse_json(
                TextIOWrapper(req, encoding='utf-8'),
                base_dir=os.getcwd(),
                sysroot=sysroot,
                root_karg=root_karg,
            )
    with open(filename_or_url, encoding='utf-8') as fobj:
        return Config.parse_json(
            fobj,
            base_dir=os.path.dirname(filename_or_url),
            sysroot=sysroot,
            root_karg=root_karg,
        )


def main():
    parser = build_argument_parser()
    args = parser.parse_args(sys.argv[1:])
    cfg = parse_config(args.config, args.sysroot, args.root_karg)
    steps = get_deploy_steps(cfg)

    try:
        steps.run()
    except ProcessError as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)
    finally:
        steps.cleanup()
