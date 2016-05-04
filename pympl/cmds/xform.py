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
from __future__ import division
from builtins import range
import six

from .base import SubmodBase
from ..model import Model, writemod
from .xformutils import mrange
from .xformutils import XFormWWU
from .xformutils import XFormWWUB
from .xformutils import XFormWWUSC
from .xformutils import XFormWWUSCB
from .xformutils import XFormWWULB
from .xformutils import XFormWWCC
from .xformutils import XFormWWCCB
from .xformutils import XFormLSU1
from .xformutils import XFormLSU2
from .xformutils import XFormLSU
from .xformutils import XFormLSUSC
from .xformutils import XFormLSUSCB
from .xformutils import XFormLSUB
from .xformutils import XFormDLSICC
from .xformutils import XFormDLSICCB
from .xformutils import XFormDLSCCB
from .xformutils import XFormDLSCCSC


def list2dict(lst, i0, NT, align="r", default=0):
    """Transform a list of variables/values into a i0..NT dictionary."""
    assert align in ("l", "r")
    missing = (NT-i0+1) - len(lst)
    if missing == 0:
        return {i0+i: lst[i] for i in range(len(lst))}
    else:
        if align == "r":
            d = {i0+missing+i: lst[i] for i in range(len(lst))}
            for i in range(missing):
                d[i0+i] = default
        else:
            d = {i0+i: lst[i] for i in range(len(lst))}
            for i in range(missing):
                d[i0+len(lst)+i] = default
        return d


def filter_strings(lst):
    """Extract the strings from a list."""
    return [x for x in lst if isinstance(x, six.string_types)]


class SubmodWWU(SubmodBase):
    """Command for creating WW-U-B extended formulations."""

    def _evalcmd(self, arg1, s, y, d, NT, Tk=None):
        """Evalutate CMD[arg1](*args)."""
        assert arg1 is None
        prefix = self._new_prefix()

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(d, list) and len(d) == NT
        varl = filter_strings(s + y)
        s = list2dict(s, 0, NT)
        y = list2dict(y, 1, NT)
        d = list2dict(d, 1, NT)
        if Tk is None:
            Tk = NT

        model = Model()
        for var in varl:
            model.add_var(name=var)
        XFormWWU(model, s, y, d, NT, Tk, prefix)
        model.rename_cons(lambda name: prefix+name)

        declared_vars = set(varl)
        self._pyvars["_model"] += writemod.model2ampl(model, declared_vars)


class SubmodWWUB(SubmodBase):
    """Command for creating WW-U-B extended formulations."""

    def _evalcmd(self, arg1, s, r, y, d, NT, Tk=None):
        """Evalutate CMD[arg1](*args)."""
        assert arg1 is None
        prefix = self._new_prefix()

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(r, list) and len(r) == NT
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(d, list) and len(d) == NT
        varl = filter_strings(s + r + y)
        s = list2dict(s, 0, NT)
        r = list2dict(r, 1, NT)
        y = list2dict(y, 1, NT)
        d = list2dict(d, 1, NT)
        if Tk is None:
            Tk = NT

        model = Model()
        for var in varl:
            model.add_var(name=var)
        XFormWWUB(model, s, r, y, d, NT, Tk, prefix)
        model.rename_cons(lambda name: prefix+name)

        declared_vars = set(varl)
        self._pyvars["_model"] += writemod.model2ampl(model, declared_vars)


class SubmodWWUSC(SubmodBase):
    """Command for creating WW-U-SC extended formulations."""

    def _evalcmd(self, arg1, s, y, z, d, NT, Tk=None):
        """Evalutate CMD[arg1](*args)."""
        assert arg1 is None
        prefix = self._new_prefix()

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(z, list) and len(z) == NT
        assert isinstance(d, list) and len(d) == NT
        varl = filter_strings(s + y + z)
        s = list2dict(s, 0, NT)
        y = list2dict(y, 1, NT)
        z = list2dict(z, 1, NT)
        d = list2dict(d, 1, NT)
        if Tk is None:
            Tk = NT

        model = Model()
        for var in varl:
            model.add_var(name=var)
        XFormWWUSC(model, s, y, z, d, NT, Tk, prefix)
        model.rename_cons(lambda name: prefix+name)

        declared_vars = set(varl)
        self._pyvars["_model"] += writemod.model2ampl(model, declared_vars)


