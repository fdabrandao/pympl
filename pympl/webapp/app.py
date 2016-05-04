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
from builtins import str
from builtins import object

import os
import sys
import string
import random
import flask
import signal
import shutil
import tempfile
from flask_limiter import Limiter
from flask import Flask, Response
from flask import render_template, json, request, redirect, url_for
from flask.ext.basicauth import BasicAuth

DEBUG = False
PORT = 5555
USERNAME = "PyMPL"
PASSWORD = "Password"

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1].isdigit():
        PORT = int(sys.argv[1])

    if len(sys.argv) >= 3:
        PASSWORD = sys.argv[2]

app = Flask(__name__)
app.debug = True
app.config["BASIC_AUTH_USERNAME"] = USERNAME
app.config["BASIC_AUTH_PASSWORD"] = PASSWORD
app.config["BASIC_AUTH_FORCE"] = True
basic_auth = BasicAuth(app)
limiter = Limiter(app, global_limits=["50/minute", "5/second"])


@app.context_processor
def inject_globals():
    """Send global data to the template."""
    data = dict(
        app_name="PyMPL App",
        pages=[
            ("/pympl", "PyMPL"),
        ],
    )
    return data


@app.route("/favicon.ico")
def favicon():
    """Favicon route."""
    return flask.send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico", mimetype='image/vnd.microsoft.icon'
    )


@app.route("/")
@basic_auth.required
def index():
    """Renders the index page."""
    return redirect(url_for("pympl"))


def load(fname):
    """Load a text file as a string."""
    with open(fname, "r") as f:
        return f.read().strip("\n")


def request_data():
    """Extract request info."""
    pympl_model = request.form["pympl_model"]
    python_code = request.form["python_code"]
    fnames = {}
    contents = {}

    for key in request.form:
        if key.startswith("fname"):
            ind = int(key.replace("fname", ""))
            fnames[ind] = request.form[key]
            if os.path.isabs(fnames[ind]) or ".." in fnames[ind]:
                fnames[ind] = "invalid file name"
        elif key.startswith("content"):
            ind = int(key.replace("content", ""))
            contents[ind] = request.form[key]

    if "addfile" in request.form:
        if fnames != {}:
            next_ind = max(fnames)+1
        else:
            next_ind = 1
        fnames[next_ind] = ""
        contents[next_ind] = ""

    files = [
        (ind, fnames[ind], contents[ind])
        for ind in sorted(fnames)
    ]
    return pympl_model, python_code, files


@app.route("/pympl/", defaults={"example": None}, methods=["GET", "POST"])
@app.route("/pympl/<example>", methods=["GET", "POST"])
@basic_auth.required
def pympl(example):
    """Render the input page."""
    title = "PyMPL: AMPL extension"

    example_folder = os.path.join(
        os.path.dirname(__file__), "data", "examples"
    )
    examples = {
        "/pympl/": ("", "", None, []),
        "/pympl/vbp": (
            "Vector Packing",
            ("vector_packing.mod", "default.py", [])
        ),
        "/pympl/vsbpp": (
            "Variable Sized Bin Packing",
            ("variable_size_bin_packing.mod", "default.py", [])
        ),
        "/pympl/pwl": (
            "Piecewise Linear Function",
            ("piecewise_linear.mod", "default.py", [])
        ),
        "/pympl/ppbymip_bike": (
            "PPbyMIP: Bike",
            ("ppbymip_bike.mod", "ppbymip.py", [])
        ),
        "/pympl/ppbymip_cgp": (
            "PPbyMIP: Consumer Goods Production",
            ("ppbymip_cgp.mod", "ppbymip.py", [
                os.path.join("data", "cgpdemand.dat"),
            ])
        ),
        "/pympl/ppbymip_clb": (
            "PPbyMIP: Cleaning Liquids Bottling Line",
            ("ppbymip_clb.mod", "ppbymip.py", [
                os.path.join("data", "cldemand.dat"),
            ])
        ),
        "/pympl/ppbymip_ps": (
            "PPbyMIP: Pigment Sequencing",
            ("ppbymip_ps.mod", "ppbymip.py", [
                os.path.join("data", "pigment_dem.dat"),
                os.path.join("data", "pigment_q.dat"),
            ])
        ),
        "/pympl/ppbymip_mp": (
            "PPbyMIP: Making and Packing",
            ("ppbymip_mp.mod", "ppbymip.py", [
                os.path.join("data", "mp_daily_demand.dat"),
                os.path.join("data", "mp_making_production_rate.dat"),
                os.path.join("data", "mp_packing_production_rate.dat"),
            ])
        ),
    }
    examples_list = sorted(examples)

    if request.method == "POST":
        pympl_model, python_code, files = request_data()
    else:
        pympl_model = ""
        python_code = ""
        files = []
        if example is not None:
            modelf, codef, flist = examples["/pympl/"+example][1]
            if modelf is not None:
                pympl_model = open(os.path.join(example_folder, modelf)).read()
            if codef is not None:
                python_code = open(os.path.join(example_folder, codef)).read()
            for ind, fname in enumerate(flist):
                content = open(os.path.join(example_folder, fname)).read()
                files.append((ind+1, fname, content))

    return render_template(
        "input.html",
        title=title,
        examples=examples,
        examples_list=examples_list,
        pympl_model=pympl_model,
        python_code=python_code,
        files=files,
        evaluator_url="/evaluate",
    )


class StringStream(object):
    """Simple string stream."""
    def __init__(self):
        self.data = ""

    def write(self, s):
        self.data += s


@app.route("/evaluate", methods=["POST"])
@limiter.limit("250/hour;50/minute;3/second")
@basic_auth.required
def evaluate():
    """Render the evaluation page."""
    from flask import make_response
    tmp_dir = tempfile.mkdtemp()
    try:
        pympl_model, python_code, files = request_data()

        with open(os.path.join(tmp_dir, "model.mod"), "w") as f:
            f.write(pympl_model)

        for ind, path, contents in files:
            path.replace(" ", "\\ ")
            if path != "":
                path = os.path.join(tmp_dir, path)
                dname = os.path.dirname(path)
                if dname != "" and not os.path.exists(dname):
                    os.makedirs(dname)
                with open(path, "w") as f:
                    f.write(contents)

        with open(os.path.join(tmp_dir, "main.py"), "w") as f:
            f.write(python_code)

        from subprocess import Popen, PIPE, STDOUT
        output = Popen(
            ["python", "main.py"], cwd=tmp_dir,
            stdout=PIPE, stderr=STDOUT,
        ).communicate()[0]

        shutil.rmtree(tmp_dir)

        if "download" in request.form:
            response = make_response(output)
            header = "attachment; filename=output.mod"
            response.headers["Content-Disposition"] = header
            return response
        else:
            response = make_response(output)
            response.mimetype = "text/plain"
            return response

    except Exception as e:
        shutil.rmtree(tmp_dir)
        raise


def get_ip_address():
    """Return the ip address of 'eth0'."""
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


if __name__ == "__main__":
    print("URL: http://{0}:{1}/".format(get_ip_address(), PORT))
    print("USERNAME: {0}".format(USERNAME))
    print("PASSWORD: {0}".format(PASSWORD))
    app.run(host="0.0.0.0", port=PORT, threaded=True)
