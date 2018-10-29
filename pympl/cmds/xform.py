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


def linkvars(prefix, newvar, varlist, begin):
    """Generate variable declarations for link variables."""
    import re
    p = re.compile('\s*([a-zA-Z0-9_]+)\s*\[([0-9]+)\]\s*$')
    specials = {}
    name = None
    end = begin+len(varlist)-1
    for i, var in zip(range(begin, end+1), varlist):
        m = p.match(str(var))
        if m is not None:
            g = m.groups()
            if int(g[1]) == i:
                if name is None:
                    name = g[0]
                continue
        specials[i] = var
    var_dcl = 'var ${newvar}{{$i in {begin}..{end}}} = '.format(
        newvar=newvar, begin=begin, end=end
    )
    for i in range(begin, end+1):
        if i in specials:
            var_dcl += 'if $i=={i} then {s} else '.format(i=i, s=specials[i])
    if name is not None:
        var_dcl += '{name}[$i];'.format(name=name)
    else:
        var_dcl += '0;'
    return prefix+newvar, var_dcl.replace('$', prefix)


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


class SubmodWWU_AMPL(SubmodBase):
    """Command for creating WW-U extended formulations in AMPL."""

    def _evalcmd(self, arg1, s, y, d, NT, Tk=None, prefix=None):
        """Evalutate CMD[arg1](*args)."""
        assert arg1 is None
        if prefix is None:
            prefix = self._new_prefix()

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(d, list) and len(d) == NT
        d = list2dict(d, 1, NT)
        if Tk is None:
            Tk = NT

        model = '#BEGIN WW-U\n'
        sname, dcl = linkvars(prefix, 's', s, 0)
        model += dcl + '\n'
        yname, dcl = linkvars(prefix, 'y', y, 1)
        model += dcl + '\n'

        """
        Basic Wagner-Whitin

        procedure XFormWWU(
            s : array (range) of linctr,
            y : array (range) of linctr,
            d : array (range) of real,
            NT : integer,
            Tk : integer,
            MC: integer)

            declarations
                XWW: array (1..NT,range) of linctr
                D : array (range,range) of real
            end-declarations

            CumulDemand(d,D,NT)
            forall (k in 1..NT,l in k..minlist(NT,k+Tk-1)| D(l,l)>0)
              XWW(k,l):=s(k-1) >= D(k,l) - sum (i in k..l) D(i,l)*y(i)
            if MC = 1 then
            forall (k in 1..NT,l in k..minlist(NT,k+Tk-1)| D(l,l)>0)
              setmodcut(XWW(k,l))
            end-if
        end-procedure
        """
        from .xformutils import NetDemand, CumulDemand
        s[0], d = NetDemand(s[0], d, NT)

        # CumulDemand(d,D,NT)
        D = {}
        CumulDemand(d, D, NT)

        D_values = ''.join(
            '[{},{}]{}'.format(i, j, D[i,j])
            for i in range(1, NT+1) for j in range(1, NT+1)
        )

        model += """
        param {p}D{{1..{NT}, 1..{NT}}};
        data; param {p}D := {D_values}; model;
        s.t. {p}wwu{{k in 1..{NT}, l in k..min({NT},k+{Tk}-1) : {p}D[l,l] > 0}}:
            {p}s[k-1] >= {p}D[k,l] - sum{{i in k..l}} {p}D[i,l] * {p}y[i];
        """.format(
            p=prefix, NT=NT, Tk=Tk,
            D_values=D_values
        ).replace('\n        ', '\n')
        model += '#END WW-U\n'
        self._pyvars["_model"] += model


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


