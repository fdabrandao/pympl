# Book: Production Planning by Mixed Integer Programming
# Cleaning Liquids Bottling Line (pag. 167)
$EXEC{
def mrange(a, b):
    return range(a, b+1)

BACKLOG = False # False on original problem
DISCRETE = False # False on the original problem
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
$PARAM[rho]{5};    # backlog cost/storage cost ratio

$PARAM[L]{7};  # production lower-bound
$PARAM[C]{16}; # production upper-bound

# demand:
$PARAM[d{^1..NI, ^1..NT}]{read_table(
    "data/cldemand.dat",
    mrange(1, _params["NI"]),
    mrange(1, _params["NT"]),
    transpose=False
)};

# production time:
var x{1..NI, 1..NT}, >= 0;

# storage variables:
var s{1..NI, 1..NT}, >= 0;

# backlog variables:
var r{1..NI, 1..NT}, ${">= 0" if BACKLOG else ">= 0, <= 0"}$;

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
    (if t > 1 then s[i, t-1]) + r[i, t] + x[i, t]
    =
    d[i, t] + (if t > 1 then r[i, t-1]) + s[i, t];

s.t. upper_bound{i in 1..NI, t in 1..NT}:
    x[i, t] ${"==" if DISCRETE else "<="}$ C*y[i, t];
s.t. lower_bound{i in 1..NI, t in 1..NT}:
    x[i, t] >= L*y[i, t];

#s.t. rNT{i in 1..NI}: r[i, NT] = 0; # not used in the book

s.t. setups1{i in 1..NI, t in 1..NT}:
    z[i, t] - (if t > 1 then w[i, t-1]) = y[i, t] - (if t > 1 then y[i, t-1]);
#s.t. setups2{i in 1..NI, t in 1..NT}:
#    z[i, t] <= y[i, t]; # not used in the book

s.t. one_at_time{t in 1..NT}: sum{i in 1..NI} y[i, t] <= 1;

$EXEC{
NI = _params["NI"]
NT = _params["NT"]
L = _params["L"]
C = _params["C"]
demand = _params["d"]
if DISCRETE is False:
    for i in mrange(1, NI):
        s = ["s[{},{}]".format(i, t) for t in mrange(1, NT)]
        x = ["x[{},{}]".format(i, t) for t in mrange(1, NT)]
        y = ["y[{},{}]".format(i, t) for t in mrange(1, NT)]
        z = ["z[{},{}]".format(i, t) for t in mrange(1, NT)]
        d = [demand[i, t] for t in mrange(1, NT)]
        if BACKLOG is False:
            #WW_U(s, y, d, NT)
            WW_CC(s, y, d, C, NT, Tk=15)
            WW_U_SC(s, y, z, d, NT, Tk=15)
            #LS_U(s, x, y, d, NT)
            #LS_U_SC(s, x, y, z, d, NT) # Not compatible with LB?
            pass
        else:
            r = ["r[{},{}]".format(i, t) for t in mrange(1, NT)]
            w = ["w[{},{}]".format(i, t) for t in mrange(1, NT)]
            #WW_U_B(s, r, y, d, NT)
            #LS_U_B(s, r, x, y, d, NT)
            WW_U_SCB(s, r, y, z, w, d, NT, Tk=15)
            WW_CC_B(s, r, y, d, C, NT, Tk=5)
        #WW_U_LB(s, y, d, L, NT, Tk=15)
else:
   for i in mrange(1, NI):
        s0 = 0
        s = ["s[{},{}]".format(i, t) for t in mrange(1, NT)]
        y = ["y[{},{}]".format(i, t) for t in mrange(1, NT)]
        z = ["z[{},{}]".format(i, t) for t in mrange(1, NT)]
        d = [demand[i, t] for t in mrange(1, NT)]
        if BACKLOG is False:
            DLSI_CC(s0, y, d, C, NT)
            #DLS_CC_SC(s, y, z, d, C, NT)
        else:
            r = ["r[{},{}]".format(i, t) for t in mrange(1, NT)]
            #DLSI_CC_B(s0, r, y, d, C, NT)
            DLS_CC_B(r, y, d, C, NT)
};
end;
