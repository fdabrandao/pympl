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
    """Parses 'bike.mod'"""

    mod_in = "bike.mod"
    mod_out = "tmp/bike.out.mod"
    parser = PyMPL(locals_=locals(), globals_=globals())
    parser.parse(mod_in, mod_out)

    lp_out = "tmp/bike.lp"
    glpkutils.mod2lp(mod_out, lp_out, True)
    try:
        out, varvalues = script_wsol(
            "glpk_wrapper.sh", lp_out, verbose=True
        )
    except Exception as e:
        print repr(e)

    #print "varvalues:", [(k, v) for k, v in sorted(varvalues.items())]


if __name__ == "__main__":
    main()
