from extensions import db
from datetime import date

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50),unique=True,nullable=False)
    password = db.Column(db.String(200),nullable=False)


class GymMember(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    first_name  = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50),nullable=False)
    expiry = db.Column(db.Date,default=date.today)