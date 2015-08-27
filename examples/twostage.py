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


def read_twostage(fname):
    """Loads two-stage instances."""
    with open(fname) as f:
        lst = map(int, f.read().split())
        W = lst.pop(0)
        H = lst.pop(0)
        m = lst.pop(0)
        w, h, b = [], [], []
        for i in xrange(m):
            w.append(lst.pop(0))
            h.append(lst.pop(0))
            b.append(lst.pop(0))
        return W, H, w, h, b


def main():
    """Parses 'twostage.mod'."""

    mod_in = "twostage.mod"
    mod_out = "tmp/twostage.out.mod"
    parser = PyMPL(locals_=locals(), globals_=globals())
    parser.parse(mod_in, mod_out)

    lp_out = "tmp/twostage.lp"
    glpkutils.mod2lp(mod_out, lp_out, True)

    out, varvalues = script_wsol(
        "glpk_wrapper.sh", lp_out, verbose=True
    )

    print("")
    print("varvalues:", [
        (k, v)
        for k, v in sorted(varvalues.items()) if not k.startswith("_")
    ])
    print("")
    assert varvalues["Z"] == 15  # check the solution objective value

    parser["VBP_FLOW"].extract(
        lambda name: varvalues.get(name, 0),
        verbose=True
    )

if __name__ == "__main__":
    main()
