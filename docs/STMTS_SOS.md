## Special ordered sets and piecewise linear functions

* [$SOS1{...};](#sos1)
* [$SOS2{...};](#sos2)
* [$PWL[...]{...};](#pwl)
* [Return to the index](STMTS)

#### SOS1
Usage: `$SOS1{varl, ub=1};`

Description: creates a special ordered set of type 1 (SOS1) for a set of variables. At most one variable in a SOS1 can take a strictly positive value.

Parameters:

  * Python:
    * `varl`: list of variable names;
    * `ub`: largest possible value if non-zero (default 1).

Creates:

  * AMPL:
    * creates a variables and constraints to model the special ordered set.

Example:

```ampl
var x{1..3}, >= 0;
$SOS1{["x[1]", "x[2]", "x[3]"]};
```

#### SOS2
Usage: `$SOS2{varl, ub=1};`

Description: creates a special ordered set of type 2 (SOS2) for a set of variables.  At most two variables in a SOS2 can take a strictly positive value, and if two are non-zero these must be consecutive in their ordering.

Parameters:

  * Python:
    * `varl`: list of variable names;
    * `ub`: largest possible value if non-zero (default 1).

Creates:

  * AMPL:
    * creates a variables and constraints to model the special ordered set.

Example:

```ampl
$PARAM[X{I}]{[0, 10, 15, 25, 30, 35, 40, 45, 50, 55, 60, 70]};
$PARAM[Y{^I}]{[0, 20, 15, 10, 0, 50, 18, 0, 15, 24, 10, 15]};
# Model a piecewise linear function
var x;
var y;
# Model a piecewise linear function using a special ordered set of type 2:
var z{I}, >= 0;
s.t. fix_x: x = sum{i in I} X[i] * z[i];
s.t. fix_y: y = sum{i in I} Y[i] * z[i];
s.t. convexity: sum{i in I} z[i] = 1;
$SOS2{["z[%d]"%i for i in _sets['I']]};
```

#### PWL
Usage: `$PWL[var_x, var_y]{xyvalues};`

Description: models a piecewise linear function given a list of pairs (x, y=f(x)).

Parameters:

  * AMPL:
    * `'var_x'`: name for the first variable;
    * `'var_y'`: name for the second variable.
  * Python:
    * 'xyvalues': list of pairs (x, y=f(x)) for the piecewise linear function f(x).

Creates:

  * AMPL:
    * creates variables `'var_x'` and `'var_y'`;
    * creates a variables and constraints to model the piecewise linear function (`'var_y'` = f(`'var_x'`)).

Examples:

```ampl
$EXEC{
xvalues = [0, 10, 15, 25, 30, 35, 40, 45, 50, 55, 60, 70]
yvalues = [0, 20, 15, 10, 0, 50, 18, 0, 15, 24, 10, 15]
};
$PWL[x,y]{zip(xvalues, yvalues)};
```

***
Copyright © Filipe Brandão. All rights reserved.  
E-mail: <fdabrandao@dcc.fc.up.pt>. [[Homepage](http://www.dcc.fc.up.pt/~fdabrandao/)]