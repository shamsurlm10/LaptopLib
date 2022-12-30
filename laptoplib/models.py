from datetime import date, datetime
from flask_login import UserMixin
from laptoplib import app, db, login_manager

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())
    credits = db.Column(db.Integer, default=2000)

    rents = db.relationship("Rent", backref="rented_by")

    def __init__(
        self, email: str, password: str
    ) -> None:
        self.email = email
        self.password = password

    def get_joindate(self):
        return self.created_at.strftime("%B, %Y")


class Laptop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String, nullable=False)
    serial_number = db.Column(db.String, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    rate = db.Column(db.Integer, default=50)

    rents = db.relationship("Rent", backref="rented_laptop")

    def __init__(
        self, model: str, serial_number: str
    ) -> None:
        self.model = model
        self.serial_number = serial_number

class Rent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rent_time = db.Column(db.DateTime, default=datetime.utcnow())
    duration = db.Column(db.Integer, default=5)


    laptop_id = db.Column(db.Integer, db.ForeignKey("laptop.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


    def __init__(
        self, laptop_id: int, user_id: int
    ) -> None:
        self.laptop_id = laptop_id
        self.user_id = user_id