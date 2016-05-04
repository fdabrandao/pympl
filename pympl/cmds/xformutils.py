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
from __future__ import division
from builtins import range

from math import floor, ceil

"""
Most of models included in this file come from the library of reformulations
LS-LIB proposed in:
  Production Planning by Mixed Integer Programming (Pochet and Wolsey 2006).
The implementations are a direct translation of LS-LIB's xform.mos file with
minor modifications.
"""

"""
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!  All Book Extended Formulations  !
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

! Xform  9/9/2005
!  Contains
!    WW-U       (XFormWWU) seems to be ok! (bike.mod, clb.mod)
!    WW-U-B     (XFormWWUB) seems to be ok! (bike.mod, clb.mod)
!    WW-U-SC    (XFormWWUSC) seems to be ok! (clb.mod)
!    WW-U-SC,B  (XFormWWUSCB) seems to be ok! (clb.mod)
!    WW-CC      (XFormWWCC) seems to be ok! (clb.mod)

!    LS-U1=(MC) (XFormLSU1) assumes s[NT] = 0 and is not compatible with LB
!    LS-U2=(SP) (XFormLSU2) assumes s[NT] = 0 and is not compatible with LB
!    LS-U-B     (XFormLSUB) assumes s[NT] = 0 and is not compatible with LB

! Added 30/9/2005
!    DLSI-CC    (XFormDLSICC) approximation if s0 != 0
!    DLSI-CC-B  (XFormDLSICCB) approximation if s0 != 0 (cgp.mod, clb.mod)
!    DLS-CC-B   (XFormDLSCCB) seems to be ok! (cgp.mod, clb.mod)
!    DLS-CC-SC  (XFormDLSCCSC) approximation and requires 0-1 demands (clb.mod)

! Added 30/9/05
!    WW-U-LB    (XFormWWULB) approximation
!    WW-CC-B    (XFormWWCCB) seems to be ok! (clb.mod)

! Added 1/11/15
!    LS-U-SC    (XFormLSUSC) assumes s[NT] = 0 and is not compatible with LB
!    LS-U-SC,B  (XFormLSUSCB) assumes s[NT] = 0 and is not compatible with LB
"""


def mrange(a, b):
    """Return a range [a, b]."""
    return range(a, b+1)


def NetDemand(sinit, d, NT):
    """Compute the net demand when s[0] != 0."""
    if isinstance(sinit, str):
        netd = {}
        for t in mrange(1, NT):
            netd[t] = d[t]
        return sinit, netd
    else:
        netd = {}
        for t in mrange(1, NT):
            netd[t] = max(d[t]-sinit, 0)
            sinit = max(sinit-d[t], 0)
        return sinit, netd


def CumulDemand(d, D, NT):
    """
    procedure CumulDemand(
        d : array (range) of real,
        D : array (range,range) of real,
        NT : integer)
        forall (k in 1..NT) D(k,k):=d(k)
        forall (k in 1..NT,l in k+1..NT) D(k,l):=D(k,l-1)+d(l)
        forall (k in 1..NT,l in 1..k-1) D(k,l):=0
    end-procedure
    """
    # forall (k in 1..NT) D(k,k):=d(k)
    for k in mrange(1, NT):
        D[k, k] = d[k]

    for k in mrange(1, NT):
        D[k, 0] = 0

    # forall (k in 1..NT,l in k+1..NT) D(k,l):=D(k,l-1)+d(l)
    for k in mrange(1, NT):
        for l in mrange(k+1, NT):
            D[k, l] = D[k, l-1]+d[l]

    # forall (k in 1..NT,l in 1..k-1) D(k,l):=0
    for k in mrange(1, NT):
        for l in mrange(1, k-1):
            D[k, l] = 0


def CumulDemand0(d, D, NT):
    """
    procedure CumulDemand0(
        d : array (range) of real,
        D : array (range) of real,
        NT : integer)
        D(1):=d(1)
        forall (l in 2..NT) D(l):=D(l-1)+d(l)
    end-procedure
    """
    # D(1):=d(1)
    # forall (l in 2..NT) D(l):=D(l-1)+d(l)
    D[1] = d[1]
    for l in mrange(2, NT):
        D[l] = D[l-1]+d[l]


def XFormWWU(model, s, y, d, NT, Tk, prefix=""):
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
    s[0], d = NetDemand(s[0], d, NT)

    # CumulDemand(d,D,NT)
    D = {}
    CumulDemand(d, D, NT)

    # forall (k in 1..NT,l in k..minlist(NT,k+Tk-1)| D(l,l)>0) XWW(k,l) :=
    # s(k-1) >= D(k,l) - sum (i in k..l) D(i,l)*y(i)
    for k in mrange(1, NT):
        for l in mrange(k, min(NT, k+Tk-1)):
            if D[l, l] > 0:
                rhs = [D[k, l]]+[
                    (-D[i, l], y[i])
                    for i in mrange(k, l)
                ]
                model.add_con(s[k-1], ">=", rhs)


def XFormWWUB(model, s, r, y, d, NT, Tk, prefix=""):
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
    s[0], d = NetDemand(s[0], d, NT)

    # CumulDemand(d,D,NT)
    D = {}
    CumulDemand(d, D, NT)

    def avar(i):
        return prefix+"a_{0}".format(i)

    def bvar(i):
        return prefix+"b_{0}".format(i)

    # a,b: array(1..NT) of mpvar
    for i in mrange(1, NT):
        model.add_var(name=avar(i), lb=0)
        model.add_var(name=bvar(i), lb=0)

    # forall (t in 1..NT) XY(t) :=
    # a(t)+b(t)+y(t)>=1
    for t in mrange(1, NT):
        model.add_con([avar(t), bvar(t), y[t]], ">=", 1)

    # forall (k in 1..NT,t in k..minlist(NT,k+Tk-1) | D(t,t)>0) XA(k,t) :=
    # s(k-1)>=sum(i in k..t) D(i,i)*a(i) - sum (i in k..t-1) D(i+1,t)*y(i)
    for k in mrange(1, NT):
        for t in mrange(k, min(NT, k+Tk-1)):
            if D[t, t] > 0:
                rhs = []
                for i in mrange(k, t):
                    rhs.append((D[i, i], avar(i)))
                for i in mrange(k, t-1):
                    rhs.append((-D[i+1, t], y[i]))
                model.add_con(s[k-1], ">=", rhs)

    # forall (k in 1..NT,t in maxlist(1,k-Tk+1)..k | D(t,t)>0) XB(k,t) :=
    # r(k)>=sum(i in t..k) D(i,i)*b(i) - sum (i in t+1..k) D(t,i-1)*y(i)
    for k in mrange(1, NT):
        for t in mrange(max(1, k-Tk+1), k):
            if D[t, t] > 0:
                rhs = [
                    (D[i, i], bvar(i))
                    for i in mrange(t, k)
                ]+[
                    (-D[t, i-1], y[i])
                    for i in mrange(t+1, k)
                ]
                model.add_con(r[k], ">=", rhs)


def XFormWWUSC(model, s, y, z, d, NT, Tk, prefix=""):
    """
    Wagner-Whitin and Start-up

    procedure XFormWWUSC(
        s : array (range) of linctr,
        y : array (range) of linctr,
        z : array (range) of linctr,
        d : array (range) of real,
        NT : integer,
        Tk : integer,
        MC: integer)

        declarations
            XWW: array (1..NT,range) of linctr
            D : array (range,range) of real
        end-declarations

        CumulDemand(d,D,NT)

        forall (k in 1..NT,l in k..minlist(NT,k+Tk-1)| D(l,l)>0) XWW(k,l) :=
            s(k-1) >= D(k,l) - D(k,l)*y(k) - sum (i in k+1..l) D(i,l)*z(i)

        if MC = 1 then
          forall (k in 1..NT,l in k..minlist(NT,k+Tk-1)| D(l,l)>0 )
          setmodcut(XWW(k,l))
        end-if
    end-procedure
    """
    s[0], d = NetDemand(s[0], d, NT)

    # CumulDemand(d,D,NT)
    D = {}
    CumulDemand(d, D, NT)

    # forall (k in 1..NT,l in k..minlist(NT,k+Tk-1)| D(l,l)>0) XWW(k,l) :=
    # s(k-1) >= D(k,l) - D(k,l)*y(k) - sum (i in k+1..l) D(i,l)*z(i)
    for k in mrange(1, NT):
        for l in mrange(k, min(NT, k+Tk-1)):
            if D[l, l] > 0:
                rhs = [D[k, l], (-D[k, l], y[k])]
                for i in mrange(k+1, l):
                    rhs.append((-D[i, l], z[i]))
                model.add_con(s[k-1], ">=", rhs)


