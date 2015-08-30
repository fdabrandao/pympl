## LS-LIB: Library of reformulations for Lot-sizing problems

* [Introduction](#introduction)
* [Examples](#examples)
* [Parameters](#parameters)
* [Wagner-Whitin models](#wagner-whitin-models)
  * [$WW_U{...};](#ww_u)
  * [$WW_U_B{...};](#ww_u_b)
  * [$WW_U_SC{...};](#ww_u_sc)
  * [$WW_U_SCB{...};](#ww_u_scb)
  * [$WW_U_LB{...};](#ww_u_lb)
  * [$WW_CC{...};](#ww_cc)
  * [$WW_CC_B{...};](#ww_cc_b)
* [Lot-sizing models](#lot-sizing-models)
  * [$LS_U or LS_U1{...};](#ls_u-or-ls_u1)
  * [$LS_U2{...};](#ls_u2)
  * [$LS_U_B{...};](#ls_u_b)
* [Return to the index](STMTS)

### Introduction

The set of statements presented in this page come from the library of reformulations LS-LIB proposed in Production Planning by Mixed Integer Programming ([Pochet and Wolsey 2006](http://www.springer.com/us/book/9780387299594)). For more details please refer to the book.

### Examples

`bike.mod`

```ampl
# PPbyMIP: A Tiny Planning Model (Section 1.1, pag. 9)
# LS-U Model (4.1)-(4.5) (Section 4.1, pag. 117)
$PARAM[NT]{8};
param p := 100;
param q := 5000;
param h := 5;
param s_ini := 200;
$PARAM[d]{[400, 400, 800, 800, 1200, 1200, 1200, 1200],i0=1};

var x{1..NT}, >= 0;
var y{1..NT}, binary;
var s{0..NT}, >= 0;
param C{t in 1..NT} := sum{tt in t..NT} d[tt]; 
# enough capacity to procude everything => LS-U problem

minimize cost:
    sum{t in 1..NT} (p * x[t] + q * y[t]) + sum{t in 1..NT-1} (h * s[t]);

s.t. dem_sat{t in 1..NT}: s[t-1] + x[t] = d[t] + s[t];
s.t. s0: s[0] = s_ini;
s.t. sNT: s[NT] = 0;
s.t. vub{t in 1..NT}: x[t] <= C[t] * y[t];

$EXEC{
def mrange(a, b):
    return range(a, b+1)

NT = _params["NT"]
demand = _params["d"]

s = ["s[%d]"%(t) for t in mrange(0, NT)]
x = ["x[%d]"%(t) for t in mrange(1, NT)]
y = ["y[%d]"%(t) for t in mrange(1, NT)]
d = [demand[t] for t in mrange(1, NT)]
LS_U(s, x, y, d, NT)
};

solve;
display x;
display y;
display s;
end;
```

`clb.mod`


```ampl
# Consumer Goods Production (pag. 195)
$EXEC{
def mrange(a, b):
    return range(a, b+1)

BACKLOG = True
};

$PARAM[NI]{4}; # number of items
$PARAM[NT]{30}; # number of shifts

# set-up costs for each period:
$PARAM[q]{[100, 100, 100, 9999, 100, 100, 100, 100, 100, 9999,
           100, 100, 100, 100, 100, 100, 100, 100, 9999, 100,
           100, 100, 100, 100, 9999, 100, 100, 100, 100, 100], i0=1};

# production per hour for each item:
$PARAM[a]{[807, 608, 1559, 1622], i0=1};

# storage costs per hour for each item:
$PARAM[h]{[0.0025, 0.0030, 0.0022, 0.0022], i0=1};

$PARAM[g]{50};     # start-up cost
$PARAM[gamma]{50}; # switch-off cost
$PARAM[rho]{2};    # backlog cost/storage cost ratio

$PARAM[L]{7};  # production lower-bound
$PARAM[C]{16}; # production upper-bound

# demand:
$PARAM[d]{read_demand("data/cldemand.dat", _params["NI"], _params["NT"])};

# production time:
var x{1..NI, 1..NT}, >= 0;

# storage variables:
var s{1..NI, 1..NT}, >= 0;

# backlog variables:
var r{1..NI, 1..NT}, ${">= 0" if BACKLOG else "== 0"}$;

# production variables:
var y{1..NI, 1..NT}, binary;

# start-up of item i at the beginning of period t:
var z{1..NI, 1..NT}, binary;

# switch-off of item i at the end of period t:
var w{1..NI, 1..NT}, binary;

minimize cost:
    sum{i in 1..NI, t in 1..NT}
        (h[i]*a[i]*s[i, t] + h[i]*rho*a[i]*r[i, t] +
         q[t]*y[i, t] + g*z[i, t] + gamma*w[i, t]);

s.t. dem_sat{i in 1..NI, t in 1..NT}:
    (if t > 1 then s[i, t-1] - r[i, t-1]) + x[i, t] = d[i, t] + s[i, t] - r[i, t];

s.t. upper_bound{i in 1..NI, t in 1..NT}: x[i, t] <= C*y[i, t];
s.t. lower_bound{i in 1..NI, t in 1..NT}: x[i, t] >= L*y[i, t];

s.t. setups1{i in 1..NI, t in 1..NT}:
    z[i, t] - (if t > 1 then w[i, t-1]) = y[i, t] - (if t > 1 then y[i, t-1]);
s.t. setups2{i in 1..NI, t in 1..NT}:
    z[i, t] <= y[i, t];

s.t. one_at_time{t in 1..NT}: sum{i in 1..NI} y[i, t] <= 1;

$EXEC{
NI = _params["NI"]
NT = _params["NT"]
L = _params["L"]
C = _params["C"]
demand = _params["d"]
for i in mrange(1, NI):
    s = ["s[%d,%d]"%(i, t) for t in mrange(1, NT)]
    x = ["x[%d,%d]"%(i, t) for t in mrange(1, NT)]
    y = ["y[%d,%d]"%(i, t) for t in mrange(1, NT)]
    z = ["z[%d,%d]"%(i, t) for t in mrange(1, NT)]
    d = [demand[i, t] for t in mrange(1, NT)]
    if BACKLOG is False:
        WW_U(s, y, d, NT)
    else:
        r = ["r[%d,%d]"%(i, t) for t in mrange(1, NT)]
        w = ["w[%d,%d]"%(i, t) for t in mrange(1, NT)]
        LS_U_B(s, r, x, y, d, NT)
        WW_U_SCB(s, r, y, z, w, d, NT, Tk=5)
};

solve;
end;
```

#### Parameters

* `NT`- number of periods;
* `s`- list of size `NT` (s0=0) or `NT+1` with the stock variables for each period;
* `r`- list of size `NT` with the backlog variables for each period;
* `y`- list of size `NT` with the set-up variables for each period;
* `z`- list of size `NT` with the start-up variables for each period;
* `w`- list of size `NT` with the switch-off variables for each period;
* `d`- list of size `NT` with the demand for each period;
* `L`- production lower-bound;
* `C`- production capacity;
* `Tk`- approximation parameter (default: `NT`).

For more details please refer to the book Production Planning by Mixed Integer Programming.

### Wagner-Whitin models

#### WW_U
Usage: `$WW_U{s, y, d, NT, Tk=None};`

Description: Basic Wagner-Whitin.

Parameters: see [parameter description](#parameters).

#### WW_U_B
Usage: `$WW_U_B{s, r, y, d, NT, Tk=None};`

Description: Wagner-Whitin and Backlogging.

Parameters: see [parameter description](#parameters).

#### WW_U_SC
Usage: `$WW_U_SC{s, y, z, d, NT, Tk=None};`

Description: Wagner-Whitin and Start-up.

Parameters: see [parameter description](#parameters).

#### WW_U_SCB
Usage: `$WW_U_SCB{s, r, y, z, w, d, NT, Tk=None};`

Description: Wagner-Whitin, Backlogging and Start-up.

Parameters: see [parameter description](#parameters).

#### WW_U_LB
Usage: `$WW_U_LB{s, y, d, L, NT, Tk=None};`

Description: Wagner-Whitin, Constant Lower Bound.

Parameters: see [parameter description](#parameters).

#### WW_CC
Usage: `$WW_CC{s, y, d, C, NT, Tk=None};`

Description: Wagner-Whitin, Constant Capacity.

Parameters: see [parameter description](#parameters).

#### WW_CC_B
Usage: `$WW_CC_B{s, r, y, d, C, NT, Tk=None};`

Description: Wagner-Whitin, Constant Capacity and Backlogging.

Parameters: see [parameter description](#parameters).

### Lot-sizing models

#### LS_U or LS_U1
Usage: `$LS_U{s, x, y, d, NT, Tk=None};` or `LS_U1{s, x, y, d, NT, Tk=None};`

Description: Multi-commodity formulation for LS-U.

Parameters: see [parameter description](#parameters).

#### LS_U2
Usage: `$LS_U2{s, x, y, d, NT, Tk=None};`

Description: Shortest path formulation for LS-U.

Parameters: see [parameter description](#parameters).

#### LS_U_B
Usage: `$LS_U_B{s, r, x, y, d, NT, Tk=None};`

Description: Multi-commodity formulation for LS-U-B.

Parameters: see [parameter description](#parameters).

***
Copyright © Filipe Brandão. All rights reserved.  
E-mail: <fdabrandao@dcc.fc.up.pt>. [[Homepage](http://www.dcc.fc.up.pt/~fdabrandao/)]