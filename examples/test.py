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

import sys
import wolsey
import equivknapsack01
import equivknapsack
import vpsolver_vbp
import vpsolver_mvp
import twostage
import tsp_gurobi
import tsp
import sos
import pwl
import lslib_test


def main():
    """Runs PyMPL examples."""
    try:
        print("equivknapsack:")
        equivknapsack.main()
    except ImportError as e:
        print(repr(e))

    try:
        print("equivknapsack01:")
        equivknapsack01.main()
    except ImportError as e:
        print(repr(e))

    try:
        print("wolsey:")
        wolsey.main()
    except ImportError as e:
        print(repr(e))

    try:
        print("vpsolver_vbp:")
        vpsolver_vbp.main()
    except ImportError as e:
        print(repr(e))

    try:
        print("vpsolver_mvp:")
        vpsolver_mvp.main()
    except ImportError as e:
        print(repr(e))

    try:
        print("twostage:")
        twostage.main()
    except ImportError as e:
        print(repr(e))

    print("sos:")
    sos.main()

    print("pwl:")
    pwl.main()

    if "quick_test" not in sys.argv:
        print("tsp:")
        tsp.main()

    if "quick_test" not in sys.argv:
        print("tsp_gurobi:")
        try:
            tsp_gurobi.main()
        except ImportError as e:
            print(repr(e))

    if "quick_test" not in sys.argv:
        print("lslib_test:")
        try:
            lslib_test.main()
        except Exception as e:
            print(repr(e))


if __name__ == "__main__":
    import os
    sdir = os.path.dirname(__file__)
    if sdir != "":
        os.chdir(sdir)
    main()
