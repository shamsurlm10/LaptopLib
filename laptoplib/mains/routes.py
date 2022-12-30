from flask import Blueprint, render_template, url_for
from flask.helpers import flash
from laptoplib import app

mains = Blueprint("mains", __name__)

@mains.route("/homepage")
@mains.route("/")
def homepage():
    return render_template("mains/homepage.html")