def XFormWWUSCB(model, s, r, y, z, w, d, NT, Tk, prefix=""):
    """
    Wagner-Whitin, Backlogging and Start-up

    procedure XFormWWUSCB(
        s : array (range) of linctr,
        r : array (range) of linctr,
        y : array (range) of linctr,
        z : array (range) of linctr,
        w : array (range) of linctr,
        d : array (range) of real,
        NT : integer,
        Tk : integer,
        MC: integer)

        declarations
            a,b: array(1..NT) of mpvar
            XA,XB:array(1..NT,1..NT) of linctr
            XY:array(1..NT) of linctr
        end-declarations

        ! Modification 9/2/04 to be checked
        !forall (t in 1..NT) XY(t):=a(t)+b(t)+y(t)>=1
        forall (t in 1..NT | d(t) > 0) XY(t):=a(t)+b(t)+y(t)>=1

        ! modification  9/2/04
        forall (k in 1..NT,t in k..minlist(NT,k+Tk-1)| d(t) > 0)
          !XA(k,t):=s(k-1)>=sum(l in k..t) d(l)*(a(l)-sum(i in k+1..l) w(i))
          ! 2nd modification 12/12/07. No
          XA(k,t):=s(k-1)>=sum(l in k..t) d(l)*(a(l)-sum(i in k..l-1) w(i))
          !XA(k,t):=s(k-1) >= sum(l in k..t) d(l)*(a(l) -if(l>k,y(k),0)-
          !  if(l>k+1,sum(i in k+1..l-1) z(i),0))
        forall (k in 1..NT,t in maxlist(1,k-Tk+1)..k | d(t) > 0)
          XB(k,t):=r(k) >= sum(l in t..k) d(l)*(b(l) - sum(i in l+1..k) z(i))
        if MC=1 then
          forall (k in 1..NT,t in k..minlist(NT,k+Tk-1)| d(t) > 0)
            setmodcut(XA(k,t))
          forall (k in 1..NT,t in maxlist(1,k-Tk+1)..k | d(t) > 0)
            setmodcut(XB(k,t))
        end-if
    end-procedure
    """
    s[0], d = NetDemand(s[0], d, NT)

    def avar(i):
        return prefix+"a_{0}".format(i)

    def bvar(i):
        return prefix+"b_{0}".format(i)

    # a,b: array(1..NT) of mpvar
    for i in mrange(1, NT):
        model.add_var(name=avar(i), lb=0)
        model.add_var(name=bvar(i), lb=0)

    # forall (t in 1..NT | d(t) > 0) XY(t) :=
    # a(t)+b(t)+y(t)>=1
    for t in mrange(1, NT):
        if d[t] > 0:
            model.add_con([avar(t), bvar(t), y[t]], ">=", 1)

    # forall (k in 1..NT,t in k..minlist(NT,k+Tk-1)| d(t) > 0) XA(k,t) :=
    # s(k-1)>=sum(l in k..t) d(l)*(a(l)-sum(i in k..l-1) w(i))
    for k in mrange(1, NT):
        for t in mrange(k, min(NT, k+Tk-1)):
            if d[t] > 0:
                rhs = []
                for l in mrange(k, t):
                    rhs.append((d[l], avar(l)))
                    for i in mrange(k, l-1):
                        rhs.append((-d[l], w[i]))
                model.add_con(s[k-1], ">=", rhs)

    # forall (k in 1..NT,t in maxlist(1,k-Tk+1)..k | d(t) > 0) XB(k,t) :=
    # r(k) >= sum(l in t..k) d(l)*(b(l) - sum(i in l+1..k) z(i))
    for k in mrange(1, NT):
        for t in mrange(max(1, k-Tk+1), k):
            if d[t] > 0:
                rhs = []
                for l in mrange(t, k):
                    rhs.append((d[l], bvar(l)))
                    for i in mrange(l+1, k):
                        rhs.append((-d[l], z[i]))
                model.add_con(r[k], ">=", rhs)


def XFormWWULB(model, s, y, d, L, NT, Tk, prefix=""):
    """
    Wagner-Whitin, Constant Lower Bound

    procedure XFormWWULB(
        s : array (range) of linctr,
        y : array (range) of linctr,
        d : array (range) of real,
        L : real,
        NT : integer,
        Tk : integer,
        MC : integer)

        declarations
            Ts=1..NT
            Ts0=0..NT
            ws: array(Ts0,range) of mpvar
            gs: array(Ts0,range) of real
            ds: array(Ts0) of mpvar
            XS,XW:array(Ts0) of linctr
            XLKT:array(Ts0,Ts0) of linctr
            XRKT:array(Ts0,Ts0,Ts0) of linctr
            D : array (range,range) of real
        end-declarations

        CumulDemand(d,D,NT)
        forall(k in Ts0,t in k+1..minlist(NT,k+Tk))
            gs(k,t):=D(k+1,t)-L*(ceil(D(k+1,t)/L)-1)
        forall(k in Ts0,t in maxlist(0,k-Tk)..k-1)
            gs(k,t):=L*(floor(D(t+1,k)/L)+1)-D(t+1,k)
        forall(k in Ts0)
            gs(k,k):=L
        forall(k in Ts0,t in maxlist(0,k-Tk)..minlist(NT,k+Tk)|gs(k,t)<>0)
            create(ws(k,t))

        forall(k in Ts0) XS(k):=
          s(k)>=L*ds(k)+
          sum(i in maxlist(0,k-Tk)..minlist(NT,k+Tk))gs(k,i)*ws(k,i)
        forall(k in Ts0) XW(k):=
          sum(i in maxlist(0,k-Tk)..minlist(NT,k+Tk)) ws(k,i)<=1
        forall (k in Ts0,l in k+1..minlist(NT,k+Tk),t in k..l) XRKT(k,l,t) :=
          ds(k)+
          sum(i in maxlist(0,k-Tk)..minlist(NT,k+Tk)|gs(k,i)>=gs(k,t))ws(k,i)>=
          floor( (D(k+1,l)-gs(k,t))/L)+1+
          sum(i in k+1..l)
            (floor((D(k+1,i-1)-gs(k,t))/L) - floor( (D(k+1,l)-gs(k,t))/L))*y(i)
        forall(k in Ts0,t in maxlist(0,k-Tk)..k-1) XLKT(k,t) :=
          ds(k)+
          sum(i in maxlist(0,k-Tk)..minlist(NT,k+Tk)|gs(k,i)>=gs(k,t))ws(k,i)>=
          sum(i in t+1..k)y(i)-floor(D(t+1,k)/L)
    end-procedure
    """
    s[0], d = NetDemand(s[0], d, NT)

    # Ts=1..NT
    # Ts0=0..NT
    Ts = mrange(1, NT)
    Ts0 = mrange(0, NT)

    # ws: array(Ts0,range) of mpvar
    def wsvar(i, j):
        return prefix+"ws_{0}_{1}".format(i, j)

    # ds: array(Ts0) of mpvar
    def dsvar(i):
        return prefix+"ds_{0}".format(i)

    # CumulDemand(d,D,NT)
    D = {}
    CumulDemand(d, D, NT)

    gs = {}
    # forall(k in Ts0,t in k+1..minlist(NT,k+Tk))
    # gs(k,t):=D(k+1,t)-L*(ceil(D(k+1,t)/L)-1)
    for k in Ts0:
        for t in mrange(k+1, min(NT, k+Tk)):
            gs[k, t] = D[k+1, t]-L*(ceil(D[k+1, t]/L)-1)

    # forall(k in Ts0,t in maxlist(0,k-Tk)..k-1)
    # gs(k,t):=L*(floor(D(t+1,k)/L)+1)-D(t+1,k)
    for k in Ts0:
        for t in mrange(max(0, k-Tk), k-1):
            gs[k, t] = L*(floor(D[t+1, k]/L)+1)-D[t+1, k]

    # forall(k in Ts0) gs(k,k):=L
    for k in Ts0:
        gs[k, k] = L

    # ws: array(Ts0,range) of mpvar
    # ds: array(Ts0) of mpvar
    # forall(k in Ts0,t in maxlist(0,k-Tk)..minlist(NT,k+Tk)|gs(k,t)<>0)
    #   create(ws(k,t))
    for k in Ts0:
        model.add_var(name=dsvar(k), lb=0)
        for t in mrange(max(0, k-Tk), min(NT, k+Tk)):
            if gs[k, t] != 0:
                model.add_var(name=wsvar(k, t), lb=0)

    # forall(k in Ts0) XS(k) :=
    # s(k)>=L*ds(k)+sum(i in maxlist(0,k-Tk)..minlist(NT,k+Tk))gs(k,i)*ws(k,i)
    for k in Ts0:
        rhs = [(L, dsvar(k))] + [
            (gs[k, i], wsvar(k, i))
            for i in mrange(max(0, k-Tk), min(NT, k+Tk))
            if gs[k, i] != 0
        ]
        model.add_con(s[k], ">=", rhs)

    # forall(k in Ts0) XW(k) :=
    # sum(i in maxlist(0,k-Tk)..minlist(NT,k+Tk)) ws(k,i)<=1
    for k in Ts0:
        lhs = [
            wsvar(k, i)
            for i in mrange(max(0, k-Tk), min(NT, k+Tk))
            if gs[k, i] != 0
        ]
        model.add_con(lhs, "<=", 1)

    # forall (k in Ts0,l in k+1..minlist(NT,k+Tk),t in k..l) XRKT(k,l,t) :=
    # ds(k)+
    # sum(i in maxlist(0,k-Tk)..minlist(NT,k+Tk)|gs(k,i)>=gs(k,t)) ws(k,i)
    # >=
    # floor( (D(k+1,l)-gs(k,t))/L)+1+
    # sum(i in k+1..l)
    #   (floor((D(k+1,i-1)-gs(k,t))/L) - floor( (D(k+1,l)-gs(k,t))/L))*y(i)
    for k in Ts0:
        for l in mrange(k+1, min(NT, k+Tk)):
            for t in mrange(k, l):
                lhs = [dsvar(k)]+[
                    wsvar(k, i)
                    for i in mrange(max(0, k-Tk), min(NT, k+Tk))
                    if gs[k, i] >= gs[k, t]
                ]
                rhs = [floor((D[k+1, l]-gs[k, t])/L)+1]
                for i in mrange(k+1, l):
                    # possible bug: floor((D[k+1, i-1]-gs[k, t])/float(L))
                    #               D[1, 0] is undefined
                    coef = (
                        floor((D[k+1, i-1]-gs[k, t])/L) -
                        floor((D[k+1, l]-gs[k, t])/L)
                    )
                    rhs.append((coef, y[i]))
                model.add_con(lhs, ">=", rhs)

    # forall(k in Ts0,t in maxlist(0,k-Tk)..k-1) XLKT(k,t) :=
    # ds(k)+
    # sum(i in maxlist(0,k-Tk)..minlist(NT,k+Tk)|gs(k,i)>=gs(k,t)) ws(k,i)
    # >= sum(i in t+1..k)y(i)-floor(D(t+1,k)/L)
    for k in Ts0:
        for t in mrange(max(0, k-Tk), k-1):
            lhs = [dsvar(k)]+[
                wsvar(k, i)
                for i in mrange(max(0, k-Tk), min(NT, k+Tk))
                if gs[k, i] >= gs[k, t]
            ]
            rhs = [y[i] for i in mrange(t+1, k)]+[-floor(D[t+1, k]/L)]
            model.add_con(lhs, ">=", rhs)


