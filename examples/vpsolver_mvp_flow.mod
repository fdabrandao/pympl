$EXEC{
from pyvpsolver import MVP
instance = MVP.from_file("data/instance.mvp")
};
$PARAM[Cs{T}]{instance.Cs, i0=1};
$PARAM[Qs{^T}]{instance.Qs, i0=1};
$PARAM[b{I}]{instance.b, i0=1};

var cost;
var x{I}, >= 0;
var Z{T}, integer, >= 0;
$MVP_FLOW[^Z{T}]{
    instance.Ws, instance.ws,
    ["x[{0}]".format(i+1) for i in range(instance.m)],
    i0=1
};

minimize obj: cost;
s.t. total_cost: cost = sum{t in T} Z[t]*Cs[t];
s.t. demand{i in I}: x[i] >= b[i];
s.t. zub{t in T: Qs[t] != -1}: Z[t] <= Qs[t];
end;