class SubmodWWUB_AMPL(SubmodBase):
    """Command for creating WW-U-B extended formulations in AMPL."""

    def _evalcmd(self, arg1, s, r, y, d, NT, Tk=None, prefix=None):
        """Evalutate CMD[arg1](*args)."""
        assert arg1 is None
        if prefix is None:
            prefix = self._new_prefix()

        assert isinstance(s, list) and len(s) in (NT, NT+1)
        assert isinstance(r, list) and len(r) == NT
        assert isinstance(y, list) and len(y) == NT
        assert isinstance(d, list) and len(d) == NT
        d = list2dict(d, 1, NT)
        if Tk is None:
            Tk = NT

        model = '#BEGIN WW-U-B\n'
        sname, dcl = linkvars(prefix, 's', s, 0)
        model += dcl + '\n'
        rname, dcl = linkvars(prefix, 'r', r, 1)
        model += dcl + '\n'
        yname, dcl = linkvars(prefix, 'y', y, 1)
        model += dcl + '\n'

        """
        Wagner-Whitin and Backlogging

        procedure XFormWWUB(
            s : array (range) of linctr,
            r : array (range) of linctr,
            y : array (range) of linctr,
            d : array (range) of real,
            NT : integer,
            Tk : integer,
            MC : integer)

            declarations
                a,b: array(1..NT) of mpvar
                XA,XB:array(1..NT,1..NT) of linctr
                XY:array(1..NT) of linctr
                D : array (range,range) of real
            end-declarations

            CumulDemand(d,D,NT)

            forall (t in 1..NT) XY(t):=a(t)+b(t)+y(t)>=1

            forall (k in 1..NT,t in k..minlist(NT,k+Tk-1) | D(t,t)>0) XA(k,t) :=
              s(k-1)>=sum(i in k..t) D(i,i)*a(i) - sum (i in k..t-1) D(i+1,t)*y(i)
            forall (k in 1..NT,t in maxlist(1,k-Tk+1)..k | D(t,t)>0) XB(k,t) :=
              r(k)>=sum(i in t..k) D(i,i)*b(i) - sum (i in t+1..k) D(t,i-1)*y(i)
            if MC=1 then
            forall (k in 1..NT,t in k..minlist(NT,k+Tk-1)| D(t,t)>0)
              setmodcut(XA(k,t))
            forall (k in 1..NT,t in maxlist(1,k-Tk+1)..k | D(t,t)>0)
              setmodcut(XB(k,t))
            end-if
        end-procedure
        """
        from .xformutils import NetDemand, CumulDemand
        s[0], d = NetDemand(s[0], d, NT)

        # CumulDemand(d,D,NT)
        D = {}
        CumulDemand(d, D, NT)

        D_values = ''.join(
            '[{},{}]{}'.format(i, j, D[i,j])
            for i in range(1, NT+1) for j in range(1, NT+1)
        )
        model += """
        param $D{{1..{NT}, 1..{NT}}};
        data; param $D := {D_values}; model;
        """.replace('$', prefix).format(NT=NT, D_values=D_values)

        # a,b: array(1..NT) of mpvar
        model += """
        var $a{{1..{NT}}};
        var $b{{1..{NT}}};
        """.replace('$', prefix).format(NT=NT)

        # forall (t in 1..NT) XY(t) :=
        # a(t)+b(t)+y(t)>=1
        model += """
        s.t. $XY{{$t in 1..{NT}}}: $a[$t]+$b[$t]+{y}[$t] >= 1;
        """.replace('$', prefix).format(NT=NT, y=yname)

        # forall (k in 1..NT,t in k..minlist(NT,k+Tk-1) | D(t,t)>0) XA(k,t) :=
        # s(k-1)>=sum(i in k..t) D(i,i)*a(i) - sum (i in k..t-1) D(i+1,t)*y(i)
        model += """
        s.t. $XA{{$k in 1..{NT}, $t in $k..min({NT}, $k+{Tk}-1): $D[$t,$t]>0}}:
            {s}[$k-1] >=
                sum{{$i in $k..$t}} $D[$i,$i]*$a[$i]
                - sum{{$i in $k..$t-1}} $D[$i+1,$t]*{y}[$i];
        """.replace('$', prefix).format(NT=NT, Tk=Tk, y=yname, s=sname)

        # forall (k in 1..NT,t in maxlist(1,k-Tk+1)..k | D(t,t)>0) XB(k,t) :=
        # r(k)>=sum(i in t..k) D(i,i)*b(i) - sum (i in t+1..k) D(t,i-1)*y(i)
        model += """
        s.t. $XB{{$k in 1..{NT}, $t in max(1, $k-{Tk}+1)..$k: $D[$t,$t]>0}}:
            {r}[$k] >=
                sum{{$i in $t..$k}} $D[$i,$i]*$b[$i]
                - sum{{$i in $t+1..$k}} $D[$t,$i-1]*{y}[$i];
        """.replace('$', prefix).format(NT=NT, Tk=Tk, y=yname, r=rname)

        model += '#END WW-U-B\n'
        model = model.replace('\n        ', '\n').replace('\n\n', '\n')
        self._pyvars["_model"] += model


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
