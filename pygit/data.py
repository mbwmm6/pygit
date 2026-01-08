import hashlib
import os
from collections import namedtuple

GIT_DIR = ".pygit"


def init():
    os.makedirs(GIT_DIR)
    os.makedirs(f"{GIT_DIR}/objects")


RefValue = namedtuple("RefValue", ["symbolic", "value"])


def set_HEAD(oid):
    with open(f"{GIT_DIR}/HEAD", "w") as f:
        f.write(oid)


def get_HEAD():
    if os.path.isfile(f"{GIT_DIR}/HEAD"):
        with open(f"{GIT_DIR}/HEAD") as f:
            return f.read().strip()


def hash_object(data, type_="blob"):
    obj = type_.encode() + b"\x00" + data
    oid = hashlib.sha256(obj).hexdigest()
    with open(f"{GIT_DIR}/objects/{oid}", "wb") as out:
        out.write(obj)
    return oid


def get_object(oid, expected="blob"):
    with open(f"{GIT_DIR}/objects/{oid}", "rb") as f:
        obj = f.read()
    type_, _, content = obj.partition(b"\x00")
    type_ = type_.decode()
    if expected is not None:
        assert type_ == expected, f"Expected {expected}, got {type_}"
    return content


def update_ref(ref, value, defer=True):
    assert not value.symbolic
    ref = _get_ref_internal(ref, defer)[0]
    ref_path = f"{GIT_DIR}/{ref}"
    os.makedirs(os.path.dirname(ref_path), exist_ok=True)
    with open(f"{GIT_DIR}/{ref}", "w") as f:
        f.write(value.value)


def get_ref(ref, defer=True):
    return _get_ref_internal(ref, defer)[1]


def _get_ref_internal(ref, defer):
    ref_path = f"{GIT_DIR}/{ref}"
    value = None
    if os.path.isfile(ref_path):
        with open(ref_path) as f:
            value = f.read().strip()
    symbolic = bool(value) and value.startswith("ref:")
    if symbolic:
        value = value.split(":", 1)[1].strip()
        if defer:
            return _get_ref_internal(value, defer=False)
    return ref, RefValue(symbolic=False, value=value)


def iter_refs(defer=True):
    refs = ["HEAD"]
    for root, _, filenames in os.walk(f"{GIT_DIR}/refs/"):
        root = os.path.relpath(root, GIT_DIR)
        refs.extend(f"{root}/{name}" for name in filenames)
    for refname in refs:
        yield refname, get_ref(refname, defer=defer)
