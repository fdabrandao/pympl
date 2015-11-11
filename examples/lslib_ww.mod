$EXEC{
def mrange(a, b):
    return range(a, b+1)

from random import seed, randint
seed(test_seed)

NT = 10
S0 = 10
S0VAR = False
C = randint(5, 10)

if TEST_PROB == "WW_U":
    BACKLOG = False
    CAPACITATED = False
    SUP_COST = 0
    SOFF_COST = 0
    LB = 0
elif TEST_PROB == "WW_U_B":
    BACKLOG = True
    CAPACITATED = False
    SUP_COST = 0
    SOFF_COST = 0
    LB = 0
elif TEST_PROB == "WW_U_SC":
    BACKLOG = False
    CAPACITATED = False
    SUP_COST = 10
    SOFF_COST = 0
    LB = 0
elif TEST_PROB == "WW_U_SCB":
    BACKLOG = True
    CAPACITATED = False
    SUP_COST = 10
    SOFF_COST = 10
    LB = 0
elif TEST_PROB == "WW_U_LB":
    BACKLOG = False
    CAPACITATED = False
    SUP_COST = 0
    SOFF_COST = 0
    LB = 2
elif TEST_PROB == "WW_CC":
    BACKLOG = False
    CAPACITATED = True
    SUP_COST = 0
    SOFF_COST = 0
    LB = 0
elif TEST_PROB == "WW_CC_B":
    BACKLOG = True
    CAPACITATED = True
    SUP_COST = 0
    SOFF_COST = 0
    LB = 0
else:
    assert False

d = []
p = []
h = []
b = []
q = []

for i in mrange(1, NT):
    d.append(randint(0, C))
    if i == 1:
        p.append(randint(1, 3))
        h.append(randint(1, 5))
        b.append(h[-1]*2)
        q.append(randint(20, 50))
    else:
        p.append(randint(1, p[-1]))
        h.append(randint(1, h[-1]))
        b.append(h[-1]*2)
        q.append(randint(20, q[-1]))

if not CAPACITATED:
    C = sum(d)

#LB = int(C/2.0)

#print("LB:", LB)
#print("C:", C)
#print("d:", d)
#print("p:", p)
#print("h:", h)
#print("b:", b)
#print("q:", q)
};

$PARAM[NT]{NT};

$PARAM[C]{C};

$PARAM[L]{LB};

$PARAM[sup_cost]{SUP_COST};

$PARAM[soff_cost]{SOFF_COST};

$PARAM[p{^1..NT}]{p, i0=1};

$PARAM[h{^1..NT}]{h, i0=1};

$PARAM[b{^1..NT}]{b, i0=1};

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
        p[t]*x[t] + h[t]*s[t] + b[t]*r[t] + q[t]*y[t] + sup_cost*z[t] + soff_cost*w[t]
    );

s.t. dem_sat{t in 1..NT}:
    s[t-1] + r[t] + x[t]
    =
    d[t] + (if t > 1 then r[t-1]) + s[t];

s.t. s0: s[0] = ${S0}$;
s.t. sNT: s[NT] = 0;
s.t. rNT: r[NT] = 0;

s.t. upper_bound{t in 1..NT}:
    x[t] <= C*y[t];

s.t. lower_bound{t in 1..NT}:
    x[t] >= L*y[t];

s.t. setups1{t in 1..NT}:
    z[t] - (if t > 1 then w[t-1]) = y[t] - (if t > 1 then y[t-1]);
s.t. setups2{t in 1..NT}:
    z[t] <= y[t];

$EXEC{
s = ["s[%d]"%(t) for t in mrange(0, NT)]
if S0VAR is False:
    s[0] = S0
r = ["r[%d]"%(t) for t in mrange(1, NT)]
x = ["x[%d]"%(t) for t in mrange(1, NT)]
y = ["y[%d]"%(t) for t in mrange(1, NT)]
z = ["z[%d]"%(t) for t in mrange(1, NT)]
w = ["w[%d]"%(t) for t in mrange(1, NT)]
d = [_params["d"][t] for t in mrange(1, NT)]
if xform:
    print("test:", TEST_PROB)
    if TEST_PROB == "WW_U":
        WW_U(s, y, d, NT)
    elif TEST_PROB == "WW_U_B":
        WW_U_B(s, r, y, d, NT)
    elif TEST_PROB == "WW_U_SC":
        WW_U_SC(s, y, z, d, NT)
    elif TEST_PROB == "WW_U_SCB":
        WW_U_SCB(s, r, y, z, w, d, NT)
    elif TEST_PROB == "WW_U_LB":
        WW_U_LB(s, y, d, LB, NT)
    elif TEST_PROB == "WW_CC":
        WW_CC(s, y, d, C, NT)
    elif TEST_PROB == "WW_CC_B":
        WW_CC_B(s, r, y, d, C, NT)
        pass
};
end;
