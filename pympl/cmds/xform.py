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
from __future__ import division
from builtins import range

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
from .xformutils import XFormLSUSL
from .xformutils import XFormLSUSCSL
from .xformutils import XFormLSUSCBSL
from .xformutils import XFormLSUB
from .xformutils import XFormDLSICC
from .xformutils import XFormDLSICCB
from .xformutils import XFormDLSCCB
from .xformutils import XFormDLSCCSC
from .xformutils import XFormDLSCCSCU


class SubmodWWU(SubmodBase):
    """Command for creating WW-U-B extended formulations."""

    def __init__(self, *args, **kwargs):
        SubmodBase.__init__(self, *args, **kwargs)
        self._cnt = 0

    def _evalcmd(self, arg1, s, y, d, NT, Tk=None):
        """Evalutates CMD[arg1](*args)."""
        assert arg1 is None
        self._cnt += 1
        prefix = "_wwu_{0}_".format(self._cnt)

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(d, list) and len(d) == NT

        varl = s + y

        if len(s) == NT:
            s = {i+1: s[i] for i in range(NT)}
            s[0] = 0
        else:
            s = {i: s[i] for i in mrange(0, NT)}
        y = {i+1: y[i] for i in range(NT)}
        d = {i+1: d[i] for i in range(NT)}

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

    def __init__(self, *args, **kwargs):
        SubmodBase.__init__(self, *args, **kwargs)
        self._cnt = 0

    def _evalcmd(self, arg1, s, r, y, d, NT, Tk=None):
        """Evalutates CMD[arg1](*args)."""
        assert arg1 is None
        self._cnt += 1
        prefix = "_wwub_{0}_".format(self._cnt)

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(r, list) and len(r) == NT
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(d, list) and len(d) == NT

        varl = s + r + y

        if len(s) == NT:
            s = {i+1: s[i] for i in range(NT)}
            s[0] = 0
        else:
            s = {i: s[i] for i in mrange(0, NT)}
        r = {i+1: r[i] for i in range(NT)}
        y = {i+1: y[i] for i in range(NT)}
        d = {i+1: d[i] for i in range(NT)}

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

    def __init__(self, *args, **kwargs):
        SubmodBase.__init__(self, *args, **kwargs)
        self._cnt = 0

    def _evalcmd(self, arg1, s, y, z, d, NT, Tk=None):
        """Evalutates CMD[arg1](*args)."""
        assert arg1 is None
        self._cnt += 1
        prefix = "_wwusc_{0}_".format(self._cnt)

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(z, list) and len(z) == NT
        assert isinstance(d, list) and len(d) == NT

        varl = s + y + z

        if len(s) == NT:
            s = {i+1: s[i] for i in range(NT)}
            s[0] = 0
        else:
            s = {i: s[i] for i in mrange(0, NT)}
        y = {i+1: y[i] for i in range(NT)}
        z = {i+1: z[i] for i in range(NT)}
        d = {i+1: d[i] for i in range(NT)}

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

    def __init__(self, *args, **kwargs):
        SubmodBase.__init__(self, *args, **kwargs)
        self._cnt = 0

    def _evalcmd(self, arg1, s, r, y, z, w, d, NT, Tk=None):
        """Evalutates CMD[arg1](*args)."""
        assert arg1 is None
        self._cnt += 1
        prefix = "_wwuscb_{0}_".format(self._cnt)

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(r, list) and len(r) == NT
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(z, list) and len(z) == NT
        assert isinstance(w, list) and len(w) == NT
        assert isinstance(d, list) and len(d) == NT

        varl = s + r + y + z + w

        if len(s) == NT:
            s = {i+1: s[i] for i in range(NT)}
            s[0] = 0
        else:
            s = {i: s[i] for i in mrange(0, NT)}
        r = {i+1: r[i] for i in range(NT)}
        y = {i+1: y[i] for i in range(NT)}
        z = {i+1: z[i] for i in range(NT)}
        w = {i+1: w[i] for i in range(NT)}
        d = {i+1: d[i] for i in range(NT)}

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

    def __init__(self, *args, **kwargs):
        SubmodBase.__init__(self, *args, **kwargs)
        self._cnt = 0

    def _evalcmd(self, arg1, s, y, d, L, NT, Tk=None):
        """Evalutates CMD[arg1](*args)."""
        assert arg1 is None
        self._cnt += 1
        prefix = "_wwulb_{0}_".format(self._cnt)

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(d, list) and len(d) == NT

        varl = s + y

        if len(s) == NT:
            s = {i+1: s[i] for i in range(NT)}
            s[0] = 0
        else:
            s = {i: s[i] for i in mrange(0, NT)}
        y = {i+1: y[i] for i in range(NT)}
        d = {i+1: d[i] for i in range(NT)}

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

    def __init__(self, *args, **kwargs):
        SubmodBase.__init__(self, *args, **kwargs)
        self._cnt = 0

    def _evalcmd(self, arg1, s, y, d, C, NT, Tk=None):
        """Evalutates CMD[arg1](*args)."""
        assert arg1 is None
        self._cnt += 1
        prefix = "_wwcc_{0}_".format(self._cnt)

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(d, list) and len(d) == NT

        varl = s + y

        if len(s) == NT:
            s = {i+1: s[i] for i in range(NT)}
            s[0] = 0
        else:
            s = {i: s[i] for i in mrange(0, NT)}
        y = {i+1: y[i] for i in range(NT)}
        d = {i+1: d[i] for i in range(NT)}

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

    def __init__(self, *args, **kwargs):
        SubmodBase.__init__(self, *args, **kwargs)
        self._cnt = 0

    def _evalcmd(self, arg1, s, r, y, d, C, NT, Tk=None):
        """Evalutates CMD[arg1](*args)."""
        assert arg1 is None
        self._cnt += 1
        prefix = "_wwccb_{0}_".format(self._cnt)

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(r, list) and len(r) == NT
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(d, list) and len(d) == NT

        varl = s + r + y

        if len(s) == NT:
            s = {i+1: s[i] for i in range(NT)}
            s[0] = 0
        else:
            s = {i: s[i] for i in mrange(0, NT)}
        r = {i+1: r[i] for i in range(NT)}
        y = {i+1: y[i] for i in range(NT)}
        d = {i+1: d[i] for i in range(NT)}

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

    def __init__(self, *args, **kwargs):
        SubmodBase.__init__(self, *args, **kwargs)
        self._cnt = 0

    def _evalcmd(self, arg1, s, x, y, d, NT, Tk=None):
        """Evalutates CMD[arg1](*args)."""
        assert arg1 is None
        self._cnt += 1
        prefix = "_lsu1_{0}_".format(self._cnt)

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(x, list) and len(x) == NT
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(d, list) and len(d) == NT

        varl = s + x + y

        if len(s) == NT:
            s = {i+1: s[i] for i in range(NT)}
            s[0] = 0
        else:
            s = {i: s[i] for i in mrange(0, NT)}
        x = {i+1: x[i] for i in range(NT)}
        y = {i+1: y[i] for i in range(NT)}
        d = {i+1: d[i] for i in range(NT)}

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

    def __init__(self, *args, **kwargs):
        SubmodBase.__init__(self, *args, **kwargs)
        self._cnt = 0

    def _evalcmd(self, arg1, s, x, y, d, NT, Tk=None):
        """Evalutates CMD[arg1](*args)."""
        assert arg1 is None
        self._cnt += 1
        prefix = "_lsu2_{0}_".format(self._cnt)

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(x, list) and len(x) == NT
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(d, list) and len(d) == NT

        varl = s + x + y

        if len(s) == NT:
            s = {i+1: s[i] for i in range(NT)}
            s[0] = 0
        else:
            s = {i: s[i] for i in mrange(0, NT)}
        x = {i+1: x[i] for i in range(NT)}
        y = {i+1: y[i] for i in range(NT)}
        d = {i+1: d[i] for i in range(NT)}

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

    def __init__(self, *args, **kwargs):
        SubmodBase.__init__(self, *args, **kwargs)
        self._cnt = 0

    def _evalcmd(self, arg1, s, x, y, d, NT, Tk=None):
        """Evalutates CMD[arg1](*args)."""
        assert arg1 is None
        self._cnt += 1
        prefix = "_lsu_{0}_".format(self._cnt)

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(x, list) and len(x) == NT
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(d, list) and len(d) == NT

        varl = s + x + y

        if len(s) == NT:
            s = {i+1: s[i] for i in range(NT)}
            s[0] = 0
        else:
            s = {i: s[i] for i in mrange(0, NT)}
        x = {i+1: x[i] for i in range(NT)}
        y = {i+1: y[i] for i in range(NT)}
        d = {i+1: d[i] for i in range(NT)}

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

    def __init__(self, *args, **kwargs):
        SubmodBase.__init__(self, *args, **kwargs)
        self._cnt = 0

    def _evalcmd(self, arg1, s, r, x, y, d, NT, Tk=None):
        """Evalutates CMD[arg1](*args)."""
        assert arg1 is None
        self._cnt += 1
        prefix = "_lsub_{0}_".format(self._cnt)

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(r, list) and len(r) == NT
        assert isinstance(x, list) and len(x) == NT
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(d, list) and len(d) == NT

        varl = s + r + x + y

        if len(s) == NT:
            s = {i+1: s[i] for i in range(NT)}
            s[0] = 0
        else:
            s = {i: s[i] for i in mrange(0, NT)}
        r = {i+1: r[i] for i in range(NT)}
        x = {i+1: x[i] for i in range(NT)}
        y = {i+1: y[i] for i in range(NT)}
        d = {i+1: d[i] for i in range(NT)}

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

    def __init__(self, *args, **kwargs):
        SubmodBase.__init__(self, *args, **kwargs)
        self._cnt = 0

    def _evalcmd(self, arg1, s, x, y, z, d, NT, Tk=None):
        """Evalutates CMD[arg1](*args)."""
        assert arg1 is None
        self._cnt += 1
        prefix = "_lsusc_{0}_".format(self._cnt)

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(x, list) and len(x) == NT
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(z, list) and len(z) == NT
        assert isinstance(d, list) and len(d) == NT

        varl = s + x + y + z

        if len(s) == NT:
            s = {i+1: s[i] for i in range(NT)}
            s[0] = 0
        else:
            s = {i: s[i] for i in mrange(0, NT)}
        x = {i+1: x[i] for i in range(NT)}
        y = {i+1: y[i] for i in range(NT)}
        z = {i+1: z[i] for i in range(NT)}
        d = {i+1: d[i] for i in range(NT)}

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

    def __init__(self, *args, **kwargs):
        SubmodBase.__init__(self, *args, **kwargs)
        self._cnt = 0

    def _evalcmd(self, arg1, s, x, y, z, w, d, NT, Tk=None):
        """Evalutates CMD[arg1](*args)."""
        assert arg1 is None
        self._cnt += 1
        prefix = "_lsuscb_{0}_".format(self._cnt)

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(x, list) and len(x) == NT
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(z, list) and len(z) == NT
        assert isinstance(w, list) and len(w) == NT
        assert isinstance(d, list) and len(d) == NT

        varl = s + x + y + z + w

        if len(s) == NT:
            s = {i+1: s[i] for i in range(NT)}
            s[0] = 0
        else:
            s = {i: s[i] for i in mrange(0, NT)}
        x = {i+1: x[i] for i in range(NT)}
        y = {i+1: y[i] for i in range(NT)}
        z = {i+1: z[i] for i in range(NT)}
        w = {i+1: w[i] for i in range(NT)}
        d = {i+1: d[i] for i in range(NT)}

        if Tk is None:
            Tk = NT

        model = Model()
        for var in varl:
            model.add_var(name=var)
        XFormLSUSCB(model, s, x, y, z, w, d, NT, Tk, prefix)
        model.rename_cons(lambda name: prefix+name)

        declared_vars = set(varl)
        self._pyvars["_model"] += writemod.model2ampl(model, declared_vars)


