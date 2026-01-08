import argparse
import os
import sys
import textwrap

from . import base, data


def main():
    args = parse_args()
    args.func(args)


def parse_args():
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command")
    commands.required = True

    oid = base.get_oid

    init_parser = commands.add_parser("init")
    init_parser.set_defaults(func=init)

    hash_object_parse = commands.add_parser("hash-object")
    hash_object_parse.set_defaults(func=hash_object)
    hash_object_parse.add_argument("file")

    cat_file_parse = commands.add_parser("cat-file")
    cat_file_parse.set_defaults(func=cat_file)
    cat_file_parse.add_argument("object", type=oid)

    write_tree_parse = commands.add_parser("write-tree")
    write_tree_parse.set_defaults(func=write_tree)

    read_tree_parse = commands.add_parser("read-tree")
    read_tree_parse.set_defaults(func=base.read_tree)
    read_tree_parse.add_argument("tree", type=oid)

    commit_parse = commands.add_parser("commit")
    commit_parse.set_defaults(func=commit)
    commit_parse.add_argument("-m", "--message", required=True)

    log_parse = commands.add_parser("log")
    log_parse.set_defaults(func=log)
    log_parse.add_argument("oid", default="@", type=oid, nargs="?")

    checkout_parse = commands.add_parser("checkout")
    checkout_parse.set_defaults(func=checkout)
    checkout_parse.add_argument("oid", type=oid)

    tag_parse = commands.add_parser("tag")
    tag_parse.set_defaults(func=tag)
    tag_parse.add_argument("name")
    tag_parse.add_argument("oid", default="@", type=oid, nargs="?")

    k_parse = commands.add_parser("k")
    k_parse.set_defaults(func=k)
    return parser.parse_args()


def init(args):
    data.init()
    print(f"Initialized empty pygit repository in {os.getcwd()}/{data.GIT_DIR}")


def hash_object(args):
    with open(args.file, "rb") as f:
        print(data.hash_object(f.read()))


def cat_file(args):
    sys.stdout.flush()
    print(base.write_tree())


def write_tree(args):
    print(base.write_tree())


def read_tree(args):
    base.read_tree()
    print(base.commit(args.message))


def commit(args):
    print(base.commit(args.message))


def log(args):
    oid = args.oid
    while oid:
        commit = base.get_commit(oid)
        print(f"commit {oid}\n")
        print(textwrap.indent(commit.message, "      "))
        print("")
        oid = commit.parent


def checkout(args):
    base.checkout(args.oid)


def tag(args):
    base.create_tag(args.name, args.oid)


def k(args):
    oids = set()
    for refname, ref in data.iter_refs():
        print(refname, ref)
        oids.add(ref)
    for oid in base.iter_commits_and_parent(oids):
        commit = base.get_commit(oid)
        print(oid)
        if commit.parent:
            print("Parent", commit.parent)
