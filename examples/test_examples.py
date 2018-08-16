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
import pytest
try:
    runslow = pytest.config.getoption("--runslow")
except:
    runslow = False
slow = pytest.mark.skipif(not runslow, reason="need --runslow option to run")


def test_equivknapsack():
    """Test equivknapsack."""
    import equivknapsack
    try:
        print("equivknapsack:")
        equivknapsack.main()
    except ImportError as e:
        print(repr(e))


def test_equivknapsack01():
    """Test equivknapsack01."""
    import equivknapsack01
    try:
        print("equivknapsack01:")
        equivknapsack01.main()
    except ImportError as e:
        print(repr(e))


def test_wolsey():
    """Test wolsey."""
    import wolsey
    try:
        print("wolsey:")
        wolsey.main()
    except ImportError as e:
        print(repr(e))


def test_vpsolver_vbp():
    """Test vpsolver_vbp."""
    import vpsolver_vbp
    try:
        print("vpsolver_vbp:")
        vpsolver_vbp.main()
    except ImportError as e:
        print(repr(e))


def test_vpsolver_mvp():
    """Test vpsolver_mvp."""
    import vpsolver_mvp
    try:
        print("vpsolver_mvp:")
        vpsolver_mvp.main()
    except ImportError as e:
        print(repr(e))


def test_twostage():
    """Test twostage."""
    import twostage
    try:
        print("twostage:")
        twostage.main()
    except ImportError as e:
        print(repr(e))


def test_sos1():
    """Test sos1."""
    import sos1
    print("sos1:")
    sos1.main()


def test_sos2():
    """Test sos2."""
    import sos2
    print("sos2:")
    sos2.main()


def test_pwl():
    """Test pwl."""
    import pwl
    print("pwl:")
    pwl.main()


def test_tsp():
    """Test tsp."""
    import tsp
    tsp.main()


@slow
def test_tsp_gurobi():
    """Test tsp_gurobi."""
    import tsp_gurobi
    try:
        tsp_gurobi.main()
    except ImportError as e:
        print(repr(e))


if __name__ == "__main__":
    test_wolsey()
    test_equivknapsack01()
    test_equivknapsack()
    test_vpsolver_vbp()
    test_vpsolver_mvp()
    test_twostage()
    test_tsp_gurobi()
    test_tsp()
    test_sos()
    test_pwl()
