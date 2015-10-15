## PyMPL Tools

PyMPL includes a few tools in order to make it easier to parse PyMPL models, solve them and extract their solutions.

* [Usage example](#usage-example)
* [Solver wrappers](#solver-wrappers)
* [Tools API](#tools-api)
* [glpkutils](#glpkutils)

### Usage example

In the following example, we solve a small cutting stock problem with rolls of width 5180,
items of width 1250, 1000, 750, 915, 920, 985 with demands
19, 264, 10, 30, 5, 21, respectively. Since the base model (`model.mod`) is a valid GMPL model, 
we use GLPK to convert it to LP and to solve it. Nevertheless, any other solver could have been used to solve it.

``model.mod (AMPL/GMPL + PyMPL statements)``

```ampl
$EXEC{
W = [5180]                                       # roll width
w = [[1250], [1000], [750], [915], [920], [985]] # item widths
b = [19, 264, 10, 30, 5, 21]                     # item demands
};
$PARAM[b{I}]{b, i0=1};
var x{I}, >= 0;
# Generate an arc-flow model (with x[i] = total amount of flow on arcs (u, v, i)):
$VBP_FLOW[Z]{W, w,  ["x[1]", "x[2]", "x[3]", "x[4]", "x[5]", "x[6]"]};
minimize obj: Z;
s.t. demand{i in I}: x[i] >= b[i];
solve;
end;
```

``solve.py (Python)``

```python
from pympl import PyMPL, Tools, glpkutils
parser = PyMPL() # initialize the parser 
parser.parse("model.mod", "model.out.mod") # parse "model.mod" and produce "model.out.mod"
glpkutils.mod2lp("model.out.mod", "model.lp") # use GLPK to convert "model.out.mod" to LP
out, varvalues = Tools.script("glpk_wrapper.sh", "model.lp") # solve and return the solution
# extract a vector packing solution from the arc-flow solution:
sol = parser["VBP_FLOW"].extract(lambda varname: varvalues.get(varname, 0))
```

``Output``

```
...
OPTIMAL LP SOLUTION FOUND
Integer optimization begins...
+    29: mip =     not found yet >=              -inf        (1; 0)
+    88: >>>>>   7.000000000e+01 >=   6.900000000e+01   1.4% (30; 0)
+    93: >>>>>   6.900000000e+01 >=   6.900000000e+01   0.0% (6; 33)
+    93: mip =   6.900000000e+01 >=     tree is empty   0.0% (0; 59)
INTEGER OPTIMAL SOLUTION FOUND
Time used:   0.0 secs
Memory used: 0.1 Mb (145550 bytes)
Writing MIP solution to `/tmp/Xz5GCUfsze/sol.out'...
Graph: Z (flow=69)                                   # 69 rolls are used
	[(4, ['i=3', 'i=3', 'i=4', 'i=4', 'i=4', 'i=4']),# 4 rolls with this pattern 
	 (1, ['i=1', 'i=2', 'i=3', 'i=3', 'i=4']),       # 1 roll with this pattern 
	 (13, ['i=1', 'i=2', 'i=2', 'i=2', 'i=4']),      # 13 rolls with this pattern 
	 (25, ['i=2', 'i=2', 'i=2', 'i=2', 'i=2']),      # 25 rolls with this pattern 
	 (5, ['i=1', 'i=2', 'i=2', 'i=2', 'i=5']),       # 5 rolls with this pattern 
	 (21, ['i=2', 'i=2', 'i=2', 'i=2', 'i=6'])]      # 21 rolls with this pattern 
```

### Solver wrappers
PyMPL includes several scripts for solving MPS/LP models using different
solvers:

* `scripts/gurobi_wrapper.sh`: Gurobi
* `scripts/cplex_wrapper.sh`: IBM CPLEX
* `scripts/coinor_wrapper.sh`: COIN-OR CBC
* `scripts/glpk_wrapper.sh`: GLPK
* `scripts/scip_wrapper.sh`: SCIP
* `scripts/lpsolve_wrapper.sh`: lp_solve

Usage:

```bash
$ X_wrapper.sh --mps model.mps
$ X_wrapper.sh --lp model.lp
$ X_wrapper.sh --mps model.mps --wsol vars.sol
$ X_wrapper.sh --lp model.lp --wsol vars.sol
```

### Tools API

How to import: 

* `from pympl import Tools`.

How to use:

* `output, solution = Tools.script(script_name, model, options=None, verbose=None)`
    * Description: calls VPSolver scripts.
    * Important arguments:
        * `script_name`: wrapper script (e.g., `glpk_wrapper.sh`);
        * `model`: model file (.mps/.lp file name);
        * `options`: parameters to pass to the wrapper.
    * Actions:
        * calls `script_name` to solve a .mps/.lp model;
        * returns the output and a python dictionary `{var:value}` with the solution.
    * Usage examples:
        * `Tools.script(script name, .mps file/MPS object)`;
        * `Tools.script(script name, .lp file/LP object)`.

* `Tools.set_verbose(verbose)`
    * Description: sets the default "verbose" behaviour.
    * Arguments:
        * `verbose`: `True` or `False`.
    * Note: The default behaviour is overridden if the `verbose` argument is set to a value different from `None` in any API call.

### glpkutils

How to import: 

* `from pympl import glpkutils`.

How to use:

* `glpkutils.mod2lp(fname_mod, fname_lp, verbose=None)`
    * Description: calls glpsol to convert GMPL models to LP.
    * Important arguments:
        * `fname_mod`: GMPL model file (.mod file name);
        * `fname_lp`: LP model file (.lp file name).

* `glpkutils.mod2mps(fname_mod, fname_mps, verbose=None)`
    * Description: calls glpsol to convert GMPL models to MPS.
    * Important arguments:
        * `fname_mod`: GMPL model file (.mod file name);
        * `fname_mps`: MPS model file (.mps file name).

***
Copyright © Filipe Brandão. All rights reserved.  
E-mail: <fdabrandao@dcc.fc.up.pt>. [[Homepage](http://www.dcc.fc.up.pt/~fdabrandao/)]