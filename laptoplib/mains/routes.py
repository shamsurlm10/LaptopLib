from datetime import datetime

from flask import (Blueprint, redirect, render_template, request, session,
                   url_for)
from flask.helpers import flash
from flask_login import current_user, login_required
from flask_login import login_user as login_user_function
from flask_login import logout_user as logout_user_function
from sqlalchemy.sql import text

from laptoplib import app, bcrypt, db
from laptoplib.models import Laptop, Rent, User
from laptoplib.users.forms import Credit, GiftForm, LoginForm, RegisterForm

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
        if fetched_user and fetched_user.password == form.password.data:
            login_user_function(fetched_user, remember=form.remember_me.data)
            return redirect(url_for("mains.homepage"))
    return render_template("mains/login.html", form=form)

@mains.route("/registration", methods=['POST', 'GET'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('mains.homepage'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(form.email.data, form.password.data)
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

@mains.route("/credit", methods=['POST', 'GET'])
@login_required
def credit():
    credit_form = Credit()

    if credit_form.validate_on_submit():
        credits = credit_form.credit.data
        cost = 3*credits
        
        if current_user.balance-cost < 0:
            return render_template("mains/error.html", status=401, message="Insufficient balance")
            
        current_user.balance = current_user.balance - cost
        current_user.credits = current_user.credits + credits
        db.session.commit()
        return redirect(url_for('mains.profile', id=current_user.id))

    return render_template("mains/credit.html",
        credit_form=credit_form)


@mains.route("/explore")
def explore():
    laptops=Laptop.query.all()
    return render_template("mains/explore.html", laptops=laptops)

@mains.route("/checkout/<int:laptop_id>")
def checkout(laptop_id: int):
    laptop = Laptop.query.get(laptop_id)
    if not laptop:
        return render_template("mains/error.html", status=404, message="Laptop not found!")
    return render_template("mains/checkout.html", laptop=laptop)

@mains.route("/return-laptop/<int:rent_id>", methods=['POSt'])
@login_required
def returnLaptop(rent_id: int):
    rent = Rent.query.get(rent_id)
    if not rent:
        return render_template("mains/error.html", status=404, message="Rent object not found!")
    
    days = request.form.get('days')
    query = text(f'CALL public.update_user_credits({current_user.id}, {rent.duration}, {days}, {rent.rented_laptop.rate});')
    db.get_engine().execute(query)

    rent.return_duration = days
    rent.rented_laptop.is_available = True
    db.session.commit()
    return redirect(url_for("mains.profile", id=current_user.id))

@mains.route("/profile/<int:id>")
def profile(id: int):
    user = User.query.get(id)
    if not user:
        return render_template("mains/error.html", status=404, message="User not found!")
    
    rented = Rent.query.filter_by(user_id=user.id, return_duration=None).first()

    return render_template("mains/profile.html", user=user, rented=rented)