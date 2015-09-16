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
from builtins import map
from builtins import range

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


def read_demand(fname, NI, NT):
    with open(fname) as f:
        text = f.read().replace(",", "")
        lst = list(map(float, text.split()))
        demand = {}
        for i in range(NI):
            for t in range(NT):
                demand[i+1, t+1] = lst.pop(0)
        assert lst == []
        return demand


def main():
    """Parses 'clb.mod'"""

    mod_in = "clb.mod"
    mod_out = "tmp/clb.out.mod"
    parser = PyMPL(locals_=locals(), globals_=globals())
    parser.parse(mod_in, mod_out)

    lp_out = "tmp/clb.lp"
    glpkutils.mod2lp(mod_out, lp_out, True)
    try:
        out, varvalues = script_wsol(
            "gurobi_wrapper.sh", lp_out,
            options="Threads=1 Presolve=0 Heuristics=0.25 MIPGap=0", verbose=True
        )
    except Exception as e:
        print(repr(e))

    #print "varvalues:", [(k, v) for k, v in sorted(varvalues.items())]

if __name__ == "__main__":
    main()
