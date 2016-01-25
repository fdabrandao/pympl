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
from __future__ import division
from builtins import zip
from builtins import range

import os
import sys
from pympl import PyMPL, Tools, glpkutils

if __name__ == "__main__":
    sdir = os.path.dirname(__file__)
    if sdir != "":
        os.chdir(sdir)


def equivknapsack(a, a0, bounds=None):
    """
    Computes minimal equivalent knapsack inequalities using 'equivknapsack.mod'
    """
    if bounds is None:
        bounds = [a0]*len(a)
    for i in range(len(a)):
        bounds[i] = min(bounds[i], a0//a[i] if a[i] != 0 else 0)

    sum_a = sum(x*y for x, y in zip(a, bounds))
    aS = abs(2*a0+1-sum_a)
    if a0 < (sum_a-1)//2:
        a0 += aS
        fix_as = 1
    else:
        fix_as = 0
        if aS > a0:
            return [0]*len(a), 0, bounds
    a = a+[aS]
    bounds = bounds+[1]

    mod_in = "equivknapsack.mod"
    mod_out = "tmp/equivknapsack.out.mod"
    parser = PyMPL(locals_=locals())
    parser.parse(mod_in, mod_out)

    lp_out = "tmp/equivknapsack.lp"
    glpkutils.mod2lp(mod_out, lp_out)
    # exit_code = os.system("glpsol --math {0}".format(mod_out))
    # assert exit_code == 0
    out, varvalues = Tools.script(
        "glpk_wrapper.sh", lp_out, verbose=True
    )

    b = [varvalues.get("pi({0})".format(i+1), 0) for i in range(len(a))]
    b0 = varvalues.get("pi(0)", 0)

    if fix_as == 1:
        b0 -= b[-1]
        b = b[:-1]
    else:
        b = b[:-1]

    return b, b0, bounds


def main():
    """Tests equivknapsack"""

    kp_cons = [
        ([3, 5], 17, None)
    ]

    cons = set()
    for a, a0, bounds in kp_cons:
        b, b0, bounds = equivknapsack(a, a0, bounds)
        if sum(b) != 0:
            cons.add((tuple(b), b0, tuple(bounds)))

    print("Original knapsack inequalities:")
    for a, a0, bounds in sorted(kp_cons, key=lambda x: (x[1], x[0])):
        print(" + ".join(
            "{0:2g} x{1:d}".format(a[i], i+1) for i in range(len(a))
        ), "<=", a0, bounds)
    print("Minimal equivalent knapsack inequalities:")
    for b, b0, bounds in sorted(cons, key=lambda x: (x[1], x[0])):
        print(" + ".join(
            "{0:2g} x{1:d}".format(b[i], i+1) for i in range(len(b))
        ), "<=", b0, bounds[:-1])

if __name__ == "__main__":
    try:
        main()
    except ImportError as e:
        print(repr(e))