def XFormWWCC(model, s, y, d, C, NT, Tk, prefix=""):
    """
    Wagner-Whitin, Constant Capacity

    procedure XFormWWCC(
        s : array (range) of linctr,
        y : array (range) of linctr,
        d : array (range) of real,
        C : real,
        NT : integer,
        Tk : integer,
        MC: integer)

        declarations
            ws: array(0..NT-1,range) of mpvar
            gs: array(0..NT-1,range) of real
            ds: array(0..NT-1) of mpvar
            XS,XW:array (1..NT) of linctr
            XKT:array (1..NT,1..NT) of linctr
            D : array (range,range) of real
        end-declarations

        CumulDemand(d,D,NT)

        forall(k in 1..NT,t in k..minlist(NT,k+Tk-1)) create(ws(k-1,t))

        forall(k in 1..NT,t in k..minlist(NT,k+Tk-1)) do
            gs(k-1,t):=D(k,t)-C*floor(D(k,t)/C)
        end-do

        forall(k in 1..NT) do
            XS(k):= s(k-1) >=
                C*ds(k-1)+sum(i in k..minlist(NT,k+Tk-1))gs(k-1,i)*ws(k-1,i)
        end-do
        forall(k in 1..NT) XW(k):=sum(i in k..minlist(NT,k+Tk-1)) ws(k-1,i)<=1
        forall (k in 1..NT,t in k..minlist(NT,k+Tk-1)) XKT(k,t) :=
            ds(k-1)+sum(i in k..t)y(i)+
            sum(i in k..minlist(NT,k+Tk-1)|gs(k-1,i)>=gs(k-1,t))ws(k-1,i) >=
            floor(D(k,t)/C)+1
        if MC=1 then
        forall (k in 1..NT,t in k..minlist(NT,k+Tk-1)) setmodcut(XKT(k,t))
        end-if

    end-procedure
    """
    s[0], d = NetDemand(s[0], d, NT)

    def wsvar(i, j):
        return prefix+"ws_{0}_{1}".format(i, j)

    def dsvar(i):
        return prefix+"ds_{0}".format(i)

    # ws: array(0..NT-1,range) of mpvar
    # ds: array(0..NT-1) of mpvar
    for k in mrange(1, NT):
        for t in mrange(k, min(NT, k+Tk-1)):
            model.add_var(name=wsvar(k-1, t), lb=0)
        model.add_var(name=dsvar(k-1), lb=0)

    # CumulDemand(d,D,NT)
    # forall(k in 1..NT,t in k..minlist(NT,k+Tk-1))
    # gs(k-1,t):=D(k,t)-C*floor(D(k,t)/C)
    D = {}
    CumulDemand(d, D, NT)
    gs = {}
    for k in mrange(1, NT):
        for t in mrange(k, min(NT, k+Tk-1)):
            gs[k-1, t] = D[k, t]-C*floor(D[k, t]/C)

    # forall(k in 1..NT) XS(k) :=
    # s(k-1) >= C*ds(k-1)+sum(i in k..minlist(NT,k+Tk-1))gs(k-1,i)*ws(k-1,i)
    for k in mrange(1, NT):
        rhs = [(C, dsvar(k-1))]
        for i in mrange(k, min(NT, k+Tk-1)):
            rhs.append((gs[k-1, i], wsvar(k-1, i)))
        model.add_con(s[k-1], ">=", rhs)

    # forall(k in 1..NT) XW(k) := sum(i in k..minlist(NT,k+Tk-1)) ws(k-1,i)<=1
    for k in mrange(1, NT):
        lhs = [wsvar(k-1, i) for i in mrange(k, min(NT, k+Tk-1))]
        model.add_con(lhs, "<=", 1)

    # forall (k in 1..NT,t in k..minlist(NT,k+Tk-1)) XKT(k,t) :=
    # ds(k-1)+sum(i in k..t)y(i)+
    # sum(i in k..minlist(NT,k+Tk-1)|gs(k-1,i)>=gs(k-1,t)) ws(k-1,i) >=
    # floor(D(k,t)/C)+1
    for k in mrange(1, NT):
        for t in mrange(k, min(NT, k+Tk-1)):
            lhs = [dsvar(k-1)]+[y[i] for i in mrange(k, t)]
            lhs += [
                wsvar(k-1, i)
                for i in mrange(k, min(NT, k+Tk-1))
                if gs[k-1, i] >= gs[k-1, t]
            ]
            model.add_con(lhs, ">=", floor(D[k, t]/C)+1)


