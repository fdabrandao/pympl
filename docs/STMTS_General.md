## General PyMPL statements

* [${...}$](#eval)
* [$EXEC{...};](#exec)
* [$STMT{...};](#stmt)
* [$SET[...]{...};](#set)
* [$PARAM[...]{...};](#param)
* [$VAR[...]{...};](#var)
* [$CON[...]{...};](#con)
* [Return to the index](STMTS)

#### EVAL
Usage: `${python expression}$`

Description: is replaced by the result of `eval("python expression")`.  

Parameters:

  * Python:
    * valid python expression.

Creates:

  * AMPL:
    * is replaced by the result of evaluating the expression.

Examples:  
```ampl
...
var x1, >= ${2+6}$, <= ${10*5}$;
s.t. con1: x + y <= ${abs((2**7)/5-135)}$ * z;
...
```
is replaced by:
```ampl
...
var x1, >= 8, <= 50;
s.t. con1: x + y <= 110 * z;
...
```

#### EXEC
Usage: `$EXEC{python code};`

Description: executes python code.

Parameters:

  * Python:
    * valid python code.

Creates:

  * AMPL:
    * May create anything that results from calls to PyMPL commands.
  * Python:
    * May create new python variables/functions/etc. that can be used in the following statements.

Examples:  

```ampl
...
$EXEC{
for i in range(3):
    STMT("var x{0}, integer, >= 0, <= {1};".format(i, i+1))
};
...
```
 
is replaced by:

```ampl
var x0, integer, >= 0, <= 1;
var x1, integer, >= 0, <= 2;
var x2, integer, >= 0, <= 3;
```

Note: you call use PyMPL commands inside python code as follows:
  * `$CMD[...]{...};` are equivalent to `CMD["..."](...)` in python code;
  * `$CMD{...};` are equivalent to `CMD(...)` in python code.

#### STMT
Usage: `$STMT{python expression};`

Description: is replaced by the result of `eval("python expression")`.  

Parameters:

  * Python:
    * valid python expression.

Creates:

  * AMPL:
    * is replaced by the result of evaluating the expression.

Examples:  

```ampl
...
$STMT{"s.t. con1: x + y <= {0} * z;".format(abs((2**7)/5-135))};
$EXEC{stmt = "s.t. {0}: x >= 10;".format("test")};
$STMT{stmt};
...
```

is replaced by:

```ampl
...
s.t. con1: x + y <= 110 * z;
s.t. test: x >= 10;
...
```
Note: `$STMT{expression};` is equivalent to `${expression}$` ([EVAL](#eval)).

#### SET
Usage: `$SET[set_name]{values};`

Description: creates an AMPL sets.

Parameters:

  * AMPL:
    * `'set_name'`: set name.
  * Python:
    * `values`: list of values.

Creates:

  * AMPL:
    * a set named `'set_name'`.
  * Python:
    * `_set['set_name']`: list of values.

Examples:  

```ampl
...
$SET[A]{range(5)};
$SET[B]{zip(range(5),range(5))};
...
```
 
is replaced by:

```ampl
set A := {0,1,2,3,4};
set B := {(0,0),(1,1),(2,2),(3,3),(4,4)};
```
Note: Is is possible to call external functions (i.e., `$SET[X]{some_function(...)}`) that return the set.

#### PARAM
Usage: `$PARAM[param_name]{values, i0=0};`

Description: creates AMPL parameters.

Parameters:

  * AMPL:
    * Option 1: `'param_name'` -> parameter name;  
    * Option 2: `'param_name{Index_name}'` -> parameter name and index name.
  * Python:
    * `values`: dictionary of key:value pairs or a list of values;
    * `i0`: initial index if `values` is a list of values.

Creates:

  * AMPL:
    * a parameter named `'param_name'`.
  * Python:
    * `_param['param_name']`: dictionary with the parameter data.

Examples:  

```ampl
...
$PARAM[NAME]{"name"}; 
$PARAM[VALUE]{10};
$PARAM[D{I}]{{'a': 1, 'b': 2}};
$PARAM[L0]{[1,2,3], i0=0};
$PARAM[L1]{[1,2,3], i0=1}; # `i0` is the initial index if `values` is a list
...
```
 
is replaced by:

```ampl
param NAME := 'name';
param VALUE := 10;
param D := ['a']1['b']2;
set I := {'a','b'};
param L0 := [0]1[1]2[2]3;
param L1 := [1]1[2]2[3]3;
```
Note: Is is possible to call external functions (i.e., `$PARAM[X]{some_function(...)}`) that return the parameter.

#### VAR
Usage: `$VAR[var_name]{typ="", lb=None, ub=None, index_set=None};`
 
Description: creates AMPL variables.

Parameters:

  * AMPL:
    * Option 1: `'var_name'` ->  variable name;
    * Option 2: `'var_name{Iname}'` -> variable name and index name (`index_set` must be provided).
  * Python:
    * `typ`: variable type (e.g., "integer");
    * `lb`: variable lower bound;
    * `ub`: variable upper bound;
    * `index_set`: index set for the variable.

Creates:

  * AMPL:
    * creates a variable named `'var_name'`.

Examples:  

```ampl
...
$VAR[x]{"integer", 0, 10};
$VAR[y]{"binary"};
$VAR[z]{ub=abs((2**7)/5-135)};
$VAR[xs{I}]{"integer", index_set=range(3)};
...
```
 
is replaced by:

```ampl
var x, integer, >= 0, <= 10;
var y, binary; 
var z, <= 110;
set I := {0,1,2};
var xs{I}, integer;
```

#### CON
Usage: `$CON[constraint_name]{left, sign, right};`

Description: creates AMPL constraints.

Parameters:

  * AMPL:
    * `'constraint_name'`: constraint name.
  * Python:
    * `left`: list of variable names, values, or pairs (variable name, coefficient);
    * `sign`: constraint type (">=", "=", "<=");
    * `right`: list of variable names, values, or pairs (variable name, coefficient).

Creates:

  * AMPL:
    * a constraint named `'constraint_name'`.

Examples:

```ampl
...
$CON[con1]{[("x1",5),("x2",15),("x3",10)],">=",20};
$CON[con2]{[("x1",5),("x2",15),-20],">=",("x3",-10)};
$CON[con3]{[("x1",5)],">=",[("x2",-15),("x3",-10),20]};
$CON[con4]{-20,">=",[("x1",-5),("x2",-15),("x3",-10)]};
$CON[con5]{-20,">=",[(-5, "x1"),("x2",-15),(-10, "x3")]};
$CON[con6]{[-20, "x1"],">=",[(-4, "x1"),("x2",-15),(-10, "x3")]};
$CON[con7]{"x1",">=",[(-4, "x1"),20,("x2",-15),(-10, "x3")]};
...
```
 
is replaced by:

```ampl
s.t. con1: +5*x1+15*x2+10*x3 >= 20;
s.t. con2: +5*x1+15*x2+10*x3 >= 20;
s.t. con3: +5*x1+15*x2+10*x3 >= 20;
s.t. con4: +5*x1+15*x2+10*x3 >= 20;
s.t. con5: +5*x1+15*x2+10*x3 >= 20;
s.t. con6: +5*x1+15*x2+10*x3 >= 20;
s.t. con7: +5*x1+15*x2+10*x3 >= 20;
``` 
Note: all the original constraints are just different representations of the same constraint.

***
Copyright © Filipe Brandão. All rights reserved.  
E-mail: <fdabrandao@dcc.fc.up.pt>. [[Homepage](http://www.dcc.fc.up.pt/~fdabrandao/)]