import os
from flask import Blueprint, render_template, url_for, redirect, request, session
from flask_login import current_user
from flask_login import login_user as login_user_function
from flask_login import logout_user as logout_user_function
from flask.helpers import flash
from laptoplib import bcrypt, db
from laptoplib import app
from laptoplib.models import User, Laptop, Rent
from laptoplib.users.forms import (LoginForm, RegisterForm)

mains = Blueprint("mains", __name__)

@mains.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('mains.homepage'))
    form = LoginForm()
    if form.validate_on_submit():
        # Fetching the user
        fetched_user = User.query.filter_by(email=form.email.data).first()
        # Checking the email and password
        if fetched_user and bcrypt.check_password_hash(fetched_user.password, form.password.data):
            login_user_function(fetched_user, remember=form.remember_me.data)
            return redirect(url_for("mains.homepage"))
    return render_template("mains/login.html", form=form)

@mains.route("/registration", methods=['POST', 'GET'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('mains.homepage'))
    form = RegisterForm()
    if form.validate_on_submit():
        # Hashing
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        user = User(form.email.data, hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("mains.login"))
    return render_template("mains/registration.html", form = form)

@mains.route("/logout")
def logout():
    if not current_user.is_authenticated:
        return redirect(url_for('mains.login'))
    logout_user_function()
    return redirect(url_for("mains.login"))

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