class SubmodWWUSCB(SubmodBase):
    """Command for creating WW-U-SC,B extended formulations."""

    def _evalcmd(self, arg1, s, r, y, z, w, d, NT, Tk=None):
        """Evalutate CMD[arg1](*args)."""
        assert arg1 is None
        prefix = self._new_prefix()

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(r, list) and len(r) == NT
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(z, list) and len(z) == NT
        assert isinstance(w, list) and len(w) == NT
        assert isinstance(d, list) and len(d) == NT
        varl = filter_strings(s + r + y + z + w)
        s = list2dict(s, 0, NT)
        r = list2dict(r, 1, NT)
        y = list2dict(y, 1, NT)
        z = list2dict(z, 1, NT)
        w = list2dict(w, 1, NT)
        d = list2dict(d, 1, NT)
        if Tk is None:
            Tk = NT

        model = Model()
        for var in varl:
            model.add_var(name=var)
        XFormWWUSCB(model, s, r, y, z, w, d, NT, Tk, prefix)
        model.rename_cons(lambda name: prefix+name)

        declared_vars = set(varl)
        self._pyvars["_model"] += writemod.model2ampl(model, declared_vars)


class SubmodWWULB(SubmodBase):
    """Command for creating WW-CC-B extended formulations."""

    def _evalcmd(self, arg1, s, y, d, L, NT, Tk=None):
        """Evalutate CMD[arg1](*args)."""
        assert arg1 is None
        prefix = self._new_prefix()

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(d, list) and len(d) == NT
        varl = filter_strings(s + y)
        s = list2dict(s, 0, NT)
        y = list2dict(y, 1, NT)
        d = list2dict(d, 1, NT)
        if Tk is None:
            Tk = NT

        model = Model()
        for var in varl:
            model.add_var(name=var)
        XFormWWULB(model, s, y, d, L, NT, Tk, prefix)
        model.rename_cons(lambda name: prefix+name)

        declared_vars = set(varl)
        self._pyvars["_model"] += writemod.model2ampl(model, declared_vars)


class SubmodWWCC(SubmodBase):
    """Command for creating WW-CC extended formulations."""

    def _evalcmd(self, arg1, s, y, d, C, NT, Tk=None):
        """Evalutate CMD[arg1](*args)."""
        assert arg1 is None
        prefix = self._new_prefix()

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(d, list) and len(d) == NT
        varl = filter_strings(s + y)
        s = list2dict(s, 0, NT)
        y = list2dict(y, 1, NT)
        d = list2dict(d, 1, NT)
        if Tk is None:
            Tk = NT

        model = Model()
        for var in varl:
            model.add_var(name=var)
        XFormWWCC(model, s, y, d, C, NT, Tk, prefix)
        model.rename_cons(lambda name: prefix+name)

        declared_vars = set(varl)
        self._pyvars["_model"] += writemod.model2ampl(model, declared_vars)


class SubmodWWCCB(SubmodBase):
    """Command for creating WW-CC-B extended formulations."""

    def _evalcmd(self, arg1, s, r, y, d, C, NT, Tk=None):
        """Evalutate CMD[arg1](*args)."""
        assert arg1 is None
        prefix = self._new_prefix()

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(r, list) and len(r) == NT
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(d, list) and len(d) == NT
        varl = filter_strings(s + r + y)
        s = list2dict(s, 0, NT)
        r = list2dict(r, 1, NT)
        y = list2dict(y, 1, NT)
        d = list2dict(d, 1, NT)
        if Tk is None:
            Tk = NT

        model = Model()
        for var in varl:
            model.add_var(name=var)
        XFormWWCCB(model, s, r, y, d, C, NT, Tk, prefix)
        model.rename_cons(lambda name: prefix+name)

        declared_vars = set(varl)
        self._pyvars["_model"] += writemod.model2ampl(model, declared_vars)


class SubmodLSU1(SubmodBase):
    """Command for creating LS-U1 extended formulations."""

    def _evalcmd(self, arg1, s, x, y, d, NT, Tk=None):
        """Evalutate CMD[arg1](*args)."""
        assert arg1 is None
        prefix = self._new_prefix()

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(x, list) and len(x) == NT
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(d, list) and len(d) == NT
        varl = filter_strings(s + x + y)
        s = list2dict(s, 0, NT)
        x = list2dict(x, 1, NT)
        y = list2dict(y, 1, NT)
        d = list2dict(d, 1, NT)
        if Tk is None:
            Tk = NT

        model = Model()
        for var in varl:
            model.add_var(name=var)
        XFormLSU1(model, s, x, y, d, NT, Tk, prefix)
        model.rename_cons(lambda name: prefix+name)

        declared_vars = set(varl)
        self._pyvars["_model"] += writemod.model2ampl(model, declared_vars)


