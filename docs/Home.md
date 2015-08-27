## Home

[PyMPL](https://github.com/fdabrandao/pympl) is a python extension to the AMPL modelling language that adds new statements for evaluating python code within AMPL models. PyMPL also includes, among others, procedures for modelling piecewise linear functions, compressed arc-flow graphs for vector packing, lot-sizing reformulations, and sub-tour elimination constraints for TSP.

### Table of Contents

  * [Useful links](#useful-links)
  * [Examples](#examples)
  * [PyMPL Parser](#pympl-parser)
  * [PyMPL Statements](STMTS)

### Useful links

* GiHub repository: <https://github.com/fdabrandao/pympl>
* BitBucket repository: <https://bitbucket.org/fdabrandao/pympl>

### Examples

``piecewise_linear.mod``

```ampl
# Evaluate python code:
$EXEC{
xvalues = [0, 10, 15, 25, 30, 35, 40, 45, 50, 55, 60, 70]
yvalues = [0, 20, 15, 10, 0, 50, 18, 0, 15, 24, 10, 15]
};

var u >= 0;
# Model a piecewise linear function given a list of pairs (x, y=f(x)):
$PWL[x,y]{zip(xvalues, yvalues)};

maximize obj: 2*x + 15*y;
s.t. A: 3*x + 4*y <= 250;
s.t. B: 7*x - 2*y + 3*u <= 170;

solve;
display x, y, u;
display "Objective:", 2*x + 15*y;
end;
```

``vector_packing.mod``:

```ampl
# Load a vector packing instance from a file:
$VBP_LOAD[instance1{I,D}]{"instance1.vbp", i0=1};

var x{I}, >= 0;

# Generate an arc-flow model for instance1:
$VBP_FLOW[Z]{_instance1.W, _instance1.w, ["x[%d]"%i for i in _sets['I']]};
# Variable declarations and flow conservation constraints will be created here

minimize obj: Z;
s.t. demand{i in I}: x[i] >= instance1_b[i]; # demand constraints

solve;
display Z;
end;
```

``variable_size_bin_packing.mod``:

```ampl
# Evaluate python code:
$EXEC{
# Bin capacities:
W1 = [100]
W2 = [120]
W3 = [150]

# Bin costs:
Costs = [100, 120, 150]

# Item weights:
ws = [[10], [14], [17], [19], [24], [29], [32], [33], [36],
      [38], [40], [50], [54], [55], [63], [66], [71], [77],
      [79], [83], [92], [95], [99]]

# Item demands:
b = [1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1]
};

# Generate a parameter 'b' for the demand:
$PARAM[b{I}]{b, i0=1};

# Generate a parameter 'C' for the cost:
$PARAM[C{T}]{Costs, i0=1};

# Feedback arcs for each graph:
var Z{T}, integer, >= 0;
# Assignment variables:
var x{T, I}, integer, >= 0;
# Generate an arc-flow graph for each bin type:
$VBP_FLOW[^Z[1]]{W1, ws, ["x[1, %d]"%i for i in _sets['I']]};
$VBP_FLOW[^Z[2]]{W2, ws, ["x[2, %d]"%i for i in _sets['I']]};
$VBP_FLOW[^Z[3]]{W3, ws, ["x[3, %d]"%i for i in _sets['I']]};
# Note: the ^prefix is used to avoid the redefinition of Z

minimize obj: sum{t in T} C[t] * Z[t];
s.t. demand{i in I}: sum{t in T} x[t, i] >= b[i];

solve;
display{t in T} Z[t]; # number of bins of type t used
display sum{t in T} C[t] * Z[t]; # cost
end;
```

### PyMPL Parser

```python
import os
from pympl import PyMPL  # import the parser

# Create a parser and pass local and global variables to the model:
parser = PyMPL(locals_=locals(), globals_=globals())`

# Parse a file with PyMPL statements and produce a valid AMPL model:
parser.parse("pympl_model.mod", "ampl_model.mod")

# Call GLPK to solve the model (if the original model uses only valid GMPL statements):
os.system("glpsol --math ampl_model.mod")

# Call AMPL to solve the model:
os.system("ampl ampl_model.mod")
```

[[Folder with examples](https://github.com/fdabrandao/pympl/tree/master/examples)]

Advanced features:

* Given a function `f(varname)` that takes a variable name returns its value:

  * If any command used implements solution extraction you can use `parser[command_name].extract(f)` to extract the solution;
  * If any command used implements cut generation you can use `parser[command_name].separate(f)` to generate cutting planes.

***
Copyright © Filipe Brandão. All rights reserved.  
E-mail: <fdabrandao@dcc.fc.up.pt>. [[Homepage](http://www.dcc.fc.up.pt/~fdabrandao/)]