def XFormWWCCB2(model, s, r, y, D, C, T1, TN, prefix=""):
    """
    Wagner-Whitin, Constant Capacity and Backlogging (auxiliar function)

    procedure XFormWWCCB(
        s : array (range) of linctr,
        r : array (range) of linctr,
        y : array (range) of linctr,
        D : array (range,range) of real,
        C : real,
        T1: integer,
        TN: integer,
        MC: integer)

        declarations
            T0=T1-1
            Ts=T1..TN
            Ts0=T0..TN
        end-declarations

        declarations
            ws,wr: array(Ts0,Ts0) of mpvar
            gs,gr: array(Ts0,Ts0) of real
            ds,dr: array(Ts0) of mpvar
            Tkk,b:integer
            a:real
            XS,XR,XWS,XWR:array(Ts0) of linctr
            XLT:array(Ts,Ts,Ts0) of linctr
        end-declarations

        forall(k in Ts0,t in T0..k-1) gr(k,t):=D(t+1,k)-C*floor(D(t+1,k)/C)
        forall(k in Ts0,t in T0..k-1) gs(k,t):=C*ceil(D(t+1,k)/C)-D(t+1,k)

        forall(k in Ts0,t in k+1..TN) gs(k,t):=D(k+1,t)-C*floor(D(k+1,t)/C)
        forall(k in Ts0,t in k+1..TN) gr(k,t):=C*ceil(D(k+1,t)/C)-D(k+1,t)

        forall(k in Ts0) gs(k,k):=0
        forall(k in Ts0) gr(k,k):=0

        forall(k in T0..TN-1) XS(k):=s(k)>=C*ds(k)+sum(i in Ts0)gs(k,i)*ws(k,i)
        forall(k in Ts) XR(k):=r(k)>=C*dr(k)+sum(i in Ts0)gr(k,i)*wr(k,i)
        forall(k in T0..TN-1) XWS(k):=sum(i in Ts0) ws(k,i)<=1
        forall(k in Ts) XWR(k):=sum(i in Ts0) wr(k,i)<=1
        forall (k in Ts,l in k..TN,t in Ts0 | ceil( (D(k,l)-gr(l,t))/C) > 0)
            XLT(k,l,t):=ds(k-1)+dr(l)+sum(i in k..l)y(i)+
                         sum(i in Ts0|gs(k-1,i)>=gs(k-1,t))ws(k-1,i)+
                         sum(i in Ts0|gr(l,i)>gr(l,t))wr(l,i)>=
                         ceil( (D(k,l)-gr(l,t))/C)
        !if MC=1 then
        !forall (k in Ts,l in k..TN,t in Ts0) setmodcut(XLT(k,l,t))
        !end-if
    """
    # T0=T1-1
    # Ts=T1..TN
    # Ts0=T0..TN
    T0 = T1-1
    Ts = mrange(T1, TN)
    Ts0 = mrange(T0, TN)

    def wsvar(i, j):
        return prefix+"ws_{0}_{1}".format(i, j)

    def wrvar(i, j):
        return prefix+"wr_{0}_{1}".format(i, j)

    def dsvar(i):
        return prefix+"ds_{0}".format(i)

    def drvar(i):
        return prefix+"dr_{0}".format(i)

    # ws,wr: array(Ts0,Ts0) of mpvar
    for i in Ts0:
        for j in Ts0:
            if wsvar(i, j) not in model.vars:
                model.add_var(name=wsvar(i, j), lb=0)
            if wrvar(i, j) not in model.vars:
                model.add_var(name=wrvar(i, j), lb=0)

    # ds,dr: array(Ts0) of mpvar
    for i in Ts0:
        if dsvar(i) not in model.vars:
            model.add_var(name=dsvar(i), lb=0)
        if drvar(i) not in model.vars:
            model.add_var(name=drvar(i), lb=0)

    gr, gs = {}, {}
    # forall(k in Ts0,t in T0..k-1) gr(k,t):=D(t+1,k)-C*floor(D(t+1,k)/C)
    # forall(k in Ts0,t in T0..k-1) gs(k,t):=C*ceil(D(t+1,k)/C)-D(t+1,k)
    for k in Ts0:
        for t in mrange(T0, k-1):
            gr[k, t] = D[t+1, k]-C*floor(D[t+1, k]/C)
            gs[k, t] = C*ceil(D[t+1, k]/C)-D[t+1, k]

    # forall(k in Ts0,t in k+1..TN) gs(k,t):=D(k+1,t)-C*floor(D(k+1,t)/C)
    # forall(k in Ts0,t in k+1..TN) gr(k,t):=C*ceil(D(k+1,t)/C)-D(k+1,t)
    for k in Ts0:
        for t in mrange(k+1, TN):
            gs[k, t] = D[k+1, t]-C*floor(D[k+1, t]/C)
            gr[k, t] = C*ceil(D[k+1, t]/C)-D[k+1, t]

    # forall(k in Ts0) gs(k,k):=0
    # forall(k in Ts0) gr(k,k):=0
    for k in Ts0:
        gs[k, k] = 0
        gr[k, k] = 0

    # forall(k in T0..TN-1) XS(k) :=
    # s(k)>=C*ds(k)+sum(i in Ts0)gs(k,i)*ws(k,i)
    for k in mrange(T0, TN-1):
        rhs = [(C, dsvar(k))]
        for i in Ts0:
            rhs.append((gs[k, i], wsvar(k, i)))
        model.add_con(s[k], ">=", rhs)

    # forall(k in Ts) XR(k) :=
    # r(k)>=C*dr(k)+sum(i in Ts0)gr(k,i)*wr(k,i)
    for k in Ts:
        rhs = [(C, drvar(k))]
        for i in Ts0:
            rhs.append((gr[k, i], wrvar(k, i)))
        model.add_con(r[k], ">=", rhs)

    # forall(k in T0..TN-1) XWS(k) :=
    # sum(i in Ts0) ws(k,i)<=1
    for k in mrange(T0, TN-1):
        model.add_con([wsvar(k, i) for i in Ts0], "<=", 1)

    # forall(k in Ts) XWR(k) :=
    # sum(i in Ts0) wr(k,i)<=1
    for k in Ts:
        model.add_con([wrvar(k, i) for i in Ts0], "<=", 1)

    # forall (k in Ts,l in k..TN,t in Ts0 | ceil( (D(k,l)-gr(l,t))/C) > 0)
    # ds(k-1)+dr(l)+sum(i in k..l)y(i)+
    # sum(i in Ts0|gs(k-1,i)>=gs(k-1,t))ws(k-1,i)+
    # sum(i in Ts0|gr(l,i)>gr(l,t))wr(l,i)
    # >= ceil( (D(k,l)-gr(l,t))/C)
    for k in Ts:
        for l in mrange(k, TN):
            for t in Ts0:
                if ceil((D[k, l]-gr[l, t])/C) > 0:
                    lhs = [dsvar(k-1), drvar(l)]
                    for i in mrange(k, l):
                        lhs.append(y[i])
                    for i in Ts0:
                        if gs[k-1, i] >= gs[k-1, t]:
                            lhs.append(wsvar(k-1, i))
                    for i in Ts0:
                        if gr[l, i] > gr[l, t]:
                            lhs.append(wrvar(l, i))
                    model.add_con(lhs, ">=", ceil((D[k, l]-gr[l, t])/C))


def XFormWWCCB(model, s, r, y, d, C, NT, Tk, prefix=""):
    """
    Wagner-Whitin, Constant Capacity and Backlogging

    procedure XFormWWCCB(
        s : array (range) of linctr,
        r : array (range) of linctr,
        y : array (range) of linctr,
        d : array (range) of real,
        C : real,
        NT: integer,
        Tk: integer,
        MC: integer)

        declarations
          t1,t2:integer
          D : array (range,range) of real
        end-declarations

        CumulDemand(d,D,NT)
        ! modified 30/4/04: added if condition
        if(2 <=Tk and Tk <= NT) then
            t1:=2-Tk
            repeat
              t1+=Tk-1
              t2:=minlist(NT,t1+Tk+Tk-3)
              XFormWWCCB(s,r,y,D,C,t1,t2,MC)
            until (t2>=NT)
        end-if
    end-procedure
    """
    s[0], d = NetDemand(s[0], d, NT)

    # CumulDemand(d,D,NT)
    D = {}
    CumulDemand(d, D, NT)
    if 2 <= Tk <= NT:
        t1 = 2-Tk
        while True:
            t1 += Tk-1
            t2 = min(NT, t1+Tk+Tk-3)
            newprefix = prefix+"_{0}_{1}_".format(t1,t2)
            XFormWWCCB2(model, s, r, y, D, C, t1, t2, newprefix)
            if t2 >= NT:
                break


def XFormLSU1(model, s, x, y, d, NT, Tk, prefix=""):
    """
    Multi-commodity for LS-U

    procedure XFormLSU1(
        s : array (range) of linctr,
        x : array (range) of linctr,
        y : array (range) of linctr,
        d : array (range) of real,
        NT : integer,
        Tk : integer,
        MC : integer)

        declarations
            MUC,YC: array (1..NT,range) of linctr
            XC,SC: array (1..NT) of linctr
            xx:dynamic array (1..NT,1..NT) of mpvar
            xs:dynamic array (0..NT-1,1..NT) of mpvar
        end-declarations

        forall(k in 1..NT,t in maxlist(1,k-Tk+1)..k) create(xx(t,k))
        forall(k in 1..NT,t in maxlist(1,k-Tk+1)..k) create(xs(t-1,k))

        forall (k in 1..NT,t in maxlist(1,k-Tk+1)..k) MUC(t,k):=
            xx(t,k)+xs(t-1,k)=if(t=k,d(t),xs(t,k))
        forall (t in 1..NT) XC(t):=x(t)>=sum(k in t..NT) xx(t,k)
        forall (t in 1..NT) SC(t):=s(t-1)>=sum(k in t..NT) xs(t-1,k)
        forall (k in 1..NT,t in maxlist(1,k-Tk+1)..k) YC(t,k):=
            d(k)*y(t)>=xx(t,k)
        if MC=1 then
            forall (k in 1..NT,t in maxlist(1,k-Tk+1)..k)
            setmodcut(YC(t,k))
        end-if
    end-procedure
    """
    s[0], d = NetDemand(s[0], d, NT)

    def xxvar(i, j):
        return prefix+"xx_{0}_{1}".format(i, j)

    def xsvar(i, j):
        return prefix+"xs_{0}_{1}".format(i, j)

    # xx:dynamic array (1..NT,1..NT) of mpvar
    # xs:dynamic array (0..NT-1,1..NT) of mpvar
    # forall(k in 1..NT,t in maxlist(1,k-Tk+1)..k) create(xx(t,k))
    # forall(k in 1..NT,t in maxlist(1,k-Tk+1)..k) create(xs(t-1,k))
    for k in mrange(1, NT):
        for t in mrange(max(1, k-Tk+1), k):
            model.add_var(name=xxvar(t, k), lb=0)
            model.add_var(name=xsvar(t-1, k), lb=0)

    # forall (k in 1..NT,t in maxlist(1,k-Tk+1)..k) MUC(t,k) :=
    # xx(t,k)+xs(t-1,k)=if(t=k,d(t),xs(t,k))
    for k in mrange(1, NT):
        for t in mrange(max(1, k-Tk+1), k):
            lhs = [xxvar(t, k), xsvar(t-1, k)]
            rhs = d[t] if t == k else xsvar(t, k)
            model.add_con(lhs, "=", rhs)

    # forall (t in 1..NT) XC(t) :=
    # x(t)>=sum(k in t..NT) xx(t,k)
    for t in mrange(1, NT):
        rhs = [xxvar(t, k) for k in mrange(t, NT)]
        model.add_con(x[t], ">=", rhs)

    # forall (t in 1..NT) SC(t) :=
    # s(t-1)>=sum(k in t..NT) xs(t-1,k)
    for t in mrange(1, NT):
        rhs = [xsvar(t-1, k) for k in mrange(t, NT)]
        model.add_con(s[t-1], ">=", rhs)

    # forall (k in 1..NT,t in maxlist(1,k-Tk+1)..k) YC(t,k) :=
    # d(k)*y(t)>=xx(t,k)
    for k in mrange(1, NT):
        for t in mrange(max(1, k-Tk+1), k):
            model.add_con((d[k], y[t]), ">=", xxvar(t, k))


