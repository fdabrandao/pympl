## PyMPL: A Mathematical Programming Toolbox
Copyright (C) 2015-2016, Filipe Brandão  
Faculdade de Ciências, Universidade do Porto  
Porto, Portugal. All rights reserved. E-mail: <fdabrandao@dcc.fc.up.pt>.

---

[PyMPL](https://github.com/fdabrandao/pympl) is a python extension to the AMPL modeling language that adds new [statements](https://github.com/fdabrandao/pympl/wiki/STMTS) for evaluating python code within AMPL/GMPL models. PyMPL also includes, among others, procedures for modeling [piecewise linear functions](https://github.com/fdabrandao/pympl/wiki/STMTS_SOS), [compressed arc-flow graphs](https://github.com/fdabrandao/pympl/wiki/STMTS_VPSolver) for vector packing, [sub-tour elimination constraints](https://github.com/fdabrandao/pympl/wiki/STMTS_TSP) for TSP, and [lot-sizing reformulations](https://github.com/fdabrandao/pympl/wiki/STMTS_LSLIB) (LS-LIB). PyMPL is fully compatible with both python 2 and 3.

![](https://img.shields.io/badge/license-AGPLv3+-blue.svg)
[![](https://travis-ci.org/fdabrandao/pympl.svg?branch=master)](https://travis-ci.org/fdabrandao/pympl)
[![Coverage Status](https://coveralls.io/repos/github/fdabrandao/pympl/badge.svg?branch=experimental)](https://coveralls.io/github/fdabrandao/pympl)

### Useful links

* PyMPL documentation: <https://github.com/fdabrandao/pympl/wiki>
* GiHub repository: <https://github.com/fdabrandao/pympl>
* BitBucket repository: <https://bitbucket.org/fdabrandao/pympl>
* Docker repository: <https://hub.docker.com/r/fdabrandao/pympl>
* PyPI repository: <https://pypi.python.org/pypi/PyMPL>

### Setup

Install from the [repository](https://pypi.python.org/pypi/PyMPL):
```bash
$ pip install pympl
```

Or build and install locally:
```
$ pip install -r requirements.txt
$ pip install . --upgrade
$ cd examples; py.test -v --cov pympl
```

PyMPL can also be used inside a [Docker container](https://github.com/fdabrandao/pympl/wiki/Docker-container) that includes a simple web app for an easy usage.

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
end;
```

``vector_packing.mod``:

```ampl
# Load a vector packing instance from a file:
$EXEC{
from pyvpsolver import VBP
instance = VBP.from_file("data/instance.vbp")
};
$PARAM[b{I}]{instance.b};
var x{I}, >= 0;

# Generate the arc-flow model:
$VBP_FLOW[Z]{instance.W, instance.w, ["x[{}]".format(i) for i in range(instance.m)]};
# Variable declarations and flow conservation constraints will be created here

minimize obj: Z;
s.t. demand{i in I}: x[i] >= b[i]; # demand constraints
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

* Given a function `f(varname)` that takes a variable name and returns its value:

  * If any command used implements solution extraction you can use `parser[command_name].extract(f)` to extract the solution;
  * If any command used implements cut generators you can use `parser[command_name].separate(f)` to generate cutting planes.

***
Copyright © 2015-2016 [Filipe Brandão](http://www.dcc.fc.up.pt/~fdabrandao/) <[fdabrandao@dcc.fc.up.pt](mailto:fdabrandao@dcc.fc.up.pt)>. All rights reserved.
