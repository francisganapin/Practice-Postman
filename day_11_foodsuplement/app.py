from flask import Flask,jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


#get all top selling item
@app.route('/top-selling',methods=['GET'])
def top_selling():
    conn = get_db_connection()
    query = '''
            SELECT p.name,SUM(s.quantity) as total_sold
            FROM sales s
            JOIN products p ON s.product_id = p.product_id
            GROUP BY p.name
            ORDER BY total_sold DESC
            LIMIT 1;
            '''
    top = conn.execute(query).fetchone()
    conn.close()
    
    if top is None:
        return jsonify({"message":"No sales Data Available"}),404



#query all item
@app.route('/product/all',methods=['GET'])
def get_all_product():
    conn = get_db_connection()
    query = 'SELECT * FROM products'
    products = conn.execute(query).fetchall()
    conn.close()

    if products is None:
        return jsonify({'message':'Product not Found'}),404
    
    product_list = [dict(row) for row in products]
    return jsonify(product_list)

#query item id
@app.route('/product/id/<int:id>',methods=['GET'])
def get_product_by_id(id):
    conn = get_db_connection()
    query = 'SELECT * FROM products WHERE product_id = ?'
    product = conn.execute(query,(id,)).fetchone()
    conn.close()


    if product is None:
        return jsonify({"message":'Product not Found'}),404
    
    return jsonify(dict(product))
    
if __name__ == '__main__':
    app.run(debug=True)