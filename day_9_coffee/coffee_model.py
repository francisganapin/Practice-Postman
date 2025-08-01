from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Coffee(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    price = db.Column(db.Float,nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coffee_id = db.Column(db.Integer, db.ForeignKey('coffee.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    coffee = db.relationship('Coffee')