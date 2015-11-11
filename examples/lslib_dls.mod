$EXEC{
def mrange(a, b):
    return range(a, b+1)

from random import seed, randint
seed(test_seed)

NT = 20
C = randint(5, 10)
S0 = randint(5, 20)
S0 = 10
S0VAR = False

if TEST_PROB == "DLSI_CC":
    BACKLOG = False
    SUP_COST = 0
    SOFF_COST = 0
elif TEST_PROB == "DLSI_CC_B":
    BACKLOG = True
    SUP_COST = 0
    SOFF_COST = 0
elif TEST_PROB == "DLS_CC_B":
    BACKLOG = True
    SUP_COST = 0
    SOFF_COST = 0
    S0 = 0
elif TEST_PROB == "DLS_CC_SC":
    BACKLOG = False
    SUP_COST = 10
    SOFF_COST = 10
    C = 1 # DLS_CC_SC requires 0-1 demands
    S0 = 0
elif TEST_PROB == "DLS_CC_SCU":
    BACKLOG = False
    SUP_COST = 10
    SOFF_COST = 10
    S0 = 0
else:
    assert False

d = []
p = []
h = []
q = []
for i in mrange(1, NT):
    d.append(randint(0, C))
    p.append(randint(1, 3))
    h.append(randint(1, 5))
    q.append(randint(20, 50))

#print("C =", C)
#print("d =", d)
#print("p =", p)
#print("h =", h)
#print("q =", q)
};

$PARAM[NT]{NT};

$PARAM[C]{C};

$PARAM[sup_cost]{SUP_COST};

$PARAM[soff_cost]{SOFF_COST};

$PARAM[p{^1..NT}]{p, i0=1};

$PARAM[h{^1..NT}]{h, i0=1};

$PARAM[q{^1..NT}]{q, i0=1};

$PARAM[d{^1..NT}]{d, i0=1};

var x{1..NT}, >= 0;

var s{0..NT}, >= 0;

var r{1..NT}, >= 0 ${", <= 0" if not BACKLOG else ""}$;

var y{1..NT}, >= 0, <= 1 ${", binary" if not relax else ""}$;

var z{1..NT}, >= 0, <= 1 ${", binary" if not relax else ""}$;

var w{1..NT}, >= 0, <= 1 ${", binary" if not relax else ""}$;

var cost;

minimize obj: cost;

s.t. obj_value:
    cost = sum{t in 1..NT} (
        p[t]*x[t] + h[t]*s[t] + 2*h[t]*r[t] + q[t]*y[t] + sup_cost*z[t] + soff_cost*w[t]
    );

s.t. dem_sat{t in 1..NT}:
    s[t-1] + r[t] + x[t]
    =
    d[t] + (if t > 1 then r[t-1]) + s[t];

s.t. s0: s[0] = ${S0}$;

s.t. upper_bound{t in 1..NT}:
    x[t] = C*y[t];

s.t. setups1{t in 1..NT}:
    z[t] - (if t > 1 then w[t-1]) = y[t] - (if t > 1 then y[t-1]);
s.t. setups2{t in 1..NT}:
    z[t] <= y[t];

$EXEC{
if S0VAR:
    S0 = "s[0]"
s = ["s[%d]"%(t) for t in mrange(1, NT)]
r = ["r[%d]"%(t) for t in mrange(1, NT)]
y = ["y[%d]"%(t) for t in mrange(1, NT)]
z = ["z[%d]"%(t) for t in mrange(1, NT)]
w = ["w[%d]"%(t) for t in mrange(1, NT)]
d = [_params["d"][t] for t in mrange(1, NT)]
if xform:
    print("test:", TEST_PROB)
    if TEST_PROB == "DLSI_CC":
        DLSI_CC(S0, y, d, C, NT)
    elif TEST_PROB == "DLSI_CC_B":
        DLSI_CC_B(S0, r, y, d, C, NT)
    elif TEST_PROB == "DLS_CC_B":
        DLS_CC_B(r, y, d, C, NT)
    elif TEST_PROB == "DLS_CC_SC":
        DLS_CC_SC(s, y, z, d, C, NT)
    elif TEST_PROB == "DLS_CC_SCU":
        DLS_CC_SCU(s, y, z, d, C, NT)
    else:
        assert False
};
end;
