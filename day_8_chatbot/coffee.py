from flask import Flask,jsonify,request,abort

app = Flask(__name__)

coffee_products = {
    1:{'name':"Espress",'price':2.99,'description':'strong and black'},
    2:{'name':"Cappucino",'price':3.99,'description':'with steamed milk foam'},
    3:{'name':'Latter','price':4.49,'description':'Mild with Milk'}
}

def get_next_id():
    return max(coffee_products.keys(),default=0) + 1

#get all coffee product
@app.route('/coffee',methods=['GET'])
def get_coffees():