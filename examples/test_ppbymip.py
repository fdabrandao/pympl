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

import os
import sys
import ppbymip_bike as bike
import ppbymip_cgp as cgp
import ppbymip_clb as clb
import ppbymip_mp as mp
import ppbymip_ps as ps

if __name__ == "__main__":
    sdir = os.path.dirname(__file__)
    if sdir != "":
        os.chdir(sdir)


def main():
    """Runs all PyMPL examples."""

    print("bike:")
    bike.main()

    if "quick_test" not in sys.argv:
        print("cgp:")
        cgp.main()

    if "quick_test" not in sys.argv:
        print("clb:")
        clb.main()

    if "quick_test" not in sys.argv:
        print("clb:")
        clb.main()

    if "quick_test" not in sys.argv:
        print("mp:")
        mp.main()

    if "quick_test" not in sys.argv:
        print("ps:")
        ps.main()

if __name__ == "__main__":
    main()