def XFormLSU2(model, s, x, y, d, NT, Tk, prefix=""):
    """
    Shortest path for LS-U

    procedure XFormLSU2(
        s : array (range) of linctr,
        x : array (range) of linctr,
        y : array (range) of linctr,
        d : array (range) of real,
        NT : integer,
        Tk : integer,
        MC : integer)

        declarations
            X,Y: array (1..NT) of linctr
            SP1,SP2: array (0..NT+1) of linctr
            S: array (0..NT-1) of linctr
            u:dynamic array (0..NT,0..NT) of mpvar
            v1,v2,w:dynamic array (0..NT) of mpvar
            D : array (range,range) of real
        end-declarations

        CumulDemand(d,D,NT)
        forall(t in 1..NT-Tk+1) create(w(t))
        forall(t in 0..NT-Tk+1) create(v1(t))
        forall(t in Tk-1..NT) create(v2(t))
        forall(i in 0..NT, j in i..minlist(i+Tk-2,NT)) create(u(i,j))

        forall (t in 0..NT+1) SP1(t):=
            if(t>=1,sum(i in 0..t-1) u(i,t-1)+v2(t-1),1) =
            if (t<=NT,sum(i in t..NT) u(t,i)+v1(t),1)
        forall (t in 1..NT-Tk+2) SP2(t):=
            v1(t-1)+if(t>1,w(t-1),0)=if(t<NT-Tk+2,w(t),0)+v2(t+Tk-2)
        forall (t in 1..NT) X(t):=
            x(t)>=sum(i in t..NT) D(t,i)*u(t,i)+D(t,t+Tk-1)*v1(t)
        forall (t in 1..NT) Y(t):=
            y(t)>=sum(i in t..NT|D(t,i)>0) u(t,i)+if(D(t,t+Tk-1)>0,v1(t),0)
        forall (t in 0..NT-1) S(t):=
            s(t) >=
            sum(i in 0..t,j in t+1..NT) D(t+1,j)*u(i,j)+
            if(t<=NT-Tk,D(t+1,t+Tk)*w(t+1),0)+
            sum(i in t+1..minlist(NT,t+Tk-1))D(t+1,i)*v2(i)
    ! Ignore the value of MC

    end-procedure
    """
    s[0], d = NetDemand(s[0], d, NT)

    # CumulDemand(d,D,NT)
    D = {}
    CumulDemand(d, D, NT)

    def v1var(i):
        if i > NT-Tk+1:  # possible bug: undefined variable
            return 0
        return prefix+"v1_{0}".format(i)

    def v2var(i):
        if i < Tk-1:  # possible bug: undefined variable
            return 0
        return prefix+"v2_{0}".format(i)

    def wvar(i):
        return prefix+"w_{0}".format(i)

    def uvar(i, j):
        if j > min(i+Tk-2, NT):
            return 0
        return prefix+"u_{0}_{1}".format(i, j)

    # v1,v2,w:dynamic array (0..NT) of mpvar
    # forall(t in 1..NT-Tk+1) create(w(t))
    # forall(t in 0..NT-Tk+1) create(v1(t))
    # forall(t in Tk-1..NT) create(v2(t))
    for t in mrange(1, NT-Tk+1):
        model.add_var(name=wvar(t), lb=0)
    for t in mrange(0, NT-Tk+1):  # possible bug: NT or NT-Tk+1?
        model.add_var(name=v1var(t), lb=0)
    for t in mrange(Tk-1, NT):  # possible bug: 0 or Tk-1?
        model.add_var(name=v2var(t), lb=0)

    # u:dynamic array (0..NT,0..NT) of mpvar
    # forall(i in 0..NT, j in i..minlist(i+Tk-2,NT)) create(u(i,j))
    for i in mrange(0, NT):
        for j in mrange(i, min(i+Tk-2, NT)):  # possible bug: i+Tk or i+Tk-2?
            model.add_var(name=uvar(i, j), lb=0)

    # forall (t in 0..NT+1) SP1(t):=
    #   if(t>=1,sum(i in 0..t-1) u(i,t-1)+v2(t-1),1) =
    #   if (t<=NT,sum(i in t..NT) u(t,i)+v1(t),1)
    for t in mrange(0, NT+1):
        if t >= 1:
            lhs = []
            for i in mrange(0, t-1):
                lhs.append(uvar(i, t-1))
                lhs.append(v2var(t-1))
        else:
            lhs = 1
        if t <= NT:
            rhs = []
            for i in mrange(t, NT):
                rhs.append(uvar(t, i))
                rhs.append(v1var(t))
        else:
            rhs = 1
        model.add_con(lhs, "=", rhs)

    # forall (t in 1..NT-Tk+2) SP2(t):=
    # v1(t-1)+if(t>1,w(t-1),0)=if(t<NT-Tk+2,w(t),0)+v2(t+Tk-2)
    for t in mrange(1, NT-Tk+2):
        lhs = [v1var(t-1)]
        if t > 1:
            lhs.append(wvar(t-1))
        rhs = [v2var(t+Tk-2)]
        if t < NT-Tk+2:
            rhs.append(wvar(t))
        model.add_con(lhs, "=", rhs)

    # forall (t in 1..NT) X(t):=
    # x(t)>=sum(i in t..NT) D(t,i)*u(t,i)+D(t,t+Tk-1)*v1(t)
    for t in mrange(1, NT):
        rhs = []
        for i in mrange(t, NT):
            rhs.append((D[t, i], uvar(t, i)))
            # possible bug: t+Tk-1 or min(t+Tk-1, NT)?
            if t+Tk-1 <= NT:
                rhs.append((D[t, t+Tk-1], v1var(t)))
        model.add_con(x[t], ">=", rhs)

    # forall (t in 1..NT) Y(t):=
    # y(t)>=sum(i in t..NT|D(t,i)>0) u(t,i)+if(D(t,t+Tk-1)>0,v1(t),0)
    for t in mrange(1, NT):
        rhs = []
        for i in mrange(t, NT):
            if D[t, i] > 0:
                rhs.append(uvar(t, i))
                # possible bug: min(t+Tk-1, NT) or t+Tk-1?
                if t+Tk-1 <= NT and D[t, t+Tk-1] > 0:
                    rhs.append(v1var(t))
        model.add_con(y[t], ">=", rhs)

    # forall (t in 0..NT-1) S(t):=
    #   s(t) >=
    #   sum(i in 0..t,j in t+1..NT) D(t+1,j)*u(i,j)+
    #   if(t<=NT-Tk,D(t+1,t+Tk)*w(t+1),0)+
    #   sum(i in t+1..minlist(NT,t+Tk-1))D(t+1,i)*v2(i)
    for t in mrange(0, NT-1):
        rhs = []
        for i in mrange(0, t):
            for j in mrange(t+1, NT):
                rhs.append((D[t+1, j], uvar(i, j)))
            if t <= NT-Tk:
                rhs.append((D[t+1, t+Tk], wvar(t+1)))
            for i in mrange(t+1, min(NT, t+Tk-1)):
                rhs.append((D[t+1, i], v2var(i)))
        model.add_con(s[t], ">=", rhs)


def XFormLSU(model, s, x, y, d, NT, Tk, prefix=""):
    """
    LS-U

    procedure XFormLSU(
        s : array (range) of linctr,
        x : array (range) of linctr,
        y : array (range) of linctr,
        d : array (range) of real,
        NT : integer,
        Tk : integer,
        MC : integer)

     XFormLSU1(s,x,y,d,NT,Tk,MC)
    end-procedure
    """
    XFormLSU1(model, s, x, y, d, NT, Tk, prefix)


