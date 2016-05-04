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
from builtins import str

from .base import CmdBase
from .. import utils


class CmdSet(CmdBase):
    """Command for creating a new AMPL set."""

    def _evalcmd(self, name, values):
        """Evalutate CMD[name](*args)."""
        match = utils.parse_symbname(name)
        assert match is not None
        name = match

        self._pyvars["_defs"] += utils.ampl_set(
            name, values, self._sets, self._params
        )[0]


class CmdParam(CmdBase):
    """Command for creating a new AMPL parameter."""

    def _evalcmd(self, arg1, values, i0=None):
        """Evalutate CMD[arg1](*args)."""
        match = utils.parse_indexed(arg1, "{}")
        assert match is not None
        name, index_list = match

        if isinstance(values, list):
            if i0 is None:
                i0 = 0
            values = utils.list2dict(values, i0)
            if index_list is not None:
                assert len(index_list) == 1
        elif isinstance(values, dict):
            assert i0 is None
        else:
            assert i0 is None
            assert index_list is None

        if isinstance(values, dict):
            if index_list is None:
                index_list = ["{0}_I".format(name)]
            if len(index_list) == 1:
                index = index_list[0]
                self._pyvars["_defs"] += utils.ampl_set(
                    index, list(values.keys()), self._sets, self._params
                )[0]
            else:
                for i, index in enumerate(index_list):
                    keys = [k[i] for k in values.keys()]
                    self._pyvars["_defs"] += utils.ampl_set(
                        index, keys, self._sets, self._params
                    )[0]

        if index_list is None:
            index = None
        else:
            index = ",".join([index.replace("^", "") for index in index_list])
        pdefs, pdata = utils.ampl_param(
            name, index, values, self._sets, self._params
        )
        self._pyvars["_defs"] += pdefs
        self._pyvars["_data"] += pdata


class CmdVar(CmdBase):
    """Command for creating a new AMPL variable."""

    def _evalcmd(self, name, typ="", lb=None, ub=None, index_set=None):
        """Evalutate CMD[name](*args)."""
        match = utils.parse_indexed(name, "{}")
        assert match is not None
        name, index = match

        if index is not None:
            assert len(index) == 1
            index = index[0]
            if not index.startswith("^"):
                assert index_set is not None

        if index_set is not None:
            if index is None:
                index = "{0}_I".format(name)
            self._pyvars["_defs"] += utils.ampl_set(
                index, index_set, self._sets, self._params
            )[0]

        self._pyvars["_model"] += utils.ampl_var(name, index, typ, lb, ub)


class CmdCon(CmdBase):
    """Command for creating a new AMPL constraint."""

    def _evalcmd(self, name, left, sign, right):
        """Evalutate CMD[name](*args)."""
        match = utils.parse_symbname(name)
        assert match is not None
        name = match
        lincomb, sign, rhs = utils.linear_constraint(left, sign, right)
        self._pyvars["_model"] += utils.ampl_con(name, lincomb, sign, rhs)


class CmdStmt(CmdBase):
    """Command for creating new AMPL statements."""

    def _evalcmd(self, arg1, statement):
        """Evalutate CMD(*args)."""
        assert arg1 is None
        self._pyvars["_model"] += str(statement)
