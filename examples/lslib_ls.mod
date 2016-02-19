$EXEC{
def mrange(a, b):
    return range(a, b+1)

from random import seed, randint
seed(test_seed)

NT = 10
S0 = 11
S0VAR = False
C = randint(5, 10)

if TEST_PROB == "LS_U":
    BACKLOG = False
    CAPACITATED = False
    SUP_COST = 0
    SOFF_COST = 0
    LB = 0
    SL = 0
    SL_VALUE = 0
elif TEST_PROB == "LS_U1":
    BACKLOG = False
    CAPACITATED = False
    SUP_COST = 0
    SOFF_COST = 0
    LB = 0
    SL = 0
    SL_VALUE = 0
elif TEST_PROB == "LS_U2":
    BACKLOG = False
    CAPACITATED = False
    SUP_COST = 0
    SOFF_COST = 0
    LB = 0
    SL = 0
    SL_VALUE = 0
elif TEST_PROB == "LS_U_B":
    BACKLOG = True
    CAPACITATED = False
    SUP_COST = 0
    SOFF_COST = 0
    LB = 0
    SL = 0
    SL_VALUE = 0
elif TEST_PROB == "LS_U_SC":
    BACKLOG = False
    CAPACITATED = False
    SUP_COST = 10
    SOFF_COST = 10
    LB = 0
    SL = 0
    SL_VALUE = 0
elif TEST_PROB == "LS_U_SCB":
    BACKLOG = True
    CAPACITATED = False
    SUP_COST = 10
    SOFF_COST = 10
    LB = 0
    SL = 0
    SL_VALUE = 0
elif TEST_PROB == "LS_U_SL":
    BACKLOG = False
    CAPACITATED = False
    SUP_COST = 0
    SOFF_COST = 0
    LB = 0
    SL = 10
    SL_VALUE = -1
elif TEST_PROB == "LS_U_SCSL":
    BACKLOG = False
    CAPACITATED = False
    SUP_COST = 10
    SOFF_COST = 10
    LB = 0
    SL = 10
    SL_VALUE = -1
elif TEST_PROB == "LS_U_SCBSL":
    BACKLOG = True
    CAPACITATED = False
    SUP_COST = 10
    SOFF_COST = 10
    LB = 0
    SL = 10
    SL_VALUE = -1
else:
    assert False

d = []
p = []
h = []
q = []
u = []
for i in mrange(1, NT):
    d.append(randint(0, C))
    p.append(randint(1, 3))
    h.append(randint(1, 5))
    q.append(randint(20, 50))
    u.append(randint(0, SL))

if not CAPACITATED:
    C = sum(d)+sum(u)

#LB = int(C/1.0)

#print("C =", C)
#print("S0 =", S0)
#print("d =", d)
#print("u =", u)
#print("p =", p)
#print("h =", h)
#print("q =", q)
};

$PARAM[NT]{NT};

$PARAM[C]{C};

$PARAM[L]{LB};

$PARAM[sup_cost]{SUP_COST};

$PARAM[soff_cost]{SOFF_COST};

$PARAM[sales_value]{SL_VALUE};

$PARAM[p{^1..NT}]{p, i0=1};

$PARAM[h{^1..NT}]{h, i0=1};

$PARAM[q{^1..NT}]{q, i0=1};

$PARAM[d{^1..NT}]{d, i0=1};

$PARAM[u{^1..NT}]{u, i0=1};

var x{1..NT}, >= 0;

var s{0..NT}, >= 0;

var v{i in 1..NT}, >= 0, <= u[i];

var r{1..NT}, >= 0 ${", <= 0" if not BACKLOG else ""}$;

var y{1..NT}, >= 0, <= 1 ${", binary" if not relax else ""}$;

var z{1..NT}, >= 0, <= 1 ${", binary" if not relax else ""}$;

var w{1..NT}, >= 0, <= 1 ${", binary" if not relax else ""}$;

var cost;

minimize obj: cost;

s.t. obj_value:
    cost = sum{t in 1..NT} (
        p[t]*x[t] + h[t]*s[t] + 2*h[t]*r[t] + q[t]*y[t] +
        sup_cost*z[t] + soff_cost*w[t] +
        sales_value*v[t]
    );

s.t. dem_sat{t in 1..NT}:
    s[t-1] + r[t] + x[t]
    =
    d[t] + v[t] + (if t > 1 then r[t-1]) + s[t];

s.t. s0: s[0] = ${S0}$;
#s.t. sNT: s[NT] = ${S0}$;
#s.t. rNT: r[NT] = 10000;

s.t. upper_bound{t in 1..NT}:
    x[t] <= C*y[t];

s.t. lower_bound{t in 1..NT}:
    x[t] >= L*y[t];

s.t. setups1{t in 1..NT}:
    z[t] - (if t > 1 then w[t-1]) = y[t] - (if t > 1 then y[t-1]);
s.t. setups2{t in 1..NT}:
    z[t] <= y[t];

$EXEC{
s = ["s[{}]".format(t) for t in mrange(0, NT)]
if S0VAR is False:
    s[0] = S0
r = ["r[{}]".format(t) for t in mrange(1, NT)]
x = ["x[{}]".format(t) for t in mrange(1, NT)]
y = ["y[{}]".format(t) for t in mrange(1, NT)]
v = ["v[{}]".format(t) for t in mrange(1, NT)]
z = ["z[{}]".format(t) for t in mrange(1, NT)]
w = ["w[{}]".format(t) for t in mrange(1, NT)]
d = [_params["d"][t] for t in mrange(1, NT)]
u = [_params["u"][t] for t in mrange(1, NT)]
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
    elif TEST_PROB == "LS_U_SL":
        LS_U_SL(s, x, y, v, d, u, NT)
    elif TEST_PROB == "LS_U_SCSL":
        LS_U_SCSL(s, x, y, z, v, d, u, NT)
    elif TEST_PROB == "LS_U_SCBSL":
        LS_U_SCBSL(s, r, x, y, z, w, v, d, u, NT)
    else:
        assert False
};
end;
