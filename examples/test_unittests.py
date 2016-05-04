#!/usr/bin/env python
"""
This code is part of the Mathematical Programming Toolbox PyMPL.

Copyright (C) 2015-2016, Filipe Brandao
Faculdade de Ciencias, Universidade do Porto
Porto, Portugal. All rights reserved. E-mail: <fdabrandao@dcc.fc.up.pt>.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import print_function

import os
import pytest
from pympl import PyMPL


def test_empty():
    """Test empty files."""
    parser = PyMPL()
    parser.input = ""
    parser.parse(comment_cmds=False)
    assert parser.output == ""


def test_set():
    """Test $SET[name]{values} calls."""
    parser = PyMPL()
    parser.input = """
    $SET[A]{range(5)};
    $SET[B]{zip(range(5),range(5))};
    $SET[^C]{range(5)};
    """
    parser.parse(comment_cmds=False)
    assert "set A := {0,1,2,3,4};" in parser.output
    assert "set B := {(0,0),(1,1),(2,2),(3,3),(4,4)};" in parser.output
    assert "set C := {0,1,2,3,4};" not in parser.output
    assert "set ^C := {0,1,2,3,4};" not in parser.output


def test_param():
    """Test $PARAM[name]{value} calls."""
    parser = PyMPL()
    parser.input = """
    $PARAM[NAME]{"name"};
    $PARAM[VALUE]{10};
    $PARAM[D{I}]{{'a': 1}};
    $PARAM[L0]{[1,2,3], i0=0};
    $PARAM[L1]{[1,2,3], i0=1};
    $PARAM[^NAME2]{"something"};
    """
    parser.parse(comment_cmds=False)
    assert "param NAME := 'name';" in parser.output
    assert "param VALUE := 10;" in parser.output
    assert "param D := ['a']1;" in parser.output
    assert "set I := {'a'};" in parser.output
    assert "param L0 := [0]1[1]2[2]3;" in parser.output
    assert "param L1 := [1]1[2]2[3]3;" in parser.output
    assert "param NAME2 := 'something';" not in parser.output
    assert "param ^NAME2 := 'something';" not in parser.output


def test_var():
    """Test $VAR[name]{typ, lb, ub} calls."""
    parser = PyMPL()
    parser.input = """
    $VAR[x]{"integer", 0, 10};
    $VAR[y]{"binary"};
    $VAR[z]{ub=abs((2**7)//5-135)};
    $VAR[^z]{"integer", 0, 10};
    $VAR[xs{I}]{"integer", index_set=range(3)};
    $EXEC{VAR['y']("binary")};
    """
    parser.parse(comment_cmds=False)
    assert "var x, integer, >= 0, <= 10;" in parser.output
    assert "var y, binary;" in parser.output
    assert "var z, <= 110;" in parser.output
    assert "var ^z, integer, >= 0, <= 10;" not in parser.output
    assert "var y, binary;" in parser.output
    assert "var xs{I}, integer;" in parser.output
    assert "set I := {0,1,2};" in parser.output


def test_con():
    """Test $CON[name]{lincomb, sign, rhs} calls."""
    parser = PyMPL()
    parser.input = """
    $VAR[x1]{}; $VAR[x2]{}; $VAR[x3]{};
    $CON[con1]{[("x1",5),("x2",15),("x3",10)],">=",20};
    $CON[con2]{[("x1",5),("x2",15),-20],">=",("x3",-10)};
    $CON[con3]{[("x1",5)],">=",[("x2",-15),("x3",-10),20]};
    $CON[con4]{-20,">=",[("x1",-5),("x2",-15),("x3",-10)]};
    $CON[con5]{-20,">=",[(-5, "x1"),("x2",-15),(-10, "x3")]};
    $CON[con6]{[-20, "x1"],">=",[(-4, "x1"),("x2",-15),(-10, "x3")]};
    $CON[con7]{"x1",">=",[(-4, "x1"),20,("x2",-15),(-10, "x3")]};
    $CON[^xyz]{[("x1",5),("x2",15),("x3",10)],">=",20};
    """
    parser.parse(comment_cmds=False)
    assert "s.t. con1: +5*x1 +15*x2 +10*x3 >= 20;" in parser.output
    assert "s.t. con2: +5*x1 +15*x2 +10*x3 >= 20;" in parser.output
    assert "s.t. con3: +5*x1 +15*x2 +10*x3 >= 20;" in parser.output
    assert "s.t. con4: +5*x1 +15*x2 +10*x3 >= 20;" in parser.output
    assert "s.t. con5: +5*x1 +15*x2 +10*x3 >= 20;" in parser.output
    assert "s.t. con6: +5*x1 +15*x2 +10*x3 >= 20;" in parser.output
    assert "s.t. con7: +5*x1 +15*x2 +10*x3 >= 20;" in parser.output
    assert "s.t. xyz: +5*x1 +15*x2 +10*x3 >= 20;" not in parser.output


def test_stmt():
    """Test $STMT{stmt} calls."""
    parser = PyMPL()
    parser.input = """
    $STMT{"s.t. con1: x + y <= {0} * z;".format(abs((2**7)//5-135))};
    $EXEC{stmt = "s.t. {0}: x >= 10;".format("test")};
    $STMT{stmt};
    """
    parser.parse(comment_cmds=False)
    assert "s.t. con1: x + y <= 110 * z;" in parser.output
    assert "s.t. test: x >= 10;" in parser.output


def test_eval():
    """Test ${expression}$ calls."""
    parser = PyMPL()
    parser.input = """
    s.t. con1: x + y <= ${abs((2**7)//5-135)}$ * z;
    var x1, >= ${2+6}$, <= ${10*5}$;
    """
    parser.parse(comment_cmds=False)
    assert "s.t. con1: x + y <= 110 * z;" in parser.output
    assert "var x1, >= 8, <= 50;" in parser.output


def test_comments():
    """Test valid comments."""
    parser = PyMPL()
    parser.input = """
    /* ... $SET[A]{range(5)}; ... */
    # $PARAM[VALUE]{10};
    # ... $PARAM[VALUE2]{10}; ...
    param a := "\\"/*";
    $PARAM[Y]{10};
    param b := "*/";
    """
    parser.parse(comment_cmds=True)
    assert "set A := {0,1,2,3,4};" not in parser.output
    assert "param VALUE := 10;" not in parser.output
    assert "param VALUE2 := 10;" not in parser.output
    assert "param Y := 10;" in parser.output
    assert "# $PARAM[VALUE]{10};" in parser.output
    assert "/*EVALUATED:PARAM[Y]{10}*/" in parser.output


def test_exceptions():
    """Test if exceptions are being thrown correctly."""
    parser = PyMPL()
    parser.input = """$EXEC{print(1/0)};"""
    with pytest.raises(ZeroDivisionError):
        parser.parse(comment_cmds=False)
    parser.input = """$SET[X]{0};"""
    with pytest.raises(TypeError):
        parser.parse(comment_cmds=False)
    parser.input = """$VBP_FLOW[Z]{100, [10, 10]};"""
    with pytest.raises(TypeError):
        parser.parse(comment_cmds=False)
    parser.input = """$VBP_FLOW[Z]{100, 10};"""
    with pytest.raises(TypeError):
        parser.parse(comment_cmds=False)
    parser.input = """$SET[X]{};"""
    with pytest.raises(TypeError):
        parser.parse(comment_cmds=False)
    parser.input = """$SET[X]{[1,2,3]};$SET[X]{[1,2]};"""
    with pytest.raises(AssertionError):
        parser.parse(comment_cmds=False)
    parser.input = """$SET[2X]{[1,2,3]};"""
    with pytest.raises(AssertionError):
        parser.parse(comment_cmds=False)


def test_glpkutils():
    """Test glpkutils."""
    from pympl import Tools, glpkutils
    os.chdir(os.path.dirname(__file__) or os.curdir)

    mod_in, mod_out = "pwl.mod", "tmp/pwl.out.mod"
    lp_out, mps_out = "tmp/pwl.lp", "tmp/pwl.mps"

    parser = PyMPL(locals_=locals(), globals_=globals())
    parser.parse(mod_in, mod_out)

    glpkutils.mod2lp(mod_out, lp_out, verbose=True)
    glpkutils.mod2mps(mod_out, mps_out, verbose=True)

    Tools.clear()
    Tools.set_verbose(False)
    out, varvalues = Tools.script("glpk_wrapper.sh", lp_out, verbose=True)
    out, varvalues = Tools.script("glpk_wrapper.sh", mps_out, verbose=True)


def test_model():
    """Test model."""
    from pympl import Model, Tools, glpkutils
    os.chdir(os.path.dirname(__file__) or os.curdir)
    model = Model()
    values = [15, 10, 9, 5]
    weights = [1, 5, 3, 4]
    xvars = []
    for i in range(len(values)):
        var = model.add_var(lb=0, ub=1, vtype="I")
        xvars.append(var)
    profit = model.add_var(lb=0, vtype="C")
    model.add_con([(x, w) for x, w in zip(xvars, weights)], "<=", 8)
    model.add_con(profit, "=", [(x, v) for x, v in zip(xvars, values)])
    model.set_obj("max", profit)
    lp_out = "tmp/model.lp"
    mps_out = "tmp/model.mps"
    mod_out = "tmp/model.mod"
    model.write(lp_out)
    model.write(mps_out)
    model.write(mod_out)
    out, varvalues = Tools.script("glpk_wrapper.sh", lp_out, verbose=True)
    assert varvalues[profit] == 29
    out, varvalues = Tools.script(
        "glpk_wrapper.sh", mps_out, options="--max", verbose=True
    )
    assert varvalues[profit] == 29
    glpkutils.mod2lp(mod_out, lp_out, verbose=True)
    out, varvalues = Tools.script("glpk_wrapper.sh", lp_out, verbose=True)
    assert varvalues[profit] == 29