class SubmodLSUSL(SubmodBase):
    """Command for creating LS-U-SL extended formulations."""

    def __init__(self, *args, **kwargs):
        SubmodBase.__init__(self, *args, **kwargs)
        self._cnt = 0

    def _evalcmd(self, arg1, s, x, y, v, d, u, NT, Tk=None):
        """Evalutates CMD[arg1](*args)."""
        assert arg1 is None
        self._cnt += 1
        prefix = "_lsusl_{0}_".format(self._cnt)

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(x, list) and len(x) == NT
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(v, list) and len(v) == NT
        assert isinstance(d, list) and len(d) == NT
        assert isinstance(u, list) and len(u) == NT

        varl = s + x + y + v

        if len(s) == NT:
            s = {i+1: s[i] for i in range(NT)}
            s[0] = 0
        else:
            s = {i: s[i] for i in mrange(0, NT)}
        x = {i+1: x[i] for i in range(NT)}
        y = {i+1: y[i] for i in range(NT)}
        v = {i+1: v[i] for i in range(NT)}
        d = {i+1: d[i] for i in range(NT)}
        u = {i+1: u[i] for i in range(NT)}

        if Tk is None:
            Tk = NT

        model = Model()
        for var in varl:
            model.add_var(name=var)
        XFormLSUSL(model, s, x, y, v, d, u, NT, Tk, prefix)
        model.rename_cons(lambda name: prefix+name)

        declared_vars = set(varl)
        self._pyvars["_model"] += writemod.model2ampl(model, declared_vars)


