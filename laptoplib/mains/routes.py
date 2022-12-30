from flask import Blueprint, render_template, url_for
from flask.helpers import flash
from laptoplib import app

mains = Blueprint("mains", __name__)

@mains.route("/login")
def login():
    return render_template("mains/login.html")

@mains.route("/homepage")
@mains.route("/")
def homepage():
    return render_template("mains/homepage.html")

@mains.route("/explore")
def explore():
    return render_template("mains/explore.html")

@mains.route("/checkout")
def checkout():
    return render_template("mains/checkout.html")