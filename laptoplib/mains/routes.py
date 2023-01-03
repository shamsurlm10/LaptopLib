from datetime import datetime

from flask import (Blueprint, redirect, render_template, request, session,
                   url_for)
from flask.helpers import flash
from flask_login import current_user, login_required
from flask_login import login_user as login_user_function
from flask_login import logout_user as logout_user_function
from sqlalchemy.sql import text

from laptoplib import app, bcrypt, db
from laptoplib.models import Laptop, Rent, User, Transaction
from laptoplib.users.forms import Credit, GiftForm, LoginForm, RegisterForm, GiftForm, CheckoutFrom

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
    gift_form = GiftForm()
    if gift_form.validate_on_submit():
        gifts = gift_form.amount.data
        email = gift_form.email.data
        receiver = User.query.filter_by(email=email).first()
        if current_user.credits-gifts < 0:
            return render_template("mains/error.html", status=401, message="Insufficient Credit")

        current_user.credits = current_user.credits - gifts
        receiver.credits = receiver.credits + gifts
        db.session.commit()
        return redirect(url_for('mains.profile', id=current_user.id))

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
        credit_form=credit_form, gift_form=gift_form)


@mains.route("/explore")
def explore():
    laptops=Laptop.query.all()
    return render_template("mains/explore.html", laptops=laptops)

@mains.route("/checkout/<int:laptop_id>", methods=['POST', 'GET'])
@login_required
def checkout(laptop_id: int):
    checkout_form = CheckoutFrom()
    laptop = Laptop.query.get(laptop_id)
    if not laptop:
        return render_template("mains/error.html", status=404, message="Laptop not found!")
    if checkout_form.validate_on_submit():
        rented = Rent.query.filter_by(user_id=current_user.id, return_duration=None).first()
        if rented:
            return redirect(url_for('mains.profile', id=current_user.id))
        q1 = """CREATE OR REPLACE FUNCTION public.update_laptop_availability()
            RETURNS trigger
            LANGUAGE 'plpgsql'
            COST 100
            VOLATILE NOT LEAKPROOF
        AS $BODY$
        BEGIN
        UPDATE public."laptop"
        SET is_available = (NEW.rent_time IS NULL)
        WHERE id = NEW.laptop_id;
        RETURN NULL;
        END;
        $BODY$;
        ALTER FUNCTION public.update_laptop_availability()
            OWNER TO postgres;
        """
        db.engine.execute(text(q1))
        sql = f'UPDATE laptop SET is_available = FALSE WHERE id = {laptop.id}'
        db.engine.execute(sql)
        duration = checkout_form.duration.data
        rent = Rent(duration, laptop_id, current_user.id)
        db.session.add(rent)
        db.session.commit()
        print("success")
    
    return render_template("mains/checkout.html", laptop=laptop, checkout_form=checkout_form)

@mains.route("/return-laptop/<int:rent_id>", methods=['POST'])
@login_required
def returnLaptop(rent_id: int):
    rent = Rent.query.get(rent_id)
    if not rent:
        return render_template("mains/error.html", status=404, message="Rent object not found!")
    
    days = request.form.get('days')
    query = """
        CREATE OR REPLACE FUNCTION public.total_rate(
        duration numeric,
        return_duration numeric,
        rate numeric
    )
        RETURNS numeric
        LANGUAGE 'plpgsql'
        COST 100
        VOLATILE PARALLEL UNSAFE
    AS $BODY$
    DECLARE
        diff NUMERIC;
    BEGIN
        IF duration < return_duration THEN
            diff := return_duration - duration;
            RETURN duration*rate + diff*rate;
        ELSE
            RETURN duration*rate;
        END IF;
    END;
    $BODY$;

    ALTER FUNCTION public.total_rate(numeric, numeric, numeric)
    OWNER TO postgres;


    CREATE OR REPLACE PROCEDURE public.update_user_credits(
        id numeric,
        duration numeric,
        return_duration numeric,
        rate numeric,
        lap_id numeric
    )
    LANGUAGE 'plpgsql'
    AS $BODY$
    DECLARE
        user_id NUMERIC;
    BEGIN
        user_id:=id;
        UPDATE public."user"
        SET credits = credits - total_rate(duration, return_duration, rate)
        WHERE public."user".id = user_id;
        UPDATE public."laptop" SET is_available= TRUE where public."laptop".id = lap_id;
    END;
    $BODY$;
    ALTER PROCEDURE public.update_user_credits(numeric, numeric, numeric, numeric, numeric)
        OWNER TO postgres;
    """
    # query1_formatted = """CALL public.update_user_credits(13, 32, 20, 83);"""
    query1 = """CALL public.update_user_credits({}, {}, {}, {}, {});"""
    query1_formatted = query1.format(current_user.id, rent.duration, days, rent.rented_laptop.rate, rent.laptop_id)
    # print("--------")
    # print(query1_formatted)
    db.engine.execute(query+query1_formatted)

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


    