from setuptools import setup

setup(
    name="pygit",
    version="0.1",
    package=["pygit"],
    entry_points={"console_scripts": ["pygit = pygit.cli:main"]},
)
