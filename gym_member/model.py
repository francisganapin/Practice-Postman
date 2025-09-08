from flask_sqlalchemy import SQLAlchemy
from datetime import date


db = SQLAlchemy()


class GymMember(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(100),nullable=False)
    last_name = db.Column(db.String(100),nullable=False)
    expiry = db.Column(db.Date,nullable=False,default=date.today)

    