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

slow = pytest.mark.skipif(
    not pytest.config.getoption("--runslow"),
    reason="need --runslow option to run"
)


def test_ppbymip_bike():
    """Test ppbymip_bike."""
    import ppbymip_bike as bike
    print("ppbymip_bike:")
    bike.main()


@slow
def test_ppbymip_cgp():
    """Test ppbymip_cgp."""
    import ppbymip_cgp as cgp
    print("ppbymip_cgp:")
    cgp.main()


@slow
def test_ppybymip_clb():
    """Test ppbymip_clb."""
    import ppbymip_clb as clb
    print("ppbymip_clb:")
    clb.main()

@slow
def test_mp():
    """Test ppbymip_mp."""
    import ppbymip_mp as mp
    mp.main()


@slow
def test_ps():
    """Test ppbymip_ps."""
    import ppbymip_ps as ps
    print("ppbymip_ps:")
    ps.main()


if __name__ == "__main__":
    test_ppbymip_bike()
    test_ppbymip_cgp()
    test_ppbymip_clb()
    test_ppbymip_mp()
    test_ppbymip_ps()
