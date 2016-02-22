$EXEC{
# bin capacities:
W1 = (100,)
W2 = (120,)
W3 = (150,)
Ws = [W1, W2, W3]

# bin costs:
Costs = [100, 120, 150]

# item weights:
ws = [
    [(10,)], [(14,)], [(17,)], [(19,)], [(24,)], [(29,)], [(32,)], [(33,)],
    [(36,)], [(38,)], [(40,)], [(50,)], [(54,)], [(55,)], [(63,)], [(66,)],
    [(71,)], [(77,)], [(79,)], [(83,)], [(92,)], [(95,)], [(99,)]
]

# item demands:
b = [1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1]
};

$PARAM[b{I}]{b, i0=1};
$PARAM[C{T}]{Costs, i0=1};

var Z{T}, integer, >= 0;
var x{I}, integer, >= 0;
$MVP_FLOW[^Z{^T}]{Ws, ws, ["x[{0}]".format(i+1) for i in range(len(b))], i0=1};

minimize obj: sum{t in T} C[t] * Z[t];
s.t. demand{i in I}: x[i] >= b[i];
end;
