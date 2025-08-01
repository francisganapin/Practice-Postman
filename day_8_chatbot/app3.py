from flask import Flask,request,jsonify
import sqlite3

app = Flask(__name__)

DATABASE = 'sales.db'


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Endpoint to get what was sold on given date or find an item
@app.route('/sales',methods=['GET'])
def get_sales():
    item = request.args.get('item')
    date = request.args.get('date')
    
    conn = get_db_connection()
    c = conn.cursor()
    query = 'SELECT * FROM sales WHERE 1=1'
    params = []
    if item:
        query += " AND ITEM = ?"
        params = []
    if item:
        query += "AND item = ?"
        params.append(item)
    if date:
        query += "AND sale_date = ?"
        params.append(date)
    c.execute(query,params)
    rows = c.fetchall()
    conn.close()

    sales = [dict(row)for row in rows]
    return jsonify(sales)


if __name__ == "__main__":
    app.run(debug=True)