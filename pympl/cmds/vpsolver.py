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
from __future__ import print_function
from builtins import zip
from builtins import str
from builtins import range
import six

import re
from .base import CmdBase, SubmodBase
from ..model import Model, writemod
from ..tools import Tools
from .. import utils


class CmdVBPGraph(CmdBase):
    """Command for creating arc-flow graphs for VBP instances."""

    def _evalcmd(
            self, names, W, w, labels, bounds=None, binary=False,
            S="S", T="T", LOSS="LOSS"):
        """Evalutate CMD[names](*args)."""
        match = utils.parse_symblist(names)
        assert match is not None
        Vname, Aname = match

        graph = self._generate_graph(
            W, w, labels, bounds, binary, S, T, LOSS
        )

        defs = ""
        defs += utils.ampl_set(
            Vname, graph.V, self._sets, self._params
        )[0]
        defs += utils.ampl_set(
            Aname, graph.A, self._sets, self._params
        )[0]
        self._pyvars["_defs"] += defs

    def _generate_graph(self, W, w, labels, bounds, binary, S, T, LOSS):
        """Generate an arc-flow graph."""
        from pyvpsolver import VBP, AFG
        m = len(w)
        ndims = len(W)
        if bounds is not None:
            b = bounds
        else:
            b = [
                min(W[d]//w[i][d]) for d in range(ndims) if w[i][d] != 0
                for i in range(m)
            ]
        instance = VBP(W, w, b, binary=binary, verbose=False)
        graph = AFG(instance, verbose=Tools.VERBOSE).graph()
        graph.relabel(
            lambda u: S if u == graph.S else T if u == graph.Ts[0] else str(u),
            lambda lbl: labels[lbl] if lbl != graph.LOSS else LOSS
        )
        return graph


class CmdMVPGraph(CmdBase):
    """Command for creating arc-flow graphs for MVP instances."""

    def _evalcmd(
            self, names, Ws, ws, labels, bounds=None, binary=False,
            S="S", Ts=None, LOSS="LOSS"):
        """Evalutate CMD[names](*args)."""
        match = utils.parse_symblist(names)
        assert match is not None
        Vname, Aname = match

        graph = self._generate_graph(
            Ws, ws, labels, bounds, binary, S, Ts, LOSS
        )

        defs = ""
        defs += utils.ampl_set(
            Vname, graph.V, self._sets, self._params
        )[0]
        A_expanded = [
            (u, v, lbl) if not isinstance(lbl, (tuple, list))
            else (u, v) + tuple(lbl)
            for (u, v, lbl) in graph.A
        ]
        defs += utils.ampl_set(
            Aname, A_expanded, self._sets, self._params
        )[0]
        self._pyvars["_defs"] += defs

    def _generate_graph(self, Ws, ws, labels, bounds, binary, S, Ts, LOSS):
        """Generate an arc-flow graph."""
        from pyvpsolver import MVP, AFG
        m = len(ws)
        ndims = len(Ws[0])
        if bounds is not None:
            b = bounds
        else:
            maxW = [max(Wi[d] for Wi in Ws) for d in range(ndims)]
            b = [None]*m
            for i in range(m):
                minw = [min(wi[d] for wi in ws[i]) for d in range(ndims)]
                b[i] = min(
                    maxW[d]//minw[d]
                    for d in range(ndims) if minw[d] != 0
                )

        Cs = [1]*len(Ws)
        Qs = [-1]*len(Ws)
        instance = MVP(Ws, Cs, Qs, ws, b, binary=binary, verbose=False)
        graph = AFG(instance, verbose=Tools.VERBOSE).graph()

        vlbl = {}
        assert Ts is None or len(Ts) == len(graph.Ts)
        for u in graph.V:
            if u == graph.S:
                vlbl[u] = S
            elif u in graph.Ts:
                vlbl[u] = Ts[graph.Ts.index(u)]
            else:
                vlbl[u] = str(u)

        graph.relabel(
            lambda u: vlbl.get(u),
            lambda lbl: labels[lbl] if lbl != graph.LOSS else LOSS
        )
        return graph


class SubmodVBPFlow(SubmodBase):
    """Command for creating arc-flow models for VBP instances."""

    def __init__(self, *args, **kwargs):
        SubmodBase.__init__(self, *args, **kwargs)
        self._zvars = []
        self._models = []
        self._graphs = []
        self._prefixes = []

    def _evalcmd(self, zvar, W, w, b, bounds=None, labels=None, binary=False):
        """Evalutate CMD[zvar](*args)."""
        match = utils.parse_symbname(zvar, allow_index="[]")
        assert match is not None
        zvar = match

        prefix = self._new_prefix()

        graph, model, declared_vars = self._generate_model(
            zvar, W, w, b, bounds, binary, labels, prefix
        )

        self._zvars.append(zvar.lstrip("^"))
        self._models.append(model)
        self._graphs.append(graph)
        self._prefixes.append(prefix)

        self._pyvars["_model"] += writemod.model2ampl(model, declared_vars)

    def _generate_model(self, zvar, W, w, b, bounds=None, binary=False,
                        labels=None, prefix=""):
        """Generate an arc-flow model."""
        from pyvpsolver import VBP, AFG
        m = len(w)
        bb = [0]*m
        bvars = []
        for i in range(m):
            if isinstance(b[i], six.string_types):
                bb[i] = min(
                    W[d]//w[i][d] for d in range(len(w[i])) if w[i][d] != 0
                )
                if bounds is not None:
                    bb[i] = min(bb[i], bounds[i])
                bvars.append(b[i])
            else:
                bb[i] = b[i]

        instance = VBP(W, w, bb, binary=binary, verbose=False)
        graph = AFG(instance, verbose=Tools.VERBOSE).graph()
        feedback = (graph.Ts[0], graph.S, graph.LOSS)

        vnames = {}
        vnames[feedback] = zvar
        ub = {}
        varl, cons = graph.get_flow_cons(vnames)
        assocs = graph.get_assocs(vnames)
        graph.names = vnames

        if labels is None:
            labels = {i: "i={0}".format(i+1) for i in instance.labels}
            for i in range(m):
                if isinstance(b[i], six.string_types):
                    labels[i] = b[i]
        graph.set_labels({
            (u, v, i): [labels[i]]
            for (u, v, i) in graph.A
            if i in labels
        })

        for i in range(m):
            if i not in assocs:
                assocs[i] = []
            if bounds is not None:
                for var in assocs[i]:
                    ub[var] = bounds[i]
            if isinstance(b[i], six.string_types):
                varl.append(b[i])
                cons.append((assocs[i], "=", b[i]))
            else:
                if b[i] > 1:
                    cons.append((assocs[i], ">=", b[i]))
                else:
                    cons.append((assocs[i], "=", b[i]))

        model = Model()
        for var in varl:
            model.add_var(name=var, lb=0, ub=ub.get(var, None), vtype="I")
        for lincomb, sign, rhs in cons:
            model.add_con(lincomb, sign, rhs)

        model.add_var(name="_total_flow", vtype="I")
        model.add_con("_total_flow", "=", zvar)

        declared_vars = set(bvars)

        def var_name(name):
            if name == zvar:
                return name
            elif name in declared_vars:
                return name
            else:
                return prefix+name

        def con_name(name):
            return prefix+name

        model.rename_vars(var_name)
        model.rename_cons(con_name)

        return graph, model, declared_vars

    def extract(self, get_var_value, verbose=None):
        """Extract arc-flow solutions."""
        lst_sol = []
        for zvar, model, graph, prefix in zip(
                self._zvars, self._models, self._graphs, self._prefixes):
            varvalues = {
                var.replace(prefix, "", 1): get_var_value(var)
                for var in model.vars if var.startswith(prefix)
            }
            total_flow = varvalues.get("_total_flow", 0)
            graph.set_flow(varvalues)
            sol = graph.extract_solution(
                graph.S, "<-", graph.Ts[0], flow_limit=total_flow
            )
            lst_sol.append((zvar, varvalues.get(zvar, 0), sol))
            Tools.log(
                "Graph: {0} (flow={1:d})\n\t{2}".format(
                    zvar, total_flow, sol
                ), verbose=verbose
            )
        return lst_sol


class SubmodMVPFlow(SubmodBase):
    """Command for creating arc-flow models for MVP instances."""

    def __init__(self, *args, **kwargs):
        SubmodBase.__init__(self, *args, **kwargs)
        self._zvars = []
        self._models = []
        self._graphs = []
        self._prefixes = []

    def _evalcmd(self, zvar, Ws, ws, b, bounds=None, binary=False,
                 labels=None, i0=0):
        """Evalutate CMD[zvar](*args)."""
        match = utils.parse_indexed(zvar, "{}")
        assert match is not None
        zvar, index_list = match
        assert index_list is None or len(index_list) == 1

        prefix = self._new_prefix()

        if zvar.startswith("^"):
            zvar = zvar.lstrip("^")
        else:
            if index_list is not None:
                assert len(index_list) == 1
                index = index_list[0]
            else:
                index = "{}_I".format(zvar)

            if not index.startswith("^"):
                sdefs, sdata = utils.ampl_set(
                    index,
                    list(range(i0, i0+len(Ws))),
                    self._sets, self._params
                )
                self._pyvars["_defs"] += sdefs
                self._pyvars["_data"] += sdata

            self._pyvars["_model"] += utils.ampl_var(
                zvar, index=index, typ="I", lb=0, ub=None
            )

        zvars = ["^{}[{}]".format(zvar, i0+i) for i in range(len(Ws))]
        graph, model, declared_vars = self._generate_model(
            zvars, Ws, ws, b, bounds, binary, labels, prefix
        )

        self._zvars.append([zvar.lstrip("^") for zvar in zvars])
        self._models.append(model)
        self._graphs.append(graph)
        self._prefixes.append(prefix)

        self._pyvars["_model"] += writemod.model2ampl(model, declared_vars)

    def _generate_model(self, zvars, Ws, ws, b, bounds=None, binary=False,
                        labels=None, prefix=""):
        """Generate an arc-flow model."""
        from pyvpsolver import MVP, AFG
        ndims = len(Ws[0])
        m = len(ws)
        bb = [0]*m
        bvars = []
        maxW = [max(Wi[d] for Wi in Ws) for d in range(ndims)]
        for i in range(m):
            if isinstance(b[i], six.string_types):
                minw = [min(wi[d] for wi in ws[i]) for d in range(ndims)]
                bb[i] = min(
                    maxW[d]//minw[d] for d in range(ndims) if minw[d] != 0
                )
                if bounds is not None:
                    bb[i] = min(bb[i], bounds[i])
                bvars.append(b[i])
            else:
                bb[i] = b[i]

        Cs = [1]*len(Ws)
        Qs = [-1]*len(Ws)
        instance = MVP(Ws, Cs, Qs, ws, bb, binary=binary, verbose=False)
        graph = AFG(instance, verbose=Tools.VERBOSE).graph()

        vnames = {
            (T, graph.S, graph.LOSS): zvar
            for zvar, T in zip(zvars, graph.Ts)
        }

        ub = {}
        varl, cons = graph.get_flow_cons(vnames)
        assocs = graph.get_assocs(vnames)
        graph.names = vnames

        nopts = [len(ws[i]) for i in range(m)]

        if labels is None:
            names = ["i={}".format(i+1) for i in range(m)]
            for i in range(m):
                if isinstance(b[i], six.string_types):
                    names[i] = b[i]
            labels = {
                (i, j): "{} opt={}".format(names[i], j+1)
                for i, j in instance.labels
            }
        graph.set_labels({
            (u, v, lbl): [labels[lbl]]
            for (u, v, lbl) in graph.A
            if lbl in labels
        })

        for i in range(m):
            lincomb = []
            for j in range(nopts[i]):
                lincomb += assocs.get((i, j), [])
            if bounds is not None:
                for var in lincomb:
                    ub[var] = bounds[i]
            if isinstance(b[i], six.string_types):
                varl.append(b[i])
                cons.append((lincomb, "=", b[i]))
            else:
                if b[i] > 1:
                    cons.append((lincomb, ">=", b[i]))
                else:
                    cons.append((lincomb, "=", b[i]))

        model = Model()
        for var in varl:
            model.add_var(name=var, lb=0, ub=ub.get(var, None), vtype="I")
        for lincomb, sign, rhs in cons:
            model.add_con(lincomb, sign, rhs)

        for i, zvar in enumerate(zvars):
            flowvar = "_total_flow_{}".format(i)
            model.add_var(name=flowvar, vtype="I")
            model.add_con(flowvar, "=", zvar)

        declared_vars = set(bvars)

        def var_name(name):
            if name in zvars:
                return name
            elif name in declared_vars:
                return name
            else:
                return prefix+name

        def con_name(name):
            return prefix+name

        model.rename_vars(var_name)
        model.rename_cons(con_name)

        return graph, model, declared_vars

    def extract(self, get_var_value, verbose=None):
        """Extract arc-flow solutions."""
        lst_sol = []
        for zvars, model, graph, prefix in zip(
                self._zvars, self._models, self._graphs, self._prefixes):
            varvalues = {
                var.replace(prefix, "", 1): get_var_value(var)
                for var in model.vars if var.startswith(prefix)
            }
            for i, zvar, T in zip(range(len(zvars)), zvars, graph.Ts):
                total_flow_i = varvalues.get("_total_flow_{}".format(i), 0)
                graph.set_flow(varvalues)
                sol = graph.extract_solution(
                    graph.S, "<-", T, flow_limit=total_flow_i
                )
                lst_sol.append((zvar, varvalues.get(zvar, 0), sol))
                Tools.log(
                    "Graph: {0} (flow={1:d})\n\t{2}".format(
                        zvar, total_flow_i, sol
                    ), verbose=verbose
                )
        return lst_sol