def XFormLSUBMC(model, s, r, x, y, d, NT, Tk, prefix=""):
    """
    procedure XFormLSUBMC(
        s : array (range) of linctr,
        r : array (range) of linctr,
        x : array (range) of linctr,
        y : array (range) of linctr,
        d : array (range) of real,
        NT : integer,
        Tk : integer,
        MC : integer)

        declarations
            QC,Y: array (1..NT,range) of linctr
            X: array (1..NT) of linctr
            S,R: array (0..NT) of linctr
            xx:dynamic array (1..NT,1..NT) of mpvar
            xs,xr:dynamic array (0..NT,1..NT) of mpvar
        end-declarations

        forall(k in 1..NT,t in maxlist(1,k-Tk+1)..minlist(NT,k+Tk-1))
            create(xx(t,k))
        forall(k in 1..NT,t in maxlist(1,k-Tk+1)..k) create(xs(t-1,k))
        forall(k in 1..NT,t in k..minlist(NT,k+Tk-1)) create(xr(t,k))

        forall (k in 1..NT,t in maxlist(1,k-Tk+1)..k-1)
            QC(t,k):=xx(t,k)+xs(t-1,k)=xs(t,k)
        forall (k in 1..NT,t in k+1..minlist(NT,k+Tk-1))
            QC(t,k):=xx(t,k)+xr(t,k)=xr(t-1,k)
        forall (k in 1..NT)
            QC(k,k):=xx(k,k)+xs(k-1,k)+xr(k,k)=d(k)
        forall (t in 1..NT) X(t):=x(t)>=sum(k in 1..NT) xx(t,k)
        forall (t in 0..NT) S(t):=s(t)>=sum(k in t+1..NT) xs(t,k)
        forall (t in 0..NT) R(t):=r(t)>=sum(k in 1..t) xr(t,k)
        forall (k in 1..NT,t in maxlist(1,k-Tk+1)..minlist(NT,k+Tk-1))
            Y(t,k):=d(k)*y(t)>=xx(t,k)
    end-procedure
    """
    s[0], d = NetDemand(s[0], d, NT)

    def xxvar(i, j):
        return prefix+"xx_{0}_{1}".format(i, j)

    def xsvar(i, j):
        return prefix+"xs_{0}_{1}".format(i, j)

    def xrvar(i, j):
        return prefix+"xr_{0}_{1}".format(i, j)

    # xx:dynamic array (1..NT,1..NT) of mpvar
    # forall(k in 1..NT,t in maxlist(1,k-Tk+1)..minlist(NT,k+Tk-1))
    # create(xx(t,k))
    for k in mrange(1, NT):
        for t in mrange(max(1, k-Tk+1), min(NT, k+Tk-1)):
            model.add_var(name=xxvar(t, k), lb=0)

    # xs,xr:dynamic array (0..NT,1..NT) of mpvar
    # forall(k in 1..NT,t in maxlist(1,k-Tk+1)..k) create(xs(t-1,k))
    for k in mrange(1, NT):
        for t in mrange(max(1, k-Tk+1), k):
            model.add_var(name=xsvar(t-1, k), lb=0)

    # forall(k in 1..NT,t in k..minlist(NT,k+Tk-1)) create(xr(t,k))
    for k in mrange(1, NT):
        for t in mrange(k, min(NT, k+Tk-1)):
            model.add_var(name=xrvar(t, k), lb=0)

    # forall (k in 1..NT,t in maxlist(1,k-Tk+1)..k-1) QC(t,k) :=
    # xx(t,k)+xs(t-1,k)=xs(t,k)
    for k in mrange(1, NT):
        for t in mrange(max(1, k-Tk+1), k-1):
            model.add_con([xxvar(t, k), xsvar(t-1, k)], "=", xsvar(t, k))

    # forall (k in 1..NT,t in k+1..minlist(NT,k+Tk-1)) QC(t,k) :=
    # xx(t,k)+xr(t,k)=xr(t-1,k)
    for k in mrange(1, NT):
        for t in mrange(k+1, min(NT, k+Tk-1)):
            model.add_con([xxvar(t, k), xrvar(t, k)], "=", xrvar(t-1, k))

    # forall (k in 1..NT) QC(k,k) :=
    # xx(k,k)+xs(k-1,k)+xr(k,k)=d(k)
    for k in mrange(1, NT):
        model.add_con([xxvar(k, k), xsvar(k-1, k), xrvar(k, k)], "=", d[k])

    # forall (t in 1..NT) X(t) :=
    # x(t)>=sum(k in 1..NT) xx(t,k)
    for t in mrange(1, NT):
        model.add_con(x[t], ">=", [xxvar(t, k) for k in mrange(1, NT)])

    # forall (t in 0..NT) S(t) :=
    # s(t)>=sum(k in t+1..NT) xs(t,k)
    for t in mrange(0, NT):
        model.add_con(s[t], ">=", [xsvar(t, k) for k in mrange(t+1, NT)])

    # forall (t in 0..NT) R(t) :=
    # r(t)>=sum(k in 1..t) xr(t,k)
    for t in mrange(0, NT):
        if t >= 1:
            lhs = r[t]  # possible bug: no r[0]
        else:
            lhs = 0
        model.add_con(lhs, ">=", [xrvar(t, k) for k in mrange(1, t)])

    # forall (k in 1..NT,t in maxlist(1,k-Tk+1)..minlist(NT,k+Tk-1)) Y(t,k) :=
    # d(k)*y(t)>=xx(t,k)
    for k in mrange(1, NT):
        for t in mrange(max(1, k-Tk+1), min(NT, k+Tk-1)):
            model.add_con((d[k], y[t]), ">=", xxvar(t, k))


def XFormLSUB(model, s, r, x, y, d, NT, Tk, prefix=""):
    """
    LS-U-B

    procedure XFormLSUB(
        s : array (range) of linctr,
        r : array (range) of linctr,
        x : array (range) of linctr,
        y : array (range) of linctr,
        d : array (range) of real,
        NT : integer,
        Tk : integer,
        MC : integer)

     XFormLSUBMC(s,r,x,y,d,NT,Tk,MC)

    end-procedure
    """
    XFormLSUBMC(model, s, r, x, y, d, NT, Tk, prefix)


def XFormLSUSC(model, s, x, y, z, d, NT, Tk, prefix=""):
    """
    LS-U-SC

    procedure XFormLSUSC(
        s: array(range) of linctr,
        x: array(range) of linctr,
        y: array(range) of linctr,
        z: array(range) of linctr,
        d: array(range) of real,
        NT: integer,
        Tk: integer,
        MC: integer)

    declarations
        w: array(range,range) of mpvar
    end-declarations

    forall(u in 1..NT,t in u..NT)do
    create(w(u,t))
    end-do

    forall(t in 1..NT)
    sum(u in 1..t)w(u,t)=1

    forall(t in 1..NT, k in 1..t)
    sum(u in k..t)w(u,t)<= y(k)+ if(k<t,sum(u in k+1..t)z(u),0)

    forall(u in 1..NT-1,t in u..NT-1)
    w(u,t)>=w(u,t+1)

    forall(t in 1..NT)do
    w(t,t)<=y(t)
    x(t)=sum(k in t..NT)d(k)*w(t,k)
    end-do

    end-procedure
    """
    s[0], d = NetDemand(s[0], d, NT)

    # w: array(range,range) of mpvar
    def wvar(i, j):
        return prefix+"w_{0}_{1}".format(i, j)

    # forall(u in 1..NT,t in u..NT) create(w(u,t))
    for u in mrange(1, NT):
        for t in mrange(u, NT):
            model.add_var(name=wvar(u, t), lb=0)

    # forall(t in 1..NT) sum(u in 1..t)w(u,t)=1
    for t in mrange(1, NT):
        lhs = [wvar(u, t) for u in mrange(1, t)]
        model.add_con(lhs, "<=", 1)  # possible bug: = or <=?

    # forall(t in 1..NT, k in 1..t)
    # sum(u in k..t)w(u,t)<= y(k)+ if(k<t,sum(u in k+1..t)z(u),0)
    for t in mrange(1, NT):
        for k in mrange(1, t):
            lhs = [wvar(u, t) for u in mrange(k, t)]
            rhs = [y[k]]+[z[u] for u in mrange(k+1, t)]
            model.add_con(lhs, "<=", rhs)

    # forall(u in 1..NT-1,t in u..NT-1)
    # w(u,t)>=w(u,t+1)
    for u in mrange(1, NT-1):
        for t in mrange(u, NT-1):
            model.add_con(wvar(u, t), ">=", wvar(u, t+1))

    # forall(t in 1..NT) do
    #   w(t,t)<=y(t)
    #   x(t)=sum(k in t..NT)d(k)*w(t,k)
    # end-do
    for t in mrange(1, NT):
        model.add_con(wvar(t, t), "<=", y[t])
        rhs = [(d[k], wvar(t, k)) for k in mrange(t, NT)]
        model.add_con(x[t], "<=", rhs)


