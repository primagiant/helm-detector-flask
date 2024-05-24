from flask import render_template
from . import about


@about.route("/")
def index():
    return render_template("views/about.html")
