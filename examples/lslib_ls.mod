$EXEC{
def mrange(a, b):
    return range(a, b+1)

from random import seed, randint
seed(test_seed)

NT = 10
S0 = 0
S0VAR = False
C = randint(5, 10)

if TEST_PROB == "LS_U":
    BACKLOG = False
    CAPACITATED = False
    SUP_COST = 0
    SOFF_COST = 0
    LB = 0
elif TEST_PROB == "LS_U1":
    BACKLOG = False
    CAPACITATED = False
    SUP_COST = 0
    SOFF_COST = 0
    LB = 0
elif TEST_PROB == "LS_U2":
    BACKLOG = False
    CAPACITATED = False
    SUP_COST = 0
    SOFF_COST = 0
    LB = 0
elif TEST_PROB == "LS_U_B":
    BACKLOG = True
    CAPACITATED = False
    SUP_COST = 0
    SOFF_COST = 0
    LB = 0
elif TEST_PROB == "LS_U_SC":
    BACKLOG = False
    CAPACITATED = False
    SUP_COST = 10
    SOFF_COST = 10
    LB = 0
elif TEST_PROB == "LS_U_SCB":
    BACKLOG = True
    CAPACITATED = False
    SUP_COST = 10
    SOFF_COST = 10
    LB = 0
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

if not CAPACITATED:
    C = sum(d)

#print("C =", C)
#print("S0 =", S0)
#print("d =", d)
#print("p =", p)
#print("h =", h)
#print("q =", q)
};

$PARAM[NT]{NT};

$PARAM[C]{C};

$PARAM[L]{LB};

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
#s.t. sNT: s[NT] = 0;

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
    if TEST_PROB == "LS_U":
        LS_U(s, x, y, d, NT)
    elif TEST_PROB == "LS_U1":
        LS_U1(s, x, y, d, NT)
    elif TEST_PROB == "LS_U2":
        LS_U2(s, x, y, d, NT)
    elif TEST_PROB == "LS_U_B":
        LS_U_B(s, r, x, y, d, NT)
    elif TEST_PROB == "LS_U_SC":
        LS_U_SC(s, x, y, z, d, NT)
    elif TEST_PROB == "LS_U_SCB":
        LS_U_SCB(s, x, y, z, w, d, NT)
    else:
        assert False
};
end;
