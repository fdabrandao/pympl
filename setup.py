#!/usr/bin/env python
"""
This code is part of the Mathematical Modelling Toolbox PyMPL.

Copyright (C) 2015-2015, Filipe Brandao
Faculdade de Ciencias, Universidade do Porto
Porto, Portugal. All rights reserved. E-mail: <fdabrandao@dcc.fc.up.pt>.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
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
    version="0.1.0",
    license="GPLv3+",
    author="Filipe Brandao",
    author_email="fdabrandao@dcc.fc.up.pt",
    url="https://github.com/fdabrandao/pympl",
    description="Python extension to the AMPL modelling language",
    long_description=open("README.md").read(),
    packages=["pympl"],
    package_data={"": ls_dir("pympl/")},
    include_package_data=True,
    scripts=[os.path.join("scripts", f) for f in ls_dir("scripts/")],
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