class SubmodLSUSCSL(SubmodBase):
    """Command for creating LS-U-SC,SL extended formulations."""

    def __init__(self, *args, **kwargs):
        SubmodBase.__init__(self, *args, **kwargs)
        self._cnt = 0

    def _evalcmd(self, arg1, s, x, y, z, v, d, u, NT, Tk=None):
        """Evalutates CMD[arg1](*args)."""
        assert arg1 is None
        self._cnt += 1
        prefix = "_lsuscsl_{0}_".format(self._cnt)

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(x, list) and len(x) == NT
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(z, list) and len(z) == NT
        assert isinstance(v, list) and len(v) == NT
        assert isinstance(d, list) and len(d) == NT
        assert isinstance(u, list) and len(u) == NT

        varl = s + x + y + z + v

        if len(s) == NT:
            s = {i+1: s[i] for i in range(NT)}
            s[0] = 0
        else:
            s = {i: s[i] for i in mrange(0, NT)}
        x = {i+1: x[i] for i in range(NT)}
        y = {i+1: y[i] for i in range(NT)}
        z = {i+1: z[i] for i in range(NT)}
        v = {i+1: v[i] for i in range(NT)}
        d = {i+1: d[i] for i in range(NT)}
        u = {i+1: u[i] for i in range(NT)}

        if Tk is None:
            Tk = NT

        model = Model()
        for var in varl:
            model.add_var(name=var)
        XFormLSUSCSL(model, s, x, y, z, v, d, u, NT, Tk, prefix)
        model.rename_cons(lambda name: prefix+name)

        declared_vars = set(varl)
        self._pyvars["_model"] += writemod.model2ampl(model, declared_vars)


