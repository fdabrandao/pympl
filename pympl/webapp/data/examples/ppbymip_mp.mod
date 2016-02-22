# Book: Production Planning by Mixed Integer Programming
# Making and Packing (pag. 422)
$EXEC{
def mrange(a, b):
    return range(a, b+1)
};
$PARAM[NT]{15}; # number of time periods
$SET[IBULK]{range(3)}; # set of bulk products
$SET[IEND]{range(3, 3+15)}; # set of end products
$SET[KBULK]{range(5)}; # set of making machines
$SET[KEND]{range(5, 5+3)}; # set of packing lines
set I := IBULK union IEND;

$EXEC{
NT = _params["NT"]
IBULK = sorted(_sets["IBULK"])
IEND = sorted(_sets["IEND"])
KBULK = sorted(_sets["KBULK"])
KEND = sorted(_sets["KEND"])
};

# association of bulk and end products SUCC[i,j]=1 iff j in succ(i):
$PARAM[SUCC{^IBULK, ^IEND}]{{
    (i, j): 1 if k2 // 5 == k1 else 0
    for k1, i in enumerate(IBULK)
    for k2, j in enumerate(IEND)
}};

# demand forecasts:
$PARAM[D{^IEND, ^1..NT}]{read_table(
    "data/mp_daily_demand.dat",
    IEND,
    mrange(1, NT),
    transpose=True
)};

# bulk initial inventory
$PARAM[s0{^IBULK}]{[600.0, 900.0, 600.0], i0=0};

# feeder rate:
$PARAM[FR{^IBULK}]{[900.0, 800.0, 750.0], i0=0};

# robot rate:
$PARAM[RR{^IEND}]{[328.0, 328.0, 820.0, 410.0, 492.0, 328.0, 328.0, 820.0,
                   410.0, 492.0, 328.0, 328.0, 820.0, 410.0, 492.0], i0=3};

# making production rate:
$PARAM[MPR{^IBULK, ^KBULK}]{read_table(
    "data/mp_making_production_rate.dat",
    IBULK,
    KBULK,
    transpose=True
)};

# packing production rate:
$PARAM[PPR{^IEND, ^KEND}]{read_table(
    "data/mp_packing_production_rate.dat",
    IEND,
    KEND,
    transpose=True
)};

param PR{i in IBULK union IEND, k in KBULK union KEND} :=
    if (i, k) in (IBULK cross KBULK) then MPR[i, k] else
    if (i, k) in (IEND cross KEND) then PPR[i, k] else
    0;

# machine changeover time:
$PARAM[ST{^KBULK union KEND}]{{
    k: 1.5 if k in KBULK else 0.5
    for k in set(KBULK)|set(KEND)
}};

$PARAM[NH]{24};   # working hours per period
$PARAM[NF]{3};    # number of feeders
$PARAM[NR]{6};    # number of robots
$PARAM[RBACK]{8}; # relative backlogging cost

# production lot size:
var x{(i, k) in (IBULK cross KBULK) union (IEND cross KEND), 1..NT: PR[i, k] > 0}, >= 0;

# production set-up:
var y{(i, k) in (IBULK cross KBULK) union (IEND cross KEND), 1..NT: PR[i, k] > 0}, binary;

# machine start-up:
var z{KBULK union KEND, 1..NT}, binary;

# inventory level:
var s{IBULK union IEND, 1..NT}, >= 0;

# backlog level:
var r{IEND, 1..NT}, >= 0;

# number of feeders assigned:
var eta{IBULK, 1..NT}, >= 0, integer;

# number of robots assigned:
var pi{KEND, 1..NT}, >= 0, integer;

minimize inv_back:
    sum{i in IEND, t in 1..NT} r[i, t] + sum{i in IBULK, t in 1..NT} s[i, t]/RBACK;

s.t. dem_sat1{i in IEND, t in 1..NT}:
    (if t > 1 then s[i, t-1]) + r[i, t] + sum{k in KEND: PR[i, k] > 0} x[i, k, t]
    =
    D[i, t] + (if t > 1 then r[i, t-1]) + s[i, t];

s.t. dem_sat2{i in IBULK, t in 1..NT}:
    (if t > 1 then s[i, t-1] else s0[i]) + sum{k in KBULK: PR[i, k] > 0} x[i, k, t]
    =
    sum{k in KEND, j in IEND: SUCC[i, j] == 1 and PR[i, k] > 0} x[j, k, t] + s[i, t];

s.t. vub{(i, k) in (IEND cross KEND) union (IBULK cross KBULK), t in 1..NT: PR[i, k] > 0}:
    x[i, k, t] <= NH*PR[i, k]*y[i, k, t];

s.t. mode{k in KBULK union KEND, t in 1..NT}:
    sum{i in IBULK union IEND: PR[i, k] > 0} y[i, k, t] <= 1;

