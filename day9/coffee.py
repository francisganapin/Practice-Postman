from flask import Flask,request,jsonify
from coffee_model import db,Coffee,Order

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coffe_shop.db'
db.init_app(app)




with app.app_context():
    db.create_all()
    

@app.route('/coffee',methods=['GET'])
def get_coffee():
    coffees = Coffee.query.all()
    return jsonify([{'id':c.id,'name':c.name,'price':c.price} for c in coffees])


@app.route('/coffees',methods=['POST'])
def add_coffee():    
    data = request.get_json()
    coffee = Coffee(name=data['name'],price=data['price'])  
    db.session.add(coffee)
    db.session.commit()
    return jsonify({'id':coffee.id,'name':coffee.name,'price':coffee.price}),201

@app.route('/orders',methods=['POST'])
def place_order():
    data = request.get_json()
    order = Order(coffee_id=data['coffee_id'],quantity=data['quantity'])
    db.session.add(order)
    db.session.commit()
    return jsonify({
        'id':order.id,
        'coffee_id':order.coffee_id,
        'quantity':order.quantity
    }),201

if __name__ == '__main__':
    app.run(debug=True)