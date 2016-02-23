#!/usr/bin/env python
"""
PyMPL
-----
PyMPL is a python extension to the AMPL modelling language that adds
new statements for evaluating python code within AMPL/GMPL models.
PyMPL also includes, among others, procedures for modelling piecewise
linear functions, compressed arc-flow graphs for vector packing,
sub-tour elimination constraints for TSP, and lot-sizing reformulations.
PyMPL is fully compatible with both python 2 and 3.

Setup
`````

.. code:: bash

    $ pip install pympl

Links
`````

* `PyMPL documentation <https://github.com/fdabrandao/pympl/wiki>`_
* `GiHub repository <https://github.com/fdabrandao/pympl>`_
* `BitBucket repository <https://bitbucket.org/fdabrandao/pympl>`_
"""
import re
import os
import ast
from distutils.core import setup
from pkg_resources import parse_version


def ls_dir(base_dir):
    """List files recursively."""
    base_dir = os.path.join(base_dir, "")
    return [
        os.path.join(dirpath.replace(base_dir, "", 1), f)
        for (dirpath, dirnames, files) in os.walk(base_dir)
        for f in files
        if (
            not f.endswith(("~", ".pyc", ".pyo", ".log")) and
            not f.startswith(".")
        )
    ]

_version_re = re.compile(r'__version__\s+=\s+(.*)')
with open("pympl/__init__.py", "rb") as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode("utf-8")).group(1)))
    # assert str(parse_version(version)) == version

setup(
    name="PyMPL",
    version=version,
    license="AGPLv3+",
    author="Filipe Brandao",
    author_email="fdabrandao@dcc.fc.up.pt",
    url="https://github.com/fdabrandao/pympl",
    description="Mathematical Programming Toolbox for AMPL/GMPL",
    long_description=__doc__,
    packages=["pympl"],
    package_data={"": ls_dir("pympl/")},
    scripts=[os.path.join("scripts", f) for f in ls_dir("scripts/")],
    platforms="any",
    install_requires=open("requirements.txt").read().split("\n"),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Topic :: Scientific/Engineering"
    ],
)
