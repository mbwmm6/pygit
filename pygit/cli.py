import argparse
import os
import sys

from . import base
from . import data


def main():
    args = parse_args()
    args.func(args)


def parse_args():
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command")
    commands.required = True

    init_parser = commands.add_parser("init")
    init_parser.set_defaults(func=init)

    hash_object_parse = commands.add_parser("hash-object")
    hash_object_parse.set_defaults(func=hash_object)
    hash_object_parse.add_argument("file")

    cat_file_parse = commands.add_parser("cat-file")
    cat_file_parse.set_defaults(func=cat_file)

    write_tree_parse = commands.add_parser("write-tree")
    write_tree_parse.set_defaults(func=write_tree)

    return parser.parse_args()


def init(args):
    data.init()
    print(f"Initialized empty pygit repository in {os.getcwd()}/{data.GIT_DIR}")


def hash_object(args):
    with open(args.file, "rb") as f:
        print(data.hash_object(f.read()))


def cat_file(args):
    sys.stdout.flush()
    sys.stdout.buffer.write(data.get_object(args.object, expected=None))


def write_tree(args):
    print(base.write_tree())
