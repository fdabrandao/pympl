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
# LS-U (enough capacity to procude everything):
param C{t in 1..NT} := sum{tt in t..NT} d[tt];

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
#LS_U1(s, x, y, d, NT)
#LS_U2(s, x, y, d, NT)
#WW_U(s, y, d, NT)
};

solve;
display x;
display y;
display s;
end;
