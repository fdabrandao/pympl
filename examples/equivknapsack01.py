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
from builtins import range
from builtins import str
import os


def equivknapsack01(a, a0):
    """Compute a minimal equivalent 0-1 knapsack inequalitie."""
    from pympl import PyMPL, Tools, glpkutils
    os.chdir(os.path.dirname(__file__) or os.curdir)

    aS = abs(2*a0+1-sum(a))
    if a0 < (sum(a)-1)//2:
        a0 += aS
        fix_as = 1
    else:
        fix_as = 0
        if aS > a0:
            return [0]*len(a), 0
    a = list(a)+[aS]

    mod_in = "equivknapsack01.mod"
    mod_out = "tmp/equivknapsack01.out.mod"

    parser = PyMPL(locals_=locals(), globals_=globals())
    parser.parse(mod_in, mod_out)

    lp_out = "tmp/equivknapsack01.lp"
    glpkutils.mod2lp(mod_out, lp_out, verbose=True)
    # exit_code = os.system("glpsol --math {0}".format(mod_out))
    # assert exit_code == 0
    out, varvalues = Tools.script(
        "glpk_wrapper.sh", lp_out, verbose=False
    )

    b = [varvalues.get("pi({0})".format(i+1), 0) for i in range(len(a))]
    b0 = varvalues.get("pi(0)", 0)

    if fix_as == 1:
        b0 -= b[-1]
        b = b[:-1]
    else:
        b = b[:-1]

    return tuple(b), b0


def main():
    """Test equivknapsack01."""
    kp_cons = [
        ((8, 12, 13, 64, 22, 41), 80),
        ((8, 12, 13, 75, 22, 41), 96),
        ((3, 6, 4, 18, 6, 4), 20),
        ((5, 10, 8, 32, 6, 12), 36),
        ((5, 13, 8, 42, 6, 20), 44),
        ((5, 13, 8, 48, 6, 20), 48),
        ((0, 0, 0, 0, 8, 0), 10),
        ((3, 0, 4, 0, 8, 0), 18),
        ((3, 2, 4, 0, 8, 4), 22),
        ((3, 2, 4, 8, 8, 4), 24),
        # ((3, 3, 3, 3, 3, 5, 5, 5), 17),
    ]
    min_kp_cons = [
        ((1, 1, 1, 4, 1, 1), 4),
        ((1, 1, 1, 4, 2, 2), 5),
        ((0, 1, 1, 5, 2, 2), 6),
        ((1, 1, 1, 2, 2, 1), 6),
        ((1, 2, 2, 6, 1, 2), 6),
    ]

    cons = set()
    for a, a0 in kp_cons:
        b, b0 = equivknapsack01(a, a0)
        if sum(b) != 0:
            cons.add((b, b0))

    print("Original knapsack inequalities:")
    for a, a0 in sorted(kp_cons, key=lambda x: (x[1], x[0])):
        print(" + ".join(
            "{0:2g} x{1:d}".format(a[i], i+1) for i in range(len(a))
        ), "<=", a0)
    print("Minimal equivalent knapsack inequalities:")
    for b, b0 in sorted(cons, key=lambda x: (x[1], x[0])):
        print(" + ".join(
            "{0:2g} x{1:d}".format(b[i], i+1) for i in range(len(b))
        ), "<=", b0)
        assert (b, b0) in min_kp_cons


if __name__ == "__main__":
    main()
