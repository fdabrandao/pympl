#!/bin/bash
# This code is part of the Mathematical Programming Toolbox PyMPL.
#
# Copyright (C) 2015-2015, Filipe Brandao
# Faculdade de Ciencias, Universidade do Porto
# Porto, Portugal. All rights reserved. E-mail: <fdabrandao@dcc.fc.up.pt>.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
BASEDIR=`dirname $0`
cd $BASEDIR
CMD="$0 $*"

error(){
    echo "Command line: "$CMD
    echo "Error: invalid arguments."
    exit 1
}

venv=""
options=""

while true;
do
  case "$1" in
    --venv)
        if [[ -n "$2" ]]; then venv=$2; else error; fi
        shift 2;;
    --options)
        if [[ -n "$2" ]]; then options=$2; else error; fi
        shift 2;;
    *)
        if [[ -n "$1" ]]; then error; else break; fi
  esac
done

if [[ -n "$venv" ]]; then
    source $venv/bin/activate;
fi;

python examples/test.py $options         || exit 1
python examples/test_ppbymip.py $options || exit 1
python examples/unittests.py $options    || exit 1
