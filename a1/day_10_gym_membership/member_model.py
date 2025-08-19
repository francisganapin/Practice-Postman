from typing import Optional
from sqlmodel import SQLModel,Field
from datetime import date
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    start_date = db.Column(db.Date, nullable=False)

