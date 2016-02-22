# Book: Production Planning by Mixed Integer Programming
# Pigment Sequencing (pag. 466)
$EXEC{
def mrange(a, b):
    return range(a, b+1)

BACKLOG = False # False on the original problem
};

$PARAM[NI]{10}; # number of products
$PARAM[NT]{100}; # number of time periods
$EXEC{
NI = _params["NI"]
NT = _params["NT"]
};

# storage costs per hour for each item:
$PARAM[h]{[10]*10, i0=1};

# relative backlogging cost:
$PARAM[RBACK]{10};

# demand:
$PARAM[d{^1..NI, ^1..NT}]{read_table(
    "data/pigment_dem.dat",
    mrange(1, NI),
    mrange(1, NT),
    transpose=True
)};

# changeover costs:
$PARAM[c{^1..NI, ^1..NI}]{read_table(
    "data/pigment_q.dat",
    mrange(1, NI),
    mrange(1, NI),
    transpose=True
)};

# production lot size:
var x{1..NI, 1..NT}, binary;

# production set-up:
var y{1..NI, 0..NT}, binary;

# inventory level:
var s{1..NI, 1..NT}, >= 0;

# backlog level:
var r{1..NI, 1..NT}, ${">= 0" if BACKLOG else ">= 0, <= 0"}$;

# start-up of item i at the beginning of period t:
var z{1..NI, 1..NT}, binary;

# switch-off of item i at the end of period t:
var w{1..NI, 0..NT}, binary;

# changeover from item i to item j in period t:
var chi{1..NI, 1..NI, 1..NT}, >= 0;

minimize cost:
    sum{i in 1..NI, t in 1..NT} h[i] * s[i, t] +
    sum{i in 1..NI, t in 1..NT} RBACK * h[i] * r[i, t] +
    sum{i in 1..NI, j in 1..NI, t in 1..NT} c[i, j] * chi[i, j, t];

s.t. dem_sat{i in 1..NI, t in 1..NT}:
    (if t > 1 then s[i, t-1]) + r[i, t] + x[i, t]
    =
    d[i, t] + (if t > 1 then r[i, t-1]) + s[i, t];

s.t. vub{i in 1..NI, t in 1..NT}:
    x[i, t] <= y[i, t];

s.t. one_at_time{t in 1..NT}:
    sum{i in 1..NI} y[i, t] = 1;

#s.t. changeovers{i in 1..NI, j in 1..NI, t in 1..NT}:
#    chi[i, j, t] >= y[i, t-1] + y[j, t] - 1;

s.t. changeovers1{j in 1..NI, t in 1..NT}:
    sum{i in 1..NI} chi[i, j, t] = y[j, t];
s.t. changeovers2{i in 1..NI, t in 1..NT}:
    sum{j in 1..NI} chi[i, j, t] = y[i, t-1];
s.t. changeovers3:
    sum{i in 1..NI} y[i, 0] = 1;

s.t. startup1{j in 1..NI, t in 1..NT}:
    chi[j, j, t] = y[j, t-1] - w[j, t-1];
s.t. startup2{j in 1..NI, t in 1..NT}:
    y[j, t] - z[j, t] = chi[j, j, t];

$EXEC{
C = 1
demand = _params["d"]
for i in mrange(1, NI):
    s0 = 0
    s = ["s[{},{}]".format(i, t) for t in mrange(1, NT)]
    y = ["y[{},{}]".format(i, t) for t in mrange(1, NT)]
    z = ["z[{},{}]".format(i, t) for t in mrange(1, NT)]
    d = [demand[i, t] for t in mrange(1, NT)]
    if BACKLOG is False:
        #DLSI_CC(s0, y, d, C, NT) # has no effect?
        DLS_CC_SC(s, y, z, d, C, NT, Tk=15)
    else:
        r = ["r[{},{}]".format(i, t) for t in mrange(1, NT)]
        DLSI_CC_B(s0, r, y, d, C, NT)
        #DLS_CC_B(r, y, d, C, NT) # has no effect?
};
end;
