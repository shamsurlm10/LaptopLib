from flask_wtf import FlaskForm
from wtforms import (EmailField, IntegerField, BooleanField, PasswordField, StringField, SubmitField)
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)
from laptoplib.models import User


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