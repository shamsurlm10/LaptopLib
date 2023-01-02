from datetime import date, datetime

from flask_login import UserMixin

from laptoplib import app, db, login_manager


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime, default=datetime.utcnow())
    balance = db.Column(db.Integer, default=10000)
    credits = db.Column(db.Integer, default=0)

    rents = db.relationship("Rent", backref="rented_by")
    transactions = db.relationship("Transaction", backref="sender")

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
    return_duration = db.Column(db.Integer, default=None)

    laptop_id = db.Column(db.Integer, db.ForeignKey("laptop.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(
        self, duration: int, laptop_id: int, user_id: int
    ) -> None:
        self.laptop_id = laptop_id
        self.user_id = user_id
        self.duration = duration

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    credit_amount = db.Column(db.Integer, default=5)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    sender_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    receiver_id = db.Column(db.Integer, nullable=False)


    def __init__(
        self, credit_amount:int, sender_id: int, receiver_id: int
    ) -> None:
        self.credit_amount = credit_amount
        self.sender_id = sender_id
        self.receiver_id = receiver_id