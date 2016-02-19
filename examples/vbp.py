#!/usr/bin/env python
"""
This code is part of the Mathematical Programming Toolbox PyMPL.

Copyright (C) 2015-2016, Filipe Brandao
Faculdade de Ciencias, Universidade do Porto
Porto, Portugal. All rights reserved. E-mail: <fdabrandao@dcc.fc.up.pt>.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import print_function

import os
import sys
from pympl import PyMPL, Tools, glpkutils

if __name__ == "__main__":
    sdir = os.path.dirname(__file__)
    if sdir != "":
        os.chdir(sdir)


def main():
    """Parses 'vbp.mod'"""

    mod_in = "vbp.mod"
    mod_out = "tmp/vbp.out.mod"
    parser = PyMPL()
    parser.parse(mod_in, mod_out)

    lp_out = "tmp/instance.lp"
    glpkutils.mod2lp(mod_out, lp_out, True)
    out, varvalues = Tools.script(
        "glpk_wrapper.sh", lp_out, verbose=True
    )
    sol = parser["VBP_FLOW"].extract(
        lambda varname: varvalues.get(varname, 0),
        verbose=True
    )

    print("")
    print("sol:", sol)
    print("varvalues:", [(k, v) for k, v in sorted(varvalues.items())])
    print("")
    assert varvalues["Z"] == 33  # check the solution objective value

    # exit_code = os.system("glpsol --math {0}".format(mod_out))
    # assert exit_code == 0

if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        print(repr(e))
