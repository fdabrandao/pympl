# Book: Production Planning by Mixed Integer Programming
# Consumer Goods Production (pag. 167)
$EXEC{
def mrange(a, b):
    return range(a, b+1)
};
$PARAM[NI]{30};   # number of items
$PARAM[NT]{60};   # number of shifts
$PARAM[NF]{6};    # number of families
$PARAM[C]{20000}; # capacity
$PARAM[FAM]{[4, 1, 2, 1, 2, 1, 2, 5, 3, 1, 2, 4, 1, 2, 4, 5, 3, 6, 1, 2, 4, 5, 3, 1, 1, 2, 2, 4, 4, 1], i0=1};
$PARAM[h]{0.125}; # storage cost
$PARAM[b]{1};     # backlog cost
$PARAM[d{^1..NI, ^1..NT}]{read_table(
    "data/cgpdemand.dat",
    mrange(1, _params['NI']),
    mrange(1, _params['NT']),
    transpose=False
)}; # demand
param cdem{i in 1..NI, t in 1..NT} := sum{u in 1..t} d[i, u];

var y{1..NI, 1..NT}, binary; # production variables
var s{1..NI, 0..NT}, >= 0;   # storage variables
var r{1..NI, 0..NT}, >= 0;   # backlog variables

minimize cost:
    sum{i in 1..NI, t in 1..NT}
        (b * r[i, t] + h * s[i, t]);

s.t. dem_sat{i in 1..NI, t in 1..NT}:
    s[i, t-1] - r[i, t-1] + C*y[i, t] = d[i, t] + s[i, t] - r[i, t];
s.t. s0{i in 1..NI}: s[i, 0] = 0;
s.t. r0{i in 1..NI}: r[i, 0] = 0;
s.t. rNT{i in 1..NI}: r[i, NT] = 0;

s.t. one_at_time{t in 1..NT}: sum{i in 1..NI} y[i, t] = 1;

# Constraints on the sequencing of families (pag. 170)
var phi{1..NF, 1..NT}, binary;
s.t. phi_value{f in 1..NF, t in 1..NT}:
    phi[f, t] = sum{i in 1..NI: FAM[i] == f} y[i, t];
s.t. phi_unique{t in 1..NT}: sum{f in 1..NF} phi[f, t] = 1;
s.t. sequence{f in 2..NF, t in 1..NT-1}:
    phi[f, t] + sum{g in 2..NF: g != f} phi[g, t+1] <= 1;

# Valid inequalies (pag. 170)
/*
s.t. vi1{i in 1..NI, t in 1..NT}:
    r[i, t] >= cdem[i, t] - (C * sum{u in 1..t} y[i, u]);
param frac{i in 1..NI, t in 1..NT} := cdem[i, t]/C-floor(cdem[i, t]/C);
s.t. vi2{i in 1..NI, t in 1..NT: frac[i, t] > 0}:
    r[i, t] >= C * frac[i, t] * (ceil(cdem[i, t]/C) - sum{u in 1..t} y[i, u]);
*/

# Sensitivity Analysis (pag. 172)
/*
param nb{i in 1..NI} := ceil(cdem[i, NT]/C);
param nc{f in 1..NF} := max{i in 1..NI: FAM[i] == f} nb[i];
s.t. minbatches{i in 2..NI: nb[i] in 1..2}: sum{t in 1..NT} y[i, t] <= nb[i];
var z{f in 2..NF, t in 1..NT: nc[f] in 1..2}, binary;
s.t. startup{f in 2..NF, t in 1..NT: nc[f] in 1..2}: z[f, t] >= phi[f, t]-(if t > 1 then phi[f, t-1]);
s.t. campaigns{f in 2..NF: nc[f] in 1..2}: sum{t in 1..NT} z[f, t] <= nc[f];
*/

$EXEC{
NI = _params["NI"]
NT = _params["NT"]
C = _params["C"]
demand = _params["d"]
for i in mrange(1, NI):
    s0 = "s[{},{}]".format(i, 0)
    s = ["s[{},{}]".format(i, t) for t in mrange(1, NT)]
    y = ["y[{},{}]".format(i, t) for t in mrange(1, NT)]
    z = ["z[{},{}]".format(i, t) for t in mrange(1, NT)]
    d = [demand[i, t] for t in mrange(1, NT)]
    r = ["r[{},{}]".format(i, t) for t in mrange(1, NT)]
    #DLSI_CC_B(s0, r, y, d, C, NT)
    DLS_CC_B(r, y, d, C, NT)
};
end;
