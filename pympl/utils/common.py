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
from builtins import range
from builtins import object
import six

from collections import defaultdict


def linear_constraint(left, sign, right):
    """Transforms (left, sign, right) constraints into (lincomb, sign, rhs)."""
    assert (
        not isinstance(left, (int, float)) or
        not isinstance(right, (int, float))
    )
    pairs = defaultdict(lambda: 0)
    rhs = 0

    def add_entry(e, signal):
        assert isinstance(e, (int, float, six.string_types, tuple))
        if isinstance(e, (int, float)):
            return -signal*e
        elif isinstance(e, six.string_types):
            pairs[e] += signal
            return 0
        elif isinstance(e, tuple):
            a, b = e
            assert (
                isinstance(a, (int, float, six.string_types)) and
                isinstance(b, (int, float, six.string_types))
            )
            if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                return signal*a*b
            elif isinstance(a, six.string_types):
                assert isinstance(b, (int, float))
                pairs[a] += signal*b
            else:
                assert isinstance(b, six.string_types)
                assert isinstance(a, (int, float))
                pairs[b] += signal*a
            return 0

    if isinstance(left, (int, float, six.string_types, tuple)):
        rhs += add_entry(left, 1)
    else:
        for e in left:
            rhs += add_entry(e, 1)

    if isinstance(right, (int, float, six.string_types, tuple)):
        rhs += add_entry(right, -1)
    else:
        for e in right:
            rhs += add_entry(e, -1)

    if sign in ("<", ">"):
        sign += "="

    lincomb = sorted(pairs.items())
    return (lincomb, sign, rhs)


def lincomb2str(lincomb, mult="*"):
    """Returns the linear combination as a string."""

    def format_entry(var, coef):
        var = var.lstrip("^")  # PyMPL special marker
        if abs(coef) != 1:
            if coef >= 0:
                return " +{0}{1}{2}".format(repr(coef), mult, var)
            else:
                return " -{0}{1}{2}".format(repr(abs(coef)), mult, var)
        else:
            if coef >= 0:
                return " +{0}".format(var)
            else:
                return " -{0}".format(var)

    return "".join(format_entry(var, coef) for var, coef in lincomb)


def list2dict(lst, i0=0):
    """Converts lists to dictionaries."""
    dic = {}

    def conv_rec(key, lst):
        for i in range(len(lst)):
            if not isinstance(lst[i], list):
                if key == []:
                    dic[i0+i] = lst[i]
                else:
                    dic[tuple(key+[i0+i])] = lst[i]
            else:
                conv_rec(key+[i0+i], lst[i])

    conv_rec([], lst)
    return dic


class UnionFind(object):
    """Union-find data structure."""

    def __init__(self, N):
        """Create a new empty union-find structure."""
        self.N = N
        self.init()

    def init(self):
        """Initialize data."""
        self.ngroups = self.N
        self.p = list(range(self.N))
        self.rank = [0]*self.N

    def find(self, x):
        """Find root of x."""
        if self.p[x] != x:
            self.p[x] = self.find(self.p[x])
        return self.p[x]

    def link(self, x, y):
        """Link x and y."""
        x = self.find(x)
        y = self.find(y)
        if x != y:
            self.ngroups -= 1;
            if self.rank[x] > self.rank[y]:
                self.p[y] = x
            else:
                self.p[x] = y
                if self.rank[x] == self.rank[y]:
                    self.rank[y] += 1

    def groups(self):
        """Retrieve groups."""
        from collections import defaultdict
        grps = defaultdict(list)
        for x in range(self.N):
            grps[self.find(x)].append(x)
        return list(grps.values())
