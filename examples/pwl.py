#!/usr/bin/env python
"""
This code is part of the Mathematical Programming Toolbox PyMPL.

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
from __future__ import print_function

import os
import sys
sdir = os.path.dirname(__file__)
if sdir != "":
    os.chdir(sdir)

if __name__ == "__main__":
    if "test_install" in sys.argv:
        sys.argv.remove("test_install")
    else:
        project_dir = "../"
        sys.path.insert(0, project_dir)
        os.environ["PATH"] = "{0}/scripts:{1}".format(
            project_dir, os.environ["PATH"]
        )

from pympl import PyMPL, glpkutils, script_wsol


def main():
    """Parses 'pwl.mod'."""

    mod_in = "pwl.mod"
    mod_out = "tmp/pwl.out.mod"
    parser = PyMPL(locals_=locals(), globals_=globals())
    parser.parse(mod_in, mod_out)

    lp_out = "tmp/pwl.lp"
    glpkutils.mod2lp(mod_out, lp_out, True)
    out, varvalues = script_wsol(
        "glpk_wrapper.sh", lp_out, verbose=True
    )

    print("varvalues:", [
        (k, v)
        for k, v in sorted(varvalues.items()) if not k.startswith("_")
    ])

    exit_code = os.system("glpsol --math {0} | grep -v _".format(mod_out))
    assert exit_code == 0

if __name__ == "__main__":
    main()
