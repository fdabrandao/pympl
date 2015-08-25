## Travelling Salesman Problem (TSP)

* [$ATSP_MTZ{...};](#atsp_mtz)
* [$ATSP_SCF{...};](#atsp_scf)
* [$ATSP_MCF{...};](#atsp_mcf)
* [Return to the index](STMTS)

#### ATSP_MTZ
Usage: `$ATSP_MTZ{xvars, DL=False, cuts=False};`

Description: creates a submodel for TSP using Miller, Tucker and Zemlin (MTZ) (1960) subtour elimination constraints.

Parameters:

  * Python:
    * `xvars`: list of binary variables for the arcs in the graph;
    * `DL`: if `True` uses Desrochers and Laporte (1991) lifted MTZ inequalities;
    * `cuts`: if `True` stores information for cut generation.

Creates:

  * AMPL:
    * A submodel for TSP projected on `xvars` variables.
  * Python:
    * stores information for cut generation if requested.

Examples:

```ampl
$SET[V]{set of vertices};
$SET[A]{set of arcs};
$PARAM[cost{^A}]{cost of each arc};
var x{A}, binary;
minimize total: sum{(i,j) in A} cost[i,j] * x[i,j];
$ATSP_MTZ{{(i,j): "x[%d,%d]"%(i,j) for i, j in _sets['A']}, DL=True, cuts=True};
```

#### ATSP_SCF
Usage: `$ATSP_SCF{xvars, cuts=False};`

Description: creates a submodel for TSP using the single commodity flow model of Gavish and Graves (1978).

Parameters:

  * Python:
    * `xvars`: list of binary variables for the arcs in the graph;
    * `cuts`: if `True` stores information for cut generation.

Creates:

  * AMPL:
    * A submodel for TSP projected on `xvars` variables.
  * Python:
    * stores information for cut generation if requested.

Examples:

```ampl
$SET[V]{set of vertices};
$SET[A]{set of arcs};
$PARAM[cost{^A}]{cost of each arc};
var x{A}, binary;
minimize total: sum{(i,j) in A} cost[i,j] * x[i,j];
$ATSP_SCF{{(i,j): "x[%d,%d]"%(i,j) for i, j in _sets['A']}, cuts=True};
```

#### ATSP_MCF
Usage: `$ATSP_SCF{xvars, cuts=False};`

Description: creates a submodel for TSP using the multi commodity flow model of Wong (1980) and Claus (1984).

Parameters:

  * Python:
    * `xvars`: list of binary variables for the arcs in the graph;
    * `cuts`: if `True` stores information for cut generation.

Creates:

  * AMPL:
    * A submodel for TSP projected on `xvars` variables.
  * Python:
    * stores information for cut generation if requested.

Examples:

```ampl
$SET[V]{set of vertices};
$SET[A]{set of arcs};
$PARAM[cost{^A}]{cost of each arc};
var x{A}, binary;
minimize total: sum{(i,j) in A} cost[i,j] * x[i,j];
$ATSP_MCF{{(i,j): "x[%d,%d]"%(i,j) for i, j in _sets['A']}};
```

***
Copyright © Filipe Brandão. All rights reserved.  
E-mail: <fdabrandao@dcc.fc.up.pt>. [[Homepage](http://www.dcc.fc.up.pt/~fdabrandao/)]
