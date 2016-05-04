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
from builtins import object


class CmdBase(object):
    """Base class for PyMPL commands."""

    def __init__(self, cmd_name, prefix, pyvars, sets, params):
        self.cmd_name = cmd_name
        self._prefix = prefix
        self._count = 0
        self._pyvars = pyvars
        self._sets = sets
        self._params = params

    def _new_prefix(self):
        self._count += 1
        return "{}_{}_".format(self._prefix, self._count)

    def __call__(self, *args, **kwargs):
        """Evalutate CMD()."""
        self._evalcmd(None, *args, **kwargs)

    def __getitem__(self, arg1):
        """Evalutate CMD[arg1]."""
        return lambda *args, **kwargs: self._evalcmd(arg1, *args, **kwargs)

    def _evalcmd(self, arg1, *args, **kwargs):
        """Evalutate CMD[arg1](*args)."""
        raise NotImplementedError("CMD[arg1](*args)")


class SubmodBase(CmdBase):
    """Base class for PyMPL submodels."""

    def separate(self, get_var_value, *args, **kwargs):
        """Compute valid inequalities for the submodel."""
        pass

    def extract(self, get_var_value, *args, **kwargs):
        """Extract the solution of the submodel."""
        pass
