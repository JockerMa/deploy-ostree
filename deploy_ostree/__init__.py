# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import argparse
import os.path
import sys

from .config import Config
from .run import ProcessError
from .steps import get_deploy_steps


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='deploy-ostree',
        description='deploy and configure an OSTree commit')

    parser.add_argument(
        'config',
        metavar='CONFIG',
        type=str,
        help='the path to the configuration file')

    return parser


def main():
    parser = build_argument_parser()
    args = parser.parse_args(sys.argv[1:])
    with open(args.config, encoding='utf-8') as fobj:
        cfg = Config.parse_json(fobj, base_dir=os.path.dirname(args.config))
    steps = get_deploy_steps(cfg)

    try:
        steps.run()
    except ProcessError as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)
