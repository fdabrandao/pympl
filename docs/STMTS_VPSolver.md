## VPSolver: Vector Packing Solver

* [$VBP_LOAD[...]{...};](#vbp_load)
* [$VBP_FLOW[...]{...};](#vbp_flow)
* [$VBP_GRAPH[...]{...};](#vbp_graph)
* [Return to the index](STMTS)

#### VBP_LOAD
Usage: `$VBP_LOAD[name]{fname, i0=0, d0=0};`

Description: loads vector packing instances.

Requirements: [VPSolver](https://github.com/fdabrandao/vpsolver)

Parameters:

  * AMPL:
    * Option 1: `'name'` -> symbolic name for the instance;
    * Option 2: `'name{Iname}'` -> symbolic name for the instance, and for the index set;
    * Option 3: `'name{Iname, Dname}'` -> symbolic name for the instance, for the index set, and for the dimension set;
  * Python:
    * `fname`: file name;
    * `i0`: initial index for items (default 0);
    * `d0`: initial index for dimensions (default 0);

Creates:

  * AMPL:
    * `param name_m`: number of different item types;
    * `param name_n`: total number of items;
    * `param name_p`: number of dimensions;
    * `param name_W`: bin capacity;
    * `param name_b`: item demands;
    * `param name_w`: item weights;
    * `set name_I`: index set for items (if no other name was specified);
    * `set name_D`: index set for dimensions (if no other name was specified).
  * Python:
    * `_set['set_name']` lists for each set;
    * `_param['param_name']` dictionaries for each param;

Examples:

`instance.vbp`:

```
2
10 3
4
3 1 4
5 2 3
8 1 1
4 1 9
```

`model.mod`:

```ampl
...
$VBP_LOAD[instance{I,D}]{"instance.vbp", i0=1, d0=0}
...
```
 
is replaced by:

```ampl
param instance_m := 4; # number of different item types
param instance_n := 17;# total number of items
param instance_p := 2; # number of dimensions
set I := {1,2,3,4};    # index set for items (starting at `i0`)
set D := {0,1};        # index set for dimensions (starting at `d0`)
param instance_W{D};   # bin capacity
param instance_b{I};   # item demands
param instance_w{I,D}; # item weights
```

#### VBP_FLOW
Usage: `$VBP_FLOW[zvar_name]{W, w, b, bounds=None};`

Description: generates arc-flow models with graph compression for vector packing instances.

Requirements: [VPSolver](https://github.com/fdabrandao/vpsolver)

Parameters:

  * AMPL:
    * `zvar_name`: variable name for the amount of flow in the feedback arc (which corresponds to the number of bins used);
  * Python:
    * `W`: bin capacity;
    * `w`: item weights;
    * `b`: item demands (may include strings with variable names if the demand is not fixed);
    * `bounds`: maximum demand for each item.  

Creates:

  * AMPL:
    * an arc-flow model with graph compression for the vector packing instance (variables and constraints);
    * a variable `'zvar_name'` for the amount of flow in the feedback arc.
  * Python:
    * stores information for solution extraction.

Examples:

```ampl
$VBP_LOAD[instance1{I,D}]{"instance.vbp",1};
var x{I}, >= 0;
$VBP_FLOW[Z]{_instance1.W, _instance1.w, ["x[%d]"%i for i in _sets['I']]};    

minimize obj: Z;
s.t. demand{i in I}: x[i] >= instance1_b[i]; # demand constraints

solve;
end;
```
 
is replaced by:

```ampl
var x{I}, >= 0;  
/* arc-flow model with graph compression for instance.vbp */
/* Z is the amount of flow on the feedback arc */
/* x[i] = amount of flow on arcs associated with item i */
minimize obj: Z;
s.t. demand{i in I}: x[i] >= instance1_b[i]; # demand constraints

solve;
end;
```

#### VBP_GRAPH
Usage: `$VBP_GRAPH[V_name, A_name]{W, w, labels, bounds=None};`

Requirements: [VPSolver](https://github.com/fdabrandao/vpsolver)

Description: generates compressed arc-flow graphs for vector packing instances.  

Parameters:

  * AMPL:
    * `V_name`: name for the set of vertices;
    * `A_name`: name for the set of arcs.
  * Python:
    * `W`: bin capacity;
    * `w`: item weights;
    * `labels`: item labels ;
    * `bounds`: maximum demand for each item.

Creates:

  * AMPL:
    * `set 'V_name'`: set of vertices;
    * `set 'A_name'`: set of arcs.
  * Python:
    * `_sets['V_name']`: set of vertices;
    * `_sets['A_name']`: set of arcs;

Examples:

```ampl
$VBP_LOAD[instance1{I,D}]{"instance.vbp", i0=1}; 
$VBP_GRAPH[V,A]{_instance1.W, _instance1.w, _sets['I']};

# Variables:
var Z, integer, >= 0; # amount of flow in the feedback arc
var f{A}, integer, >= 0; # amount of flow in each arc
# Objective:
maximize obj: Z;
# Flow conservation constraints:
s.t. flowcon{k in V}: 
    sum{(u,v,i) in A: v == k} f[u,v,i]  - sum{(u,v,i) in A: u == k} f[u, v, i] 
    = if k == 'T' then Z else
      if k == 'S' then -Z else
      0;
# Demand constraints:
s.t. demand{k in I}: sum{(u,v,i) in A: i == k} >= instance1_b[i];
```

Note: the source vertex is `'S'`, the target is `'T'`, and loss arcs are labeled with `'LOSS'`.

***
Copyright © Filipe Brandão. All rights reserved.  
E-mail: <fdabrandao@dcc.fc.up.pt>. [[Homepage](http://www.dcc.fc.up.pt/~fdabrandao/)]