class SubmodLSU2(SubmodBase):
    """Command for creating LS-U1 extended formulations."""

    def _evalcmd(self, arg1, s, x, y, d, NT, Tk=None):
        """Evalutate CMD[arg1](*args)."""
        assert arg1 is None
        prefix = self._new_prefix()

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(x, list) and len(x) == NT
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(d, list) and len(d) == NT
        varl = filter_strings(s + x + y)
        s = list2dict(s, 0, NT)
        x = list2dict(x, 1, NT)
        y = list2dict(y, 1, NT)
        d = list2dict(d, 1, NT)
        if Tk is None:
            Tk = NT

        model = Model()
        for var in varl:
            model.add_var(name=var)
        XFormLSU2(model, s, x, y, d, NT, Tk, prefix)
        model.rename_cons(lambda name: prefix+name)

        declared_vars = set(varl)
        self._pyvars["_model"] += writemod.model2ampl(model, declared_vars)


class SubmodLSU(SubmodBase):
    """Command for creating LS-U extended formulations."""

    def _evalcmd(self, arg1, s, x, y, d, NT, Tk=None):
        """Evalutate CMD[arg1](*args)."""
        assert arg1 is None
        prefix = self._new_prefix()

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(x, list) and len(x) == NT
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(d, list) and len(d) == NT
        varl = filter_strings(s + x + y)
        s = list2dict(s, 0, NT)
        x = list2dict(x, 1, NT)
        y = list2dict(y, 1, NT)
        d = list2dict(d, 1, NT)
        if Tk is None:
            Tk = NT

        model = Model()
        for var in varl:
            model.add_var(name=var)
        XFormLSU(model, s, x, y, d, NT, Tk, prefix)
        model.rename_cons(lambda name: prefix+name)

        declared_vars = set(varl)
        self._pyvars["_model"] += writemod.model2ampl(model, declared_vars)


class SubmodLSUB(SubmodBase):
    """Command for creating LS-U-B extended formulations."""

    def _evalcmd(self, arg1, s, r, x, y, d, NT, Tk=None):
        """Evalutate CMD[arg1](*args)."""
        assert arg1 is None
        prefix = self._new_prefix()

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(r, list) and len(r) == NT
        assert isinstance(x, list) and len(x) == NT
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(d, list) and len(d) == NT
        varl = filter_strings(s + r + x + y)
        s = list2dict(s, 0, NT)
        r = list2dict(r, 1, NT)
        x = list2dict(x, 1, NT)
        y = list2dict(y, 1, NT)
        d = list2dict(d, 1, NT)
        if Tk is None:
            Tk = NT

        model = Model()
        for var in varl:
            model.add_var(name=var)
        XFormLSUB(model, s, r, x, y, d, NT, Tk, prefix)
        model.rename_cons(lambda name: prefix+name)

        declared_vars = set(varl)
        self._pyvars["_model"] += writemod.model2ampl(model, declared_vars)


class SubmodLSUSC(SubmodBase):
    """Command for creating LS-U-SC extended formulations."""

    def _evalcmd(self, arg1, s, x, y, z, d, NT, Tk=None):
        """Evalutate CMD[arg1](*args)."""
        assert arg1 is None
        prefix = self._new_prefix()

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(x, list) and len(x) == NT
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(z, list) and len(z) == NT
        assert isinstance(d, list) and len(d) == NT
        varl = filter_strings(s + x + y + z)
        s = list2dict(s, 0, NT)
        x = list2dict(x, 1, NT)
        y = list2dict(y, 1, NT)
        z = list2dict(z, 1, NT)
        d = list2dict(d, 1, NT)
        if Tk is None:
            Tk = NT

        model = Model()
        for var in varl:
            model.add_var(name=var)
        XFormLSUSC(model, s, x, y, z, d, NT, Tk, prefix)
        model.rename_cons(lambda name: prefix+name)

        declared_vars = set(varl)
        self._pyvars["_model"] += writemod.model2ampl(model, declared_vars)


