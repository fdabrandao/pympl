## PyMPL: A Mathematical Programming Toolbox

Copyright (C) 2015-2015, Filipe Brandão
Faculdade de Ciencias, Universidade do Porto
Porto, Portugal. All rights reserved. E-mail: <fdabrandao@dcc.fc.up.pt>.

---
[PyMPL](https://github.com/fdabrandao/pympl) is a python extension to the AMPL modelling language that adds new statements for evaluating python code within AMPL models. PyMPL also includes, among others, procedures for modelling piecewise linear functions, compressed arc-flow graphs for vector packing, lot-sizing reformulations, and sub-tour elimination constraints for TSP.

### Useful links

* PyMPL documentation: <https://github.com/fdabrandao/pympl/wiki>
* GiHub repository: <https://github.com/fdabrandao/pympl>
* BitBucket repository: <https://bitbucket.org/fdabrandao/pympl>

### Setup

Install from the repository:
```bash
$ sudo pip install pympl
```

Or build and install locally:
```
$ sudo pip install -r requirements.txt
$ sudo pip install . --upgrade
$ bash test.sh test_install
```

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