class SubmodLSUSCBSL(SubmodBase):
    """Command for creating LS-U-SC,B,SL extended formulations."""

    def __init__(self, *args, **kwargs):
        SubmodBase.__init__(self, *args, **kwargs)
        self._cnt = 0

    def _evalcmd(self, arg1, s, r, x, y, z, w, v, d, u, NT, Tk=None):
        """Evalutates CMD[arg1](*args)."""
        assert arg1 is None
        self._cnt += 1
        prefix = "_lsuscbsl_{0}_".format(self._cnt)

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(r, list) and len(r) == NT
        assert isinstance(x, list) and len(x) == NT
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(z, list) and len(z) == NT
        assert isinstance(w, list) and len(w) == NT
        assert isinstance(v, list) and len(v) == NT
        assert isinstance(d, list) and len(d) == NT
        assert isinstance(u, list) and len(u) == NT

        varl = s + r + x + y + z + w + v

        if len(s) == NT:
            s = {i+1: s[i] for i in range(NT)}
            s[0] = 0
        else:
            s = {i: s[i] for i in mrange(0, NT)}
        r = {i+1: r[i] for i in range(NT)}
        x = {i+1: x[i] for i in range(NT)}
        y = {i+1: y[i] for i in range(NT)}
        z = {i+1: z[i] for i in range(NT)}
        w = {i+1: w[i] for i in range(NT)}
        v = {i+1: v[i] for i in range(NT)}
        d = {i+1: d[i] for i in range(NT)}
        u = {i+1: u[i] for i in range(NT)}

        if Tk is None:
            Tk = NT

        model = Model()
        for var in varl:
            model.add_var(name=var)
        XFormLSUSCBSL(model, s, r, x, y, z, w, v, d, u, NT, Tk, prefix)
        model.rename_cons(lambda name: prefix+name)

        declared_vars = set(varl)
        self._pyvars["_model"] += writemod.model2ampl(model, declared_vars)


