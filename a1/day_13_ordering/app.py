from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLACHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Order(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    customer_name = db.Column(db.String(100),nullable=False)
    order_date = db.Column(db.DateTime,default=datetime.timezone.utc)
    items = db.relationship('OrderItem',backref='order',cascade='all,delete-orphan')


class OrderItem(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    product_name = db.Column(db.String(100),nullable=False)
    quantity = db.Column(db.Integer,nullable=False)
    price = db.Column(db.Float,nullale=False)
    order_id = db.Column(db.Integer,db.ForeignKey('order.id'),nullable=False)


@app.route('/order',methods=['POST'])
def create_order():
    data = request.get_json()
    if not data or 'customer_name' not in data or 'item' not in data:
        return jsonify({'error':'Missing required field'}),400

    new_order = Order(customer_name=data['customer_name'])
    db.session.add(new_order)

    total_price = 0
    for item in data['items']:
        order_item = OrderItem(
            product_name=item['product_name'],
        )