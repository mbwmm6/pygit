import hashlib
import os

GIT_DIR = ".pygit"


def init():
    os.makedirs(GIT_DIR)
    os.makedirs(f"{GIT_DIR}/objects")


def hash_object(data):
    oid = hashlib.sha256(data).hexdigest()
    with open(f"{GIT_DIR}/objects/{oid}", "wb") as out:
        out.write(data)
    return oid


def get_object(oid):
    with open(f"{GIT_DIR}/objects/{oid}", "rb") as f:
        return f.read()