class SubmodDLSICC(SubmodBase):
    """Command for creating DLSI-CC extended formulations."""

    def __init__(self, *args, **kwargs):
        SubmodBase.__init__(self, *args, **kwargs)
        self._cnt = 0

    def _evalcmd(self, arg1, s0, y, d, C, NT, Tk=None):
        """Evalutates CMD[arg1](*args)."""
        assert arg1 is None
        self._cnt += 1
        prefix = "_dlsicc_{0}_".format(self._cnt)

        assert isinstance(y, list) and len(y) == NT
        assert isinstance(d, list) and len(d) == NT

        varl = [s0] + y

        y = {i+1: y[i] for i in range(NT)}
        d = {i+1: d[i] for i in range(NT)}

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

    def __init__(self, *args, **kwargs):
        SubmodBase.__init__(self, *args, **kwargs)
        self._cnt = 0

    def _evalcmd(self, arg1, s0, r, y, d, C, NT, Tk=None):
        """Evalutates CMD[arg1](*args)."""
        assert arg1 is None
        self._cnt += 1
        prefix = "_dlsiccb_{0}_".format(self._cnt)

        assert isinstance(r, list) and len(r) == NT
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(d, list) and len(d) == NT

        varl = [s0] + r + y

        r = {i+1: r[i] for i in range(NT)}
        y = {i+1: y[i] for i in range(NT)}
        d = {i+1: d[i] for i in range(NT)}

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

    def __init__(self, *args, **kwargs):
        SubmodBase.__init__(self, *args, **kwargs)
        self._cnt = 0

    def _evalcmd(self, arg1, r, y, d, C, NT, Tk=None):
        """Evalutates CMD[arg1](*args)."""
        assert arg1 is None
        self._cnt += 1
        prefix = "_dlsccb_{0}_".format(self._cnt)

        assert isinstance(r, list) and len(r) == NT
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(d, list) and len(d) == NT

        varl = r + y

        r = {i+1: r[i] for i in range(NT)}
        y = {i+1: y[i] for i in range(NT)}
        d = {i+1: d[i] for i in range(NT)}

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

    def __init__(self, *args, **kwargs):
        SubmodBase.__init__(self, *args, **kwargs)
        self._cnt = 0

    def _evalcmd(self, arg1, s, y, z, d, C, NT, Tk=None):
        """Evalutates CMD[arg1](*args)."""
        assert arg1 is None
        self._cnt += 1
        prefix = "_dlsccsc_{0}_".format(self._cnt)

        assert isinstance(s, list) and len(s) == NT
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(z, list) and len(z) == NT
        assert isinstance(d, list) and len(d) == NT

        varl = s + y + z

        s = {i+1: s[i] for i in range(NT)}
        y = {i+1: y[i] for i in range(NT)}
        z = {i+1: z[i] for i in range(NT)}
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


class SubmodDLSCCSCU(SubmodBase):
    """Command for creating DLS-CC-SC-U extended formulations."""

    def __init__(self, *args, **kwargs):
        SubmodBase.__init__(self, *args, **kwargs)
        self._cnt = 0

    def _evalcmd(self, arg1, s, y, z, d, C, NT, Tk=None):
        """Evalutates CMD[arg1](*args)."""
        assert arg1 is None
        self._cnt += 1
        prefix = "_dlsccscu_{0}_".format(self._cnt)

        assert isinstance(s, list) and len(s) == NT
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(z, list) and len(z) == NT
        assert isinstance(d, list) and len(d) == NT

        varl = s + y + z

        s = {i+1: s[i] for i in range(NT)}
        y = {i+1: y[i] for i in range(NT)}
        z = {i+1: z[i] for i in range(NT)}
        d = {i+1: d[i] for i in range(NT)}

        if Tk is None:
            Tk = NT

        model = Model()
        for var in varl:
            model.add_var(name=var)

        XFormDLSCCSCU(model, s, y, z, d, NT, Tk, prefix)
        model.rename_cons(lambda name: prefix+name)

        declared_vars = set(varl)
        self._pyvars["_model"] += writemod.model2ampl(model, declared_vars)