s.t. start_up{(i, k) in (IEND cross KEND) union (IBULK cross KBULK), t in 1..NT: PR[i, k] > 0}:
    z[k, t] >= y[i, k, t] - (if t > 1 then y[i, k, t-1]);

s.t. capa1{k in KBULK, t in 1..NT}:
    sum{i in IBULK: PR[i, k] > 0} x[i, k, t]/PR[i, k] <= NH - ST[k]*z[k, t];

s.t. capa2{k in KEND, t in 1..NT}:
    sum{i in IEND: PR[i, k] > 0} x[i, k, t]/PR[i, k] <= NH - ST[k]*z[k, t];

s.t. feed_ass{t in 1..NT}:
    sum{i in IBULK} eta[i, t] = NF;

s.t. feed_cap{i in IBULK, t in 1..NT}:
     sum{k in KEND, j in IEND: SUCC[i, j] == 1 and PR[j, k] > 0} x[j, k, t]/FR[i] <= NH * eta[i, t];

s.t. rob_ass{t in 1..NT}:
    sum{k in KEND} pi[k, t] = NR;

s.t. rob_cap{k in KEND, t in 1..NT}:
    sum{i in IEND: PR[i, k] > 0} x[i, k, t]/RR[i] <= NH * pi[k, t];

# Echelon stock reformulation:
var es{i in IBULK, t in 0..NT}, >= 0;
s.t. es_value{i in IBULK, t in 1..NT}: es[i, t] = s[i, t] + sum{j in IEND: SUCC[i, j] == 1} s[j, t];
s.t. es0_value{i in IBULK}: es[i, 0] = s0[i];

var er{i in IBULK, t in 1..NT}, >= 0;
s.t. er_value{i in IBULK, t in 1..NT}: er[i, t] = sum{j in IEND: SUCC[i, j] == 1} r[j, t];

var ax{i in IBULK union IEND, t in 1..NT}, >= 0;
s.t. ax_value1{i in IBULK, t in 1..NT}: ax[i, t] = sum{k in KBULK: PR[i, k] > 0} x[i, k, t]*PR[i, k];
s.t. ax_value2{i in IEND, t in 1..NT}: ax[i, t] = sum{k in KEND: PR[i, k] > 0} x[i, k, t];

var ay{i in IBULK union IEND, t in 1..NT}, >= 0, binary;
s.t. ay_value1{i in IBULK, t in 1..NT}: ay[i, t] = sum{k in KBULK: PR[i, k] > 0} y[i, k, t];
s.t. ay_value2{i in IEND, t in 1..NT}: ay[i, t] = sum{k in KEND: PR[i, k] > 0} y[i, k, t];

s.t. edem_sat1{i in IBULK, t in 1..NT}:
    es[i, t-1] + er[i, t] + ax[i, t]
    =
    sum{j in IEND: SUCC[i, j] == 1} D[j, t] + (if t > 1 then er[i, t-1]) + es[i, t];

s.t. evub{i in IBULK, t in 1..NT}:
    ax[i, t] <= (max{k in KBULK} NH*PR[i,k]) * ay[i, t];

s.t. edem_sat2{i in IEND, t in 1..NT}:
    (if t > 1 then s[i, t-1]) + r[i, t] + ax[i, t] = D[i, t] + (if t > 1 then r[i, t-1]) + s[i, t];

s.t. evub2{i in IEND, t in 1..NT}:
    ax[i, t] <= (max{k in KEND} NH*PR[i,k]) * ay[i, t];

$EXEC{
D = _params["D"]
SUCC = _params["SUCC"]
NH, PPR = _params["NH"], _params["PPR"]
for i in IBULK:
    s = ["es[{},{}]".format(i, t) for t in mrange(0, NT)]
    r = ["er[{},{}]".format(i, t) for t in mrange(1, NT)]
    x = ["ax[{},{}]".format(i, t) for t in mrange(1, NT)]
    y = ["ay[{},{}]".format(i, t) for t in mrange(1, NT)]
    d = [
        sum(D[j, t] for j in IEND if SUCC[i, j] == 1)
        for t in mrange(1, NT)
    ]
    WW_U_B(s, r, y, d, NT, Tk=4)
for i in IEND:
    s = ["s[{},{}]".format(i, t) for t in mrange(1, NT)]
    r = ["r[{},{}]".format(i, t) for t in mrange(1, NT)]
    x = ["ax[{},{}]".format(i, t) for t in mrange(1, NT)]
    y = ["ay[{},{}]".format(i, t) for t in mrange(1, NT)]
    d = [
        D[i, t]
        for t in mrange(1, NT)
    ]
    C = max(NH*PPR[i,k] for k in KEND)
    WW_U_B(s, r, y, d, NT, Tk=8)
    #WW_CC_B(s, r, y, d, C, NT, Tk=6)
};
end;
