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


def read_tsp(fname):
    """Load a TSP instance from a file."""
    xs, ys = [], []
    with open(fname) as f:
        lst = list(map(float, f.read().split()))
        n = int(lst.pop(0))
        for i in range(n):
            xs.append(lst.pop(0))
            ys.append(lst.pop(0))
    return n, xs, ys


def main():
    """Solve 'tsp_gurobi.mod' using a cut generator."""
    from pympl import PyMPL, Tools, glpkutils
    from gurobipy import GRB, LinExpr, read
    os.chdir(os.path.dirname(__file__) or os.curdir)

    mod_in = "tsp_gurobi.mod"
    mod_out = "tmp/tsp_gurobi.out.mod"
    graph_size = "large"
    parser = PyMPL(locals_=locals(), globals_=globals())
    parser.parse(mod_in, mod_out)

    lp_out = "tmp/tsp_gurobi.lp"
    glpkutils.mod2lp(mod_out, lp_out, verbose=True)

    m = read(lp_out)
    m.params.LazyConstraints = 1
    m.params.MIPGap = 0
    m.params.MIPGapAbs = 1-1e-5

    def sep_callback(model, where):
        """Gurobi callback function."""
        if where == GRB.callback.MIPNODE:
            model._cnt += 1
            if model._cnt - model._lastrun < 10:
                return
            model._lastrun = model._cnt

            # check if the submodel was used
            assert "ATSP_MTZ" in parser.submodels()

            # calls the separate method to compute valid inequalities
            cuts = parser["ATSP_MTZ"].separate(
                lambda name: model.cbGetNodeRel(model.getVarByName(name))
            )

            # add the cuts to the model
            if len(cuts) > 0:
                print("add {0} {1}".format(
                    len(cuts), "cuts" if len(cuts) > 1 else "cut"
                ))
            for cut in cuts:
                lincomb, sign, rhs = cut
                expr = LinExpr([
                    (coef, model.getVarByName(var))
                    for var, coef in lincomb
                ])
                if sign[0] == ">":
                    model.cbLazy(expr >= rhs)
                elif sign[0] == "<":
                    model.cbLazy(expr <= rhs)
                else:
                    model.cbLazy(expr == rhs)

    m._cnt = 0
    m._lastrun = float("-inf")
    m.optimize(sep_callback)

    print("Objective:", m.ObjVal)


if __name__ == "__main__":
    main()
