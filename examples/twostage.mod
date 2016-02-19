/*
Models the two-stage two-dimensional guillotine cutting stock problem
based on a simplified version of Macedo et al. (2010) arc-flow model
*/

$EXEC{
W, H, w, h, b = read_twostage("data/twostage_A2.txt")
hcuts = sorted(set(h))
};

$SET[HS]{hcuts};
$SET[I]{range(len(b))};
$PARAM[b{^I}]{b};

$EXEC{
HS = _sets["HS"]
I = _sets["I"]
};

# Stage 1 (horizontal cuts):
# Z is the number of sheets used
# hbars[h] is the number of horizontal strips of height h cut
var hbars{HS}, >= 0, integer;
$VBP_FLOW[Z]{
    [H],
    [[hc] for hc in hcuts],
    ["hbars[{}]".format(height) for height in HS]
};

# Stage 2 (vertical cuts):
# x[h, i] is the number of items of type i cut from strips of height h
var x{HS, I}, >= 0, integer;
$EXEC{
for height in HS:
    ws = [
        [w[it]] if h[it] == height else [W+1] # '<=' for non-extact
        for it in I
    ]
    xvars = ["x[{},{}]".format(height, it) for it in I]
    VBP_FLOW["^hbars[{}]".format(height)]([W], ws, xvars)
};

minimize obj: Z;
# Demand constraints:
s.t. demand{it in I}: sum{h in HS} x[h, it] >= b[it];
end;
