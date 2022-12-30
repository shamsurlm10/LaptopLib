from flask import Blueprint, render_template, url_for
from flask.helpers import flash
from laptoplib import app

users = Blueprint("users", __name__)