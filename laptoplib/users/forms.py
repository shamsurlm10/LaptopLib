from flask_wtf import FlaskForm
from wtforms import (EmailField, IntegerField, BooleanField, PasswordField, SubmitField)
from wtforms.validators import (DataRequired, EqualTo, Length,)


class RegisterForm(FlaskForm):
    email = EmailField("Email Address", validators=[
        DataRequired(), Length(min=4, max=150)
    ], render_kw={"placeholder": "Email"})
    
    password = PasswordField("Password", validators=[
        DataRequired(), Length(min=6)
    ], render_kw={"placeholder": "Password"})
    
    c_password = PasswordField("Confirm Password", validators=[
        DataRequired(), Length(min=6), EqualTo(
            "password", "Confirm password did not matched")
    ], render_kw={"placeholder": "Confirm Password"})
    
    condition_check = BooleanField("Accept terms and conditions", validators=[
        DataRequired()])
    
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = EmailField("Email Address", validators=[
        DataRequired(), Length(min=4, max=150)
    ], render_kw={"placeholder": "Email"})
    
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)],
                             render_kw={"placeholder": "Password"})
    
    remember_me = BooleanField("Remember Me")
    
    submit = SubmitField("Login")

class Credit(FlaskForm):
    credit = IntegerField("Credit", validators=[
        DataRequired(), Length(min=1, max=150)
    ], render_kw={"placeholder": "Credit"})

    buy = SubmitField("Buy")

    gift_to = EmailField("Email", validators=[
        DataRequired(), Length(min=4, max=150)
    ], render_kw={"placeholder": "Email"})

    amount = credit = IntegerField("Amount", validators=[
        DataRequired(), Length(min=1, max=150)
    ], render_kw={"placeholder": "Enter Amount"})
    
    gift = SubmitField("Gift")