def XFormLSUSCB(model, s, x, y, z, w, d, NT, Tk, prefix=""):
    """
    LS-U-SC-B

    procedure XFormLSUSCB(
        s: array(range) of linctr,
        !r: array(range) of linctr,
        x: array(range) of linctr,
        y: array(range) of linctr,
        z: array(range) of linctr,
        w: array(range) of linctr,
        d: array(range) of real,
        NT: integer,
        Tk: integer,
        MC: integer)

    declarations
        v: array(range,range) of mpvar
    end-declarations

    forall(u in 1..NT,t in 1..NT)do
    create(v(u,t))
    end-do

    forall(t in 1..NT)
    sum(u in 1..NT)v(u,t)=1

    !forall(t in 1..NT, k in 1..t)
    !sum(u in k..t)v(u,t)<= y(k)+ if(k<t,sum(u in k+1..t)z(u),0)

    !
    forall(k in 1..NT, u in maxlist(1,k-Tk)..k,t in k..minlist(k+Tk,NT))
    sum(i in u..t)v(i,k)<= y(k)+ if(t>k,sum(i in k+1..t)z(i),0)+
            if(u<k,sum(i in u..k-1)w(i),0)
    !)


    forall(u in 1..NT-1,t in u..NT-1)
    v(u,t)>=v(u,t+1)

    forall(u in 2..NT,t in 1..u)
    v(u,t)>=v(u,t-1)

    forall(t in 1..NT)do
    v(t,t)<=y(t)
    x(t)=sum(k in 1..NT)d(k)*v(t,k)
    end-do

    forall(t in 1..NT-1)
    s(t)=sum(u in 1..t,k in t+1..NT)d(k)*v(u,k)

    end-procedure

    + some minor modifications to handle variable s[0]
    """
    s[0], d = NetDemand(s[0], d, NT)

    # v: array(range,range) of mpvar
    def vvar(i, j):
        return prefix+"v_{0}_{1}".format(i, j)

    # forall(u in 1..NT,t in 1..NT) create(v(u,t))
    for u in mrange(0, NT):  # possible bug: 0 or 1?
        for t in mrange(0, NT):  # possible bug: 0 or 1?
            model.add_var(name=vvar(u, t), lb=0)

    # forall(t in 1..NT) sum(u in 1..NT)v(u,t)=1
    for t in mrange(1, NT):
        lhs = [vvar(u, t) for u in mrange(0, NT)]  # possible bug: 0 or 1?
        model.add_con(lhs, "<=", 1)  # possible bug: = or <=?

    # forall(k in 1..NT, u in maxlist(1,k-Tk)..k,t in k..minlist(k+Tk,NT))
    # sum(i in u..t)v(i,k)<= y(k)+ if(t>k,sum(i in k+1..t)z(i),0)+
    #         if(u<k,sum(i in u..k-1)w(i),0)
    for k in mrange(1, NT):
        for u in mrange(max(0, k-Tk), k):  # possible bug: 0 or 1?
            for t in mrange(k, min(k+Tk, NT)):
                lhs = [vvar(i, k) for i in mrange(u, t)]
                rhs = [y[k]]
                rhs += [z[i] for i in mrange(k+1, t) if i > 0]
                rhs += [w[i] for i in mrange(u, k-1) if i > 0]
                model.add_con(lhs, "<=", rhs)

    # forall(u in 1..NT-1,t in u..NT-1) v(u,t)>=v(u,t+1)
    for u in mrange(1, NT-1):  # possible bug: 0 or 1?
        for t in mrange(u, NT-1):
            model.add_con(vvar(u, t), ">=", vvar(u, t+1))

    # forall(u in 2..NT,t in 1..u) v(u,t)>=v(u,t-1)
    for u in mrange(2, NT):
        for t in mrange(1, u):
            model.add_con(vvar(u, t), ">=", vvar(u, t-1))

    # forall(t in 1..NT) do
    #   v(t,t)<=y(t)
    #   x(t)=sum(k in 1..NT)d(k)*v(t,k)
    # end-do
    for t in mrange(1, NT):
        model.add_con(vvar(t, t), "<=", y[t])
        rhs = [(d[k], vvar(t, k)) for k in mrange(1, NT)]
        model.add_con(x[t], "=", rhs)

    # forall(t in 1..NT-1) s(t)=sum(u in 1..t,k in t+1..NT)d(k)*v(u,k)
    for t in mrange(1, NT-1):
        rhs = [
            (d[k], vvar(u, k))
            for u in mrange(0, t)  # possible bug: 0 or 1?
            for k in mrange(t+1, NT)
        ]
        model.add_con(s[t], ">=", rhs)  # possible bug: >= or =?


def XFormDLSICC(model, s0, y, d, C, NT, Tk, prefix=""):
    """
    DLSI-CC

    procedure XFormDLSICC(
        s : linctr,
        y : array (range) of linctr,
        d : array (range) of real,
        C : real,
        NT : integer,
        Tk : integer,
        MC : integer)

        declarations
            ws: array(range) of mpvar
            gs: array(range) of real
            ds: mpvar
            XS,XW: linctr
            XKT:array (1..NT) of linctr
            D : array (range) of real
        end-declarations

        CumulDemand0(d,D,NT)

        forall(t in 1..minlist(NT,Tk)) create(ws(t))

        forall(t in 1..minlist(NT,Tk)) do
            gs(t):=D(t)-C*floor(D(t)/C)
        end-do

        XS:=s>=C*ds+sum(i in 1..minlist(NT,Tk))gs(i)*ws(i)
        XW:=sum(i in 1..minlist(NT,Tk)) ws(i)<=1
        forall (t in 1..minlist(NT,Tk))
            XKT(t):= ds+sum(i in 1..t)y(i)+
                       sum(i in 1..minlist(NT,Tk)|gs(i)>=gs(t))ws(i) >=
                       floor(D(t)/C)+1
                       !ceil(D(t)/C)
    end-procedure
    """
    s0, d = NetDemand(s0, d, NT)

    def wsvar(i):
        return prefix+"ws_{0}".format(i)

    def dsvar():
        return prefix+"ds"

    # CumulDemand0(d,D,NT)
    D = {}
    CumulDemand0(d, D, NT)

    # ds: mpvar
    model.add_var(name=dsvar(), lb=0)

    # forall(t in 1..minlist(NT,Tk)) create(ws(t))
    for t in mrange(1, min(NT, Tk)):
        model.add_var(name=wsvar(t), lb=0)

    # forall(t in 1..minlist(NT,Tk)) do
    #    gs(t):=D(t)-C*floor(D(t)/C)
    # end-do
    gs = {}
    for t in mrange(1, min(NT, Tk)):
        gs[t] = D[t] - C*floor(D[t]/C)

    # XS:=s>=C*ds+sum(i in 1..minlist(NT,Tk))gs(i)*ws(i)
    model.add_con(
        s0, ">=",
        [(C, dsvar())]+[(gs[i], wsvar(i)) for i in mrange(1, min(NT, Tk))]
    )

    # XW:=sum(i in 1..minlist(NT,Tk)) ws(i)<=1
    model.add_con([wsvar(i) for i in mrange(1, min(NT, Tk))], "<=", 1)

    # forall (t in 1..minlist(NT,Tk)) XKT(t) :=
    #   ds+sum(i in 1..t)y(i)+
    #   sum(i in 1..minlist(NT,Tk)|gs(i)>=gs(t))ws(i) >= floor(D(t)/C)+1
    for t in mrange(1, min(NT, Tk)):
        lhs = [dsvar()]
        lhs += [y[i] for i in mrange(1, t)]
        lhs += [wsvar(i) for i in mrange(1, min(NT, Tk)) if gs[i] >= gs[t]]
        model.add_con(lhs, ">=", floor(D[t]/C)+1)


