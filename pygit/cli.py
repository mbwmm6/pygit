import argparse
import os
import subprocess
import sys
import textwrap
import webbrowser

from . import base, data


def main():
    if len(sys.argv) == 1:
        sys.argv.append("--help")
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
    checkout_parse.add_argument("commit")

    tag_parse = commands.add_parser("tag")
    tag_parse.set_defaults(func=tag)
    tag_parse.add_argument("name")
    tag_parse.add_argument("oid", default="@", type=oid, nargs="?")

    k_parse = commands.add_parser("k")
    k_parse.set_defaults(func=k)

    branch_parse = commands.add_parser("branch")
    branch_parse.set_defaults(func=branch)
    branch_parse.add_argument("name")
    branch_parse.add_argument("start_point", default="@", type=oid, nargs="?")
    return parser.parse_args()


def init(args):
    base.init()
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
    for oid in base.iter_commits_and_parent({args.oid}):
        commit = base.get_commit(oid)
        print(f"commit {oid}\n")
        print(textwrap.indent(commit.message, "      "))
        print("")


def checkout(args):
    base.checkout(args.commit)


def tag(args):
    base.create_tag(args.name, args.oid)


def k(args):
    dot = ["digraph commits {"]
    oids = set()
    for refname, ref in data.iter_refs(defer=False):
        dot.append(f'"{refname}" [shape=note]')
        dot.append(f'"{refname}" -> "{ref.value}"')
    if not ref.symbolic:
        oids.add(ref.value)
    for oid in base.iter_commits_and_parent(oids):
        commit = base.get_commit(oid)
        dot.append(f'"{oid}" [shape=box style=filled label="{oid[:10]}"]')
        if commit.parent:
            dot.append(f'"{oid}" -> "{commit.parent}"')
    dot.append("}")
    dot_text = "\n".join(dot)
    print(dot_text)
    out = "commits.png"
    subprocess.run(["dot", "-Tpng", "-o", out], input=dot_text.encode(), check=True)
    webbrowser.open(os.path.abspath(out))


def branch(args):
    base.create_branch(args.name, args.start_point)
    print(f"Branch {args.name} created at {args.start_point[:10]}")
