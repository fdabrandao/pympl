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
$MVP_GRAPH[V, A]{
    instance.Ws,
    instance.ws,
    {(i, j): (i+1, j+1) for i in range(instance.m) for j in range(len(instance.ws[i]))},
    instance.b,
    S="S", Ts=["T{}".format(i+1) for i in range(len(instance.Ws))], LOSS=("LOSS", "ARC")
};
var f{(u, v, i, o) in A}, >= 0, <= (if i != 'LOSS' then b[i] else Infinity);
s.t. flow_con{k in V}:
    sum{(u, v, i, o) in A: v==k} f[u, v, i, o] - sum{(u, v, i, o) in A: u==k} f[u, v, i, o] = 0;
s.t. assocs{it in I}: x[it] = sum{(u, v, i, o) in A: i == it} f[u, v, i, o];
s.t. zvalues{t in T}: Z[t] = f['T'&t, 'S', 'LOSS', 'ARC'];

minimize obj: cost;
s.t. total_cost: cost = sum{t in T} Z[t]*Cs[t];
s.t. demand{i in I}: x[i] >= b[i];
s.t. zub{t in T: Qs[t] != -1}: Z[t] <= Qs[t];
end;
