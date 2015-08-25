#!/usr/bin/env python
"""
PyMPL
-----
PyMPL is a python extension to the AMPL modelling language that adds
new statements for evaluating python code within AMPL models.
PyMPL includes, among others, procedures for modelling piecewise linear
functions, arc-flow graphs for vector packing, and sub-tour elimination
constraints for TSP.

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

import os
from setuptools import setup
from setuptools.command.install import install


class CustomInstallCommand(install):
    """Custom Install Command."""

    def run(self):
        os.system("/bin/cp " + self.install_scripts)
        install.run(self)


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


setup(
    name="PyMPL",
    version="0.3.0",
    license="GPLv3+",
    author="Filipe Brandao",
    author_email="fdabrandao@dcc.fc.up.pt",
    url="https://github.com/fdabrandao/pympl",
    description="Python extension to the AMPL modelling language",
    long_description=__doc__,
    packages=["pympl"],
    package_data={"": ls_dir("pympl/")},
    include_package_data=True,
    scripts=[os.path.join("scripts", f) for f in ls_dir("scripts/")],
    platforms='any',
    install_requires=[],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Topic :: Scientific/Engineering"
    ],
    cmdclass={"install": CustomInstallCommand},
    use_2to3=True
)
