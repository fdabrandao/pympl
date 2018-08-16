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
from builtins import range
from builtins import map

import os
import sys
import pytest
try:
    runslow = pytest.config.getoption("--runslow")
except:
    runslow = False
slow = pytest.mark.skipif(not runslow, reason="need --runslow option to run")


inf = float("inf")
TESTS = {
    "LS_U": ("lslib_ls.mod", True),
    "LS_U1": ("lslib_ls.mod", True),
    "LS_U2": ("lslib_ls.mod", True),
    "LS_U_B": ("lslib_ls.mod", True),
    "LS_U_SC": ("lslib_ls.mod", True),
    "LS_U_SCB": ("lslib_ls.mod", True),
    "WW_U": ("lslib_ww.mod", True),
    "WW_U_B": ("lslib_ww.mod", True),
    "WW_U_SC": ("lslib_ww.mod", True),
    "WW_U_SCB": ("lslib_ww.mod", True),
    "WW_U_LB": ("lslib_ww.mod", False),
    "WW_CC": ("lslib_ww.mod", True),
    "WW_CC_B": ("lslib_ww.mod", True),
    "DLSI_CC": ("lslib_dls.mod", True),
    "DLSI_CC_B": ("lslib_dls.mod", True),
    "DLS_CC_B": ("lslib_dls.mod", True),
    "DLS_CC_SC": ("lslib_dls.mod", False),
}


def parse(mod_in, prob, relax, xform, test_seed):
    """Parse LS-LIB test files."""
    from pympl import PyMPL, glpkutils
    os.chdir(os.path.dirname(__file__) or os.curdir)

    mod_out = "tmp/lstlib_test.out.mod"
    TEST_PROB = prob  # pass the problem name to the model
    parser = PyMPL(locals_=locals(), globals_=globals())
    parser.parse(mod_in, mod_out)

    lp_out = "tmp/lslib_test.out.lp"
    glpkutils.mod2lp(mod_out, lp_out, verbose=False)
    return lp_out


def solve_gurobi(model):
    """Solve a lot-sizing model using Gurobi."""
    from pympl import Tools
    out, varvalues = Tools.script(
         "gurobi_wrapper.sh", model,
         options="Threads=1 Presolve=0 Heuristics=0.25 MIPGap=0",
         verbose=False
    )
    try:
        return varvalues["cost"]
    except:
        return inf


def solve_glpk(model):
    """Solve a lot-sizing model using GLPK."""
    from pympl import Tools
    out, varvalues = Tools.script("glpk_wrapper.sh", model, verbose=False)
    try:
        return varvalues["cost"]
    except:
        return inf


def xtest(prob, solve, ntests, approx=False):
    """Run LS-LIB routines."""
    fname, check_exact = TESTS[prob]
    if approx:
        check_exact = False
    for ind in range(ntests):
        model1 = parse(fname, prob, relax=True, xform=False, test_seed=ind)
        model2 = parse(fname, prob, relax=False, xform=False, test_seed=ind)
        model3 = parse(fname, prob, relax=True, xform=True, test_seed=ind)
        model4 = parse(fname, prob, relax=False, xform=True, test_seed=ind)
        z_lp1, z_ip1 = solve(model1), solve(model2)
        z_lp2, z_ip2 = solve(model3), solve(model4)
        print("---")
        print("test:", ind)
        print("z_ip1: {0:9.4f}\tz_ip2: {1:9.4f}\tdiff: {2:g}".format(
            z_ip1, z_ip2, abs(z_ip1-z_ip2)
        ))
        print("z_lp1: {0:9.4f}\tz_lp2: {1:9.4f}\tdiff: {2:g}".format(
            z_lp1, z_lp2, abs(z_lp1-z_lp2)
        ))
        print("z_lp2: {0:9.4f}\tz_ip2: {1:9.4f}\tdiff: {2:g}".format(
            z_lp2, z_ip2, abs(z_lp2-z_ip2)
        ))
        print("---")
        assert z_lp2 >= z_lp1
        assert abs(z_ip2-z_ip1) < 1e-5
        if check_exact:
            assert abs(z_ip2-z_lp2) < 1e-5


def test_lslib():
    """Test LS_LIB reformulations."""
    ntests = 1
    approx = False
    for prob_name in sorted(TESTS):
        xtest(prob_name, solve_glpk, ntests, approx)


@slow
def test_lslib_slow():
    """Test LS_LIB reformulations."""
    ntests = 10
    approx = False
    for prob_name in sorted(TESTS):
        xtest(prob_name, solve_gurobi, ntests, approx)


def main(prob_prefix="", ntests=50, approx=False):
    """Run all LS-LIB tests."""
    if prob_prefix in TESTS:
        xtest(prob_prefix, solve_gurobi, ntests, approx)
    else:
        for prob_name in sorted(TESTS):
            if prob_name.startswith(prob_prefix):
                xtest(prob_name, solve_gurobi, ntests, approx)


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        prefix = sys.argv[1]
        approx = len(sys.argv) == 3 and sys.argv[2] == "approx"
        main(prefix, 50, approx)
    else:
        main()
