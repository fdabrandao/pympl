"""
This code is part of the Mathematical Modelling Toolbox PyMPL.

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

from .base import SubmodBase
from ..model import Model, writemod
from .xformutils import ww_u
from .xformutils import ww_u_b
from .xformutils import ww_u_sc
from .xformutils import ww_u_sc_b
from .xformutils import ww_u_lb
from .xformutils import ww_cc
from .xformutils import ww_cc_b_aux
from .xformutils import ww_cc_b


class SubmodWW_U(SubmodBase):
    """Command for creating WW-U-B extended formulations."""

    def __init__(self, *args, **kwargs):
        SubmodBase.__init__(self, *args, **kwargs)
        self._cnt = 0

    def _evalcmd(self, arg1, s, y, d, NT, Tk=None):
        """Evalutates CMD[arg1](*args)."""
        assert arg1 is None
        self._cnt += 1
        prefix = "_wwu{0}_".format(self._cnt)

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(d, list) and len(d) == NT

        varl = s + y

        if len(s) == NT:
            s = {i+1: s[i] for i in xrange(NT)}
            s[0] = 0
        else:
            s = {i: s[i] for i in mrange(0, NT)}
        y = {i+1: y[i] for i in xrange(NT)}
        d = {i+1: d[i] for i in xrange(NT)}

        if Tk is None:
            Tk = NT

        model = Model()
        for var in varl:
            model.add_var(name=var)
        ww_u(model, s, y, d, NT, Tk, prefix)
        model.rename_cons(lambda name: prefix+name)

        declared_vars = set(varl)
        self._pyvars["_model"] += writemod.model2ampl(model, declared_vars)


class SubmodWW_U_B(SubmodBase):
    """Command for creating WW-U-B extended formulations."""

    def __init__(self, *args, **kwargs):
        SubmodBase.__init__(self, *args, **kwargs)
        self._cnt = 0

    def _evalcmd(self, arg1, s, r, y, d, NT, Tk=None):
        """Evalutates CMD[arg1](*args)."""
        assert arg1 is None
        self._cnt += 1
        prefix = "_wwub{0}_".format(self._cnt)

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(r, list) and len(r) == NT
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(d, list) and len(d) == NT

        varl = s + r + y

        if len(s) == NT:
            s = {i+1: s[i] for i in xrange(NT)}
            s[0] = 0
        else:
            s = {i: s[i] for i in mrange(0, NT)}
        r = {i+1: r[i] for i in xrange(NT)}
        y = {i+1: y[i] for i in xrange(NT)}
        d = {i+1: d[i] for i in xrange(NT)}

        if Tk is None:
            Tk = NT

        model = Model()
        for var in varl:
            model.add_var(name=var)
        ww_u_b(model, s, r, y, d, NT, Tk, prefix)
        model.rename_cons(lambda name: prefix+name)

        declared_vars = set(varl)
        self._pyvars["_model"] += writemod.model2ampl(model, declared_vars)


class SubmodWW_U_SC(SubmodBase):
    """Command for creating WW-U-SC extended formulations."""

    def __init__(self, *args, **kwargs):
        SubmodBase.__init__(self, *args, **kwargs)
        self._cnt = 0

    def _evalcmd(self, arg1, s, y, z, d, NT, Tk=None):
        """Evalutates CMD[arg1](*args)."""
        assert arg1 is None
        self._cnt += 1
        prefix = "_wwusc{0}_".format(self._cnt)

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(z, list) and len(z) == NT
        assert isinstance(d, list) and len(d) == NT

        varl = s + y + z

        if len(s) == NT:
            s = {i+1: s[i] for i in xrange(NT)}
            s[0] = 0
        else:
            s = {i: s[i] for i in mrange(0, NT)}
        y = {i+1: y[i] for i in xrange(NT)}
        z = {i+1: z[i] for i in xrange(NT)}
        d = {i+1: d[i] for i in xrange(NT)}

        if Tk is None:
            Tk = NT

        model = Model()
        for var in varl:
            model.add_var(name=var)
        ww_u_sc(model, s, y, z, d, NT, Tk, prefix)
        model.rename_cons(lambda name: prefix+name)

        declared_vars = set(varl)
        self._pyvars["_model"] += writemod.model2ampl(model, declared_vars)


class SubmodWW_U_SCB(SubmodBase):
    """Command for creating WW-U-SC,B extended formulations."""

    def __init__(self, *args, **kwargs):
        SubmodBase.__init__(self, *args, **kwargs)
        self._cnt = 0

    def _evalcmd(self, arg1, s, r, y, z, w, d, NT, Tk=None):
        """Evalutates CMD[arg1](*args)."""
        assert arg1 is None
        self._cnt += 1
        prefix = "_wwuscb{0}_".format(self._cnt)

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(r, list) and len(r) == NT
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(z, list) and len(z) == NT
        assert isinstance(w, list) and len(w) == NT
        assert isinstance(d, list) and len(d) == NT

        varl = s + r + y + z + w

        if len(s) == NT:
            s = {i+1: s[i] for i in xrange(NT)}
            s[0] = 0
        else:
            s = {i: s[i] for i in mrange(0, NT)}
        r = {i+1: r[i] for i in xrange(NT)}
        y = {i+1: y[i] for i in xrange(NT)}
        z = {i+1: z[i] for i in xrange(NT)}
        w = {i+1: w[i] for i in xrange(NT)}
        d = {i+1: d[i] for i in xrange(NT)}

        if Tk is None:
            Tk = NT

        model = Model()
        for var in varl:
            model.add_var(name=var)
        ww_u_sc_b(model, s, r, y, z, w, d, NT, Tk, prefix)
        model.rename_cons(lambda name: prefix+name)

        declared_vars = set(varl)
        self._pyvars["_model"] += writemod.model2ampl(model, declared_vars)


class SubmodWW_U_LB(SubmodBase):
    """Command for creating WW-CC-B extended formulations."""

    def __init__(self, *args, **kwargs):
        SubmodBase.__init__(self, *args, **kwargs)
        self._cnt = 0

    def _evalcmd(self, arg1, s, y, d, L, NT, Tk=None):
        """Evalutates CMD[arg1](*args)."""
        assert arg1 is None
        self._cnt += 1
        prefix = "_wwulb{0}_".format(self._cnt)

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(d, list) and len(d) == NT

        varl = s + y

        if len(s) == NT:
            s = {i+1: s[i] for i in xrange(NT)}
            s[0] = 0
        else:
            s = {i: s[i] for i in mrange(0, NT)}
        y = {i+1: y[i] for i in xrange(NT)}
        d = {i+1: d[i] for i in xrange(NT)}

        if Tk is None:
            Tk = NT

        model = Model()
        for var in varl:
            model.add_var(name=var)
        ww_u_lb(model, s, y, d, L, NT, Tk, prefix)
        model.rename_cons(lambda name: prefix+name)

        declared_vars = set(varl)
        self._pyvars["_model"] += writemod.model2ampl(model, declared_vars)


class SubmodWW_CC(SubmodBase):
    """Command for creating WW-CC extended formulations."""

    def __init__(self, *args, **kwargs):
        SubmodBase.__init__(self, *args, **kwargs)
        self._cnt = 0

    def _evalcmd(self, arg1, s, y, d, C, NT, Tk=None):
        """Evalutates CMD[arg1](*args)."""
        assert arg1 is None
        self._cnt += 1
        prefix = "_wwcc{0}_".format(self._cnt)

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(d, list) and len(d) == NT

        varl = s + y

        if len(s) == NT:
            s = {i+1: s[i] for i in xrange(NT)}
            s[0] = 0
        else:
            s = {i: s[i] for i in mrange(0, NT)}
        y = {i+1: y[i] for i in xrange(NT)}
        d = {i+1: d[i] for i in xrange(NT)}

        if Tk is None:
            Tk = NT

        model = Model()
        for var in varl:
            model.add_var(name=var)
        ww_cc(model, s, y, d, C, NT, Tk, prefix)
        model.rename_cons(lambda name: prefix+name)

        declared_vars = set(varl)
        self._pyvars["_model"] += writemod.model2ampl(model, declared_vars)


class SubmodWW_CC_B(SubmodBase):
    """Command for creating WW-CC-B extended formulations."""

    def __init__(self, *args, **kwargs):
        SubmodBase.__init__(self, *args, **kwargs)
        self._cnt = 0

    def _evalcmd(self, arg1, s, r, y, d, C, NT, Tk=None):
        """Evalutates CMD[arg1](*args)."""
        assert arg1 is None
        self._cnt += 1
        prefix = "_wwccb{0}_".format(self._cnt)

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(r, list) and len(r) == NT
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(d, list) and len(d) == NT

        varl = s + r + y

        if len(s) == NT:
            s = {i+1: s[i] for i in xrange(NT)}
            s[0] = 0
        else:
            s = {i: s[i] for i in mrange(0, NT)}
        r = {i+1: r[i] for i in xrange(NT)}
        y = {i+1: y[i] for i in xrange(NT)}
        d = {i+1: d[i] for i in xrange(NT)}

        if Tk is None:
            Tk = NT

        model = Model()
        for var in varl:
            model.add_var(name=var)
        ww_cc_b(model, s, r, y, d, C, NT, Tk, prefix)
        model.rename_cons(lambda name: prefix+name)

        declared_vars = set(varl)
        self._pyvars["_model"] += writemod.model2ampl(model, declared_vars)
