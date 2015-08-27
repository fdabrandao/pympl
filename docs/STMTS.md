## PyMPL Statements

There are three types of statements:

1. `${python code}$`
 
  * [EVAL](STMTS_General#eval): `${python expression}$`

2. `$CMD{python parameters or code};`

  * [EXEC](STMTS_General#exec): `$EXEC{python code};`
  * [STMT](STMTS_General#stmt): `$STMT{python expression};`

3. `$CMD[AMPL parameters]{python arguments or code};` 

  * [SET](STMTS_General#set): `$SET[set_name]{values};`
  * [PARAM](STMTS_General#param): `$PARAM[param_name]{values, i0=0};`
  * [VAR](STMTS_General#var): `$VAR[var_name]{typ="", lb=None, ub=None, index_set=None};`
  * [CON](STMTS_General#con): `$CON[constraint_name]{left, sign, right};`

Additional statements:

1. Statements for [VPSolver](https://github.com/fdabrandao/vpsolver):

  * [VBP_LOAD](STMTS_VPSolver#vbp_load): `$VBP_LOAD[name]{fname, i0=0, d0=0};`
  * [VBP_FLOW](STMTS_VPSolver#vbp_flow): `$VBP_FLOW[zvar]{W, w, b, bounds=None};`
  * [VBP_GRAPH](STMTS_VPSolver#vbp_graph): `$VBP_GRAPH[V_name, A_name]{W, w, labels, bounds=None};`

2. Statements for special ordered sets and piecewise linear functions:

  * [SOS1](STMTS_SOS#sos1): `$SOS1{varl, ub=1};`
  * [SOS2](STMTS_SOS#sos2): `$SOS2{varl, ub=1};`
  * [PWL](STMTS_SOS#pwl): `$PWL[var_x, var_y]{xyvalues};`

3. Statements for TSP:

  * [ATSP_MTZ](STMTS_TSP#atsp_mtz): `$ATSP_MTZ{xvars, DL=False, cuts=False};`
  * [ATSP_SCF](STMTS_TSP#atsp_scf): `$ATSP_SCF{xvars, cuts=False};`
  * [ATSP_MCF](STMTS_TSP#atsp_mcf): `$ATSP_SCF{xvars, cuts=False};`

4. Statements for Lot-sizing ([LS-LIB](STMTS_LSLIB)):

  * [Wagner-Whitin models](STMTS_LSLIB#wagner-whitin-models): `$WW_*{...};`
  * [Lot-sizing models](STMTS_LSLIB#lot-sizing-models): `$LS_*{...};`

**Note**: The values between `[]` are usually used to name new AMPL variables, constraints, sets, or parameters. Names starting with a `^` indicate that the corresponding AMPL element should not be defined by the command. This prefix is useful when the corresponding AMPL element was declared before and we do not want to declared it again.

***
Copyright © Filipe Brandão. All rights reserved.  
E-mail: <fdabrandao@dcc.fc.up.pt>. [[Homepage](http://www.dcc.fc.up.pt/~fdabrandao/)]