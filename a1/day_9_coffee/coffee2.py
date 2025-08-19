from flask import Flask,request,jsonify
from coffee_model import db,Coffee,Order


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coffee_shop.db'
app.config['SQLALCHMEY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return 'Welcome to the Coffee Shop API!'


#Get list of all Coffee
@app.route('/coffees',methods=['GET'])
def get_coffees():
    coffees = Coffee.query.all()
    return jsonify([{'id':c.id,'name':c.name,'price':c.price} for c in coffees])

#get single list of coffee
@app.route('/coffees/id/<int:coffee_id>',methods=['GET'])
def get_coffee(coffee_id):
    coffees = Coffee.query.get_or_404(coffee_id)
    return jsonify({'id':coffees.id,'name':coffees.name,'price':coffees.price})

@app.route('/coffees/add',methods=['POST'])
def add_coffee():
    data = request.json
    coffee = Coffee(name=data['name'],price=data['price'])
    db.session.add(coffee)
    db.session.commit()
    return jsonify({'id':coffee.id,'name':coffee.name,'price':coffee.price}),201

@app.route('/coffees/update/<int:coffee_id>',methods=['PUT'])
def update_coffee(coffee_id):
    coffee = Coffee.query.get_or_404(coffee_id)
    data = request.json
    coffee.name = data['name']
    coffee.price = data['price']
    db.session.commit()
    return jsonify({"message":"coffee updated"})


@app.route('/coffees/delete/<int:coffee_id>',methods=['DELETE'])
def delete_coffee(coffee_id):
    coffee = Coffee.query.get_or_404(coffee_id)
    coffee_name = coffee.name # get the name before deletation
    db.session.delete(coffee)
    db.session.commit()
    return jsonify({'message':'Coffee Deleted',
                    "id":coffee_id,
                    'name':coffee_name})

@app.route('/orders',methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([
        {
            'id':o.id,
            'coffee_id':o.coffee_id,
            'coffee_name':o.quantity
        }for o in orders
    ])

@app.route('/orders',methods=['POST'])
def add_order():
    data = request.json
    order = Order(coffee_id=data['coffee_id'],quantity=data['quantity'])
    db.session.add(order)
    db.session.commit()
    return jsonify({"id":order.id,'coffee_id':order.coffee_id,'quantity':order.quantity}),201


@app.route('/orders/order/<int:order_id>',methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message':"Order Deleted"})

if __name__ == '__main__':
    app.run(debug=True)