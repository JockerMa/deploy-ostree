# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import argparse
import sys


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='deploy-ostree',
        description='deploy and configure an OSTree commit')

    parser.add_argument(
        'config',
        metavar='CONFIG',
        type=str,
        nargs=1,
        help='the path to the configuration file')

    return parser


def main():
    parser = build_argument_parser()
    parser.parse_args(sys.argv[1:])