def XFormDLSICCB(model, s0, r, y, d, C, NT, Tk, prefix=""):
    """
    DLSI-CC-B

    procedure XFormDLSICCB(
        s : linctr,
        r : array (range) of linctr,
        y : array (range) of linctr,
        d : array (range) of real,
        C : real,
        NT : integer,
        Tk : integer,
        MC : integer)

        declarations
        Tkk: integer
        end-declarations
        Tkk:=minlist(NT,Tk)


        declarations
            a: array(0..Tkk) of mpvar
            z: array(0..Tkk) of linctr
            f: array(0..Tkk,0..Tkk) of real
            X1,X2:array(0..Tkk,0..Tkk) of linctr
            X3,X4:array(1..Tkk) of linctr
            D : array (1..Tkk) of real
        end-declarations

        CumulDemand0(d,D,Tkk)
        f(0,0):=0
        forall(j in 1..Tkk) f(j,0):=D(j)/C-floor(D(j)/C)
        forall(j in 1..Tkk,l in 0..Tkk|j<>l)
            f(j,l):=f(j,0)-f(l,0)+if(f(j,0)<f(l,0),1,0)

        forall(j in 1..Tkk) z(j):=sum(i in 1..j) y(i) - floor(D(j)/C)

        forall (j in 1..Tkk,l in 0..Tkk|f(l,0)>f(j,0))
            X1(j,l):= s+r(j)+C*f(j,l)*z(j) >= C*f(l,0)+a(j)-a(l)
        forall (j in 1..Tkk,l in 0..Tkk|f(l,0)<f(j,0))
            X2(j,l):= r(j)+C*f(j,l)*z(j) >= a(j)-a(l)
        forall (l in 1..Tkk)
            X3(l):= s >= C*f(l,0)+a(0)-a(l)
        forall (j in 1..Tkk)
            X4(j):= s+r(j)+C*z(j) >= C*f(j,0)

    end-procedure
    """
    s0, d = NetDemand(s0, d, NT)

    def zvar(i):
        return prefix+"z_{0}".format(i)

    def avar(i):
        return prefix+"a_{0}".format(i)

    # CumulDemand0(d,D,NT)
    D = {}
    CumulDemand0(d, D, NT)

    # Tkk:=minlist(NT,Tk)
    Tkk = min(NT, Tk)

    # f(0,0):=0
    # forall(j in 1..Tkk) f(j,0):=D(j)/C-floor(D(j)/C)
    f = {}
    f[0, 0] = 0
    for j in mrange(1, Tkk):
        f[j, 0] = D[j]/C-floor(D[j]/C)
    # forall(j in 1..Tkk,l in 0..Tkk|j<>l)
    #   f(j,l):=f(j,0)-f(l,0)+if(f(j,0)<f(l,0),1,0)
    for j in mrange(1, Tkk):
        for l in mrange(0, Tkk):
            if j != l:
                f[j, l] = f[j, 0]-f[l, 0]+(1 if f[j, 0] < f[l, 0] else 0)

    # z: array(0..Tkk) of linctr
    # forall(j in 1..Tkk) z(j):=sum(i in 1..j) y(i) - floor(D(j)/C)
    for j in mrange(1, Tkk):
        model.add_var(name=zvar(j))
        rhs = [y[i] for i in mrange(1, j)]+[-floor(D[j]/C)]
        model.add_con(zvar(j), "=", rhs)

    # a: array(0..Tkk) of mpvar
    for i in mrange(0, Tkk):
        model.add_var(name=avar(i), lb=0)

    # forall (j in 1..Tkk,l in 0..Tkk|f(l,0)>f(j,0)) X1(j,l) :=
    # s+r(j)+C*f(j,l)*z(j) >= C*f(l,0)+a(j)-a(l)
    for j in mrange(1, Tkk):
        for l in mrange(0, Tkk):
            if f[l, 0] > f[j, 0]:
                lhs = [s0, r[j], (C*f[j, l], zvar(j))]
                rhs = [C*f[l, 0], (1, avar(j)), (-1, avar(l))]
                model.add_con(lhs, ">=", rhs)

    # forall (j in 1..Tkk,l in 0..Tkk|f(l,0)<f(j,0)) X2(j,l) :=
    # r(j)+C*f(j,l)*z(j) >= a(j)-a(l)
    for j in mrange(1, Tkk):
        for l in mrange(0, Tkk):
            if f[l, 0] < f[j, 0]:
                lhs = [r[j], (C*f[j, l], zvar(j))]
                rhs = [(1, avar(j)), (-1, avar(l))]
                model.add_con(lhs, ">=", rhs)

    # forall (l in 1..Tkk) X3(l) :=
    # s >= C*f(l,0)+a(0)-a(l)
    for l in mrange(1, Tkk):
        model.add_con(s0, ">=", [C*f[l,0], (1, avar(0)), (-1, avar(l))])

    # forall (j in 1..Tkk) X4(j) :=
    # s+r(j)+C*z(j) >= C*f(j,0)
    for j in mrange(1, Tkk):
        model.add_con([s0, r[j], (C, zvar(j))], ">=", C*f[j, 0])


def XFormDLSCCB(model, r, y, d, C, NT, Tk, prefix=""):
    """
    DLS-CC-B

    procedure XFormDLSCCB(
        r : array (range) of linctr,
        y : array (range) of linctr,
        d : array (range) of real,
        C : real,
        NT : integer,
        Tk : integer,
        MC : integer)

        declarations

            eta: array(1..NT) of integer
            rr: array(1..NT) of real
            Aee:array (1..NT) of linctr
            D : array (range,range) of real
        end-declarations

        CumulDemand(d,D,NT)

        forall(t in 1..NT) do
            eta(t):= ceil(D(1,t)/C)
            rr(t):= D(1,t)-C*floor(D(1,t)/C)
        end-do

        if(Tk>0) then
          forall(t in 1..Tk| D(1,t)>0 and rr(t)<> 0)
          Aee(t):= r(t) +SUM(v in 1..t)rr(t)*y(v)>= rr(t)*eta(t)
        end-if

        if (MC >0 and Tk > 0) then
        forall(t in 1..Tk| D(1,t)>0 and rr(t)<> 0)
        setmodcut(Aee(t))
    end-if
    end-procedure
    """
    # CumulDemand(d,D,NT)
    D = {}
    CumulDemand(d, D, NT)

    # forall(t in 1..NT) do
    #   eta(t):= ceil(D(1,t)/C)
    #   rr(t):= D(1,t)-C*floor(D(1,t)/C)
    # end-do
    eta = {}
    rr = {}
    for t in mrange(1, NT):
        eta[t] = ceil(D[1, t]/C)
        rr[t] = D[1, t]-C*floor(D[1, t]/C)

    # if(Tk>0) then
    #   forall(t in 1..Tk| D(1,t)>0 and rr(t)<> 0)
    #   Aee(t):= r(t) +SUM(v in 1..t)rr(t)*y(v)>= rr(t)*eta(t)
    # end-if
    if Tk > 0:
        for t in mrange(1, Tk):
            if D[1, t] > 0 and rr[t] != 0:
                lhs = [r[t]]+[(rr[t], y[v]) for v in mrange(1, t)]
                model.add_con(lhs, ">=", rr[t]*eta[t])


def XFormDLSCCSC(model, s, y, z, d, NT, Tk, prefix=""):
    """
    DLS-CC-SC

    procedure XFormDLSCCSC(
        s : array (range) of linctr,
        y : array (range) of linctr,
        z : array (range) of linctr,
        d : array (range) of real,
        NT : integer,
        Tk : integer,
        MC: integer)
        ! Modification 4-10-2009
        !Valid for more general integer demands
        !Need to have demands in 0,1

        declarations
            XWW: array (1..NT,range) of linctr
            D : array (range,range) of real
            ! Added 2/10/05
            BA: array(range,range,range) of linctr
        end-declarations

        CumulDemand(d,D,NT)

        ! Changed 4-10-2009
        !forall(t in 1..NT,l in t..NT,p1 in 1..Tk|
        !    t>= l-Tk and d(l)>0 and floor(D(t,l))= p1 and t<= NT+1-p1)
        forall(t in 1..NT,l in t..NT,p1 in 1..minlist(Tk,l-t)|
            t>= l-Tk and d(l)>0 and floor(D(t,l))= p1 and t<= NT+1-p1)
            BA(t,l,p1):=
                IF(t> 1,s(t-1),0)>= D(t,l)-
                SUM(u in t..t+p1-1)y(u)-
                SUM(u in t+1..t+p1-1)(D(u,l)-p1+u-t)*z(u) -
                SUM(u in t+p1..l|t+p1<= l)(D(u,l))*z(u)

        if MC >0 then
            forall(t in 1..NT,l in t..NT,p1 in 1..Tk|
                t>= l-Tk and d(l)>0 and floor(D(t,l))= p1 and t<= NT+1-p1)
                setmodcut(BA(t,l,p1))
        end-if

    end-procedure
    """
    # !Need to have demands in 0,1
    for i in mrange(1, NT):
        assert d[i] in (0, 1)

    # CumulDemand(d,D,NT)
    D = {}
    CumulDemand(d, D, NT)

    # forall(t in 1..NT,l in t..NT,p1 in 1..minlist(Tk,l-t)|
    #   t>= l-Tk and d(l)>0 and floor(D(t,l))= p1 and t<= NT+1-p1) BA(t,l,p1):=
    #     IF(t> 1,s(t-1),0)>= D(t,l)-
    #     SUM(u in t..t+p1-1)y(u)-
    #     SUM(u in t+1..t+p1-1)(D(u,l)-p1+u-t)*z(u) -
    #     SUM(u in t+p1..l|t+p1<= l)(D(u,l))*z(u)
    for t in mrange(1, NT):
        for l in mrange(t, NT):
            for p1 in mrange(1, min(Tk, l-t)):
                if (t >= l-Tk and d[l] > 0 and
                    floor(D[t, l]) == p1 and t <= NT+1-p1):
                    lhs = s[t-1] if t > 1 else 0
                    rhs = [D[t, l]]
                    rhs += [(-1, y[u]) for u in mrange(t, t+p1-1)]
                    rhs += [
                        (-1*(D[u, l]-p1+u-t), z[u])
                        for u in mrange(t+1, t+p1-1)
                    ]
                    rhs += [
                        (-D[u, l], z[u])
                        for u in mrange(t+p1, l)
                    ]
                    model.add_con(lhs, ">=", rhs)