class SubmodLSUSCB(SubmodBase):
    """Command for creating LS-U-SC,B extended formulations."""

    def _evalcmd(self, arg1, s, x, y, z, w, d, NT, Tk=None):
        """Evalutate CMD[arg1](*args)."""
        assert arg1 is None
        prefix = self._new_prefix()

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(x, list) and len(x) == NT
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(z, list) and len(z) == NT
        assert isinstance(w, list) and len(w) == NT
        assert isinstance(d, list) and len(d) == NT
        varl = filter_strings(s + x + y + z + w)
        s = list2dict(s, 0, NT)
        x = list2dict(x, 1, NT)
        y = list2dict(y, 1, NT)
        z = list2dict(z, 1, NT)
        w = list2dict(w, 1, NT)
        d = list2dict(d, 1, NT)
        if Tk is None:
            Tk = NT

        model = Model()
        for var in varl:
            model.add_var(name=var)
        XFormLSUSCB(model, s, x, y, z, w, d, NT, Tk, prefix)
        model.rename_cons(lambda name: prefix+name)

        declared_vars = set(varl)
        self._pyvars["_model"] += writemod.model2ampl(model, declared_vars)


class SubmodDLSICC(SubmodBase):
    """Command for creating DLSI-CC extended formulations."""

    def _evalcmd(self, arg1, s0, y, d, C, NT, Tk=None):
        """Evalutate CMD[arg1](*args)."""
        assert arg1 is None
        prefix = self._new_prefix()

        assert isinstance(y, list) and len(y) == NT
        assert isinstance(d, list) and len(d) == NT
        varl = filter_strings([s0] + y)
        y = list2dict(y, 1, NT)
        d = list2dict(d, 1, NT)
        if Tk is None:
            Tk = NT

        model = Model()
        for var in varl:
            model.add_var(name=var)

        XFormDLSICC(model, s0, y, d, C, NT, Tk, prefix)
        model.rename_cons(lambda name: prefix+name)

        declared_vars = set(varl)
        self._pyvars["_model"] += writemod.model2ampl(model, declared_vars)


class SubmodDLSICCB(SubmodBase):
    """Command for creating DLSI-CC-B extended formulations."""

    def _evalcmd(self, arg1, s0, r, y, d, C, NT, Tk=None):
        """Evalutate CMD[arg1](*args)."""
        assert arg1 is None
        prefix = self._new_prefix()

        assert isinstance(r, list) and len(r) == NT
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(d, list) and len(d) == NT
        varl = filter_strings([s0] + r + y)
        r = list2dict(r, 1, NT)
        y = list2dict(y, 1, NT)
        d = list2dict(d, 1, NT)
        if Tk is None:
            Tk = NT

        model = Model()
        for var in varl:
            model.add_var(name=var)

        XFormDLSICCB(model, s0, r, y, d, C, NT, Tk, prefix)
        model.rename_cons(lambda name: prefix+name)

        declared_vars = set(varl)
        self._pyvars["_model"] += writemod.model2ampl(model, declared_vars)


class SubmodDLSCCB(SubmodBase):
    """Command for creating DLS-CC-B extended formulations."""

    def _evalcmd(self, arg1, r, y, d, C, NT, Tk=None):
        """Evalutate CMD[arg1](*args)."""
        assert arg1 is None
        prefix = self._new_prefix()

        assert isinstance(r, list) and len(r) == NT
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(d, list) and len(d) == NT
        varl = filter_strings(r + y)
        r = list2dict(r, 1, NT)
        y = list2dict(y, 1, NT)
        d = list2dict(d, 1, NT)
        if Tk is None:
            Tk = NT

        model = Model()
        for var in varl:
            model.add_var(name=var)

        XFormDLSCCB(model, r, y, d, C, NT, Tk, prefix)
        model.rename_cons(lambda name: prefix+name)

        declared_vars = set(varl)
        self._pyvars["_model"] += writemod.model2ampl(model, declared_vars)


class SubmodDLSCCSC(SubmodBase):
    """Command for creating DLS-CC-SC extended formulations."""

    def _evalcmd(self, arg1, s, y, z, d, C, NT, Tk=None):
        """Evalutate CMD[arg1](*args)."""
        assert arg1 is None
        prefix = self._new_prefix()

        assert isinstance(s, list) and len(s) == NT
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(z, list) and len(z) == NT
        assert isinstance(d, list) and len(d) == NT
        varl = filter_strings(s + y + z)
        s = list2dict(s, 1, NT)
        y = list2dict(y, 1, NT)
        z = list2dict(z, 1, NT)
        d = {i+1: d[i]/C for i in range(NT)}
        if Tk is None:
            Tk = NT

        model = Model()
        for var in varl:
            model.add_var(name=var)

        XFormDLSCCSC(model, s, y, z, d, NT, Tk, prefix)
        model.rename_cons(lambda name: prefix+name)

        declared_vars = set(varl)
        self._pyvars["_model"] += writemod.model2ampl(model, declared_vars)
