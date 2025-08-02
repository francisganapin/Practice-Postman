from flask import Flask,request,jsonify
from database import get_db_connections,create_table

app = Flask(__name__)
create_table()

@app.route('/phones',methods=['POST'])
def add_phone():
    data = request.get_json()
    brand = data.get('brand')
    model = data.get('model')
    price = data.get('price')
    stock = data.get('stock')

    #make the all input complete
    if not all([brand,model,price,stock]):
        return jsonify({'error':'All field are required'}),400
    
    conn = get_db_connections()
    conn.execute('INSERT INTO PHONES (brand,model,price,stock) VALUES(?,?,?,?)',
    (brand,model,price,stock))
    
    conn.commit()
    conn.close()

    return jsonify({'message':"Phone added successfully"}),201


#get all phones
@app.route('/phones',methods=['GET'])
def get_phones():
    conn = get_db_connections()
    phones = conn.execute('SELECT * FROM phones').fetchall()
    conn.close()

    return jsonify([dict(row) for row in phones])


# get a single phone
@app.route('/phones/<int:phone_id>',methods=['GET'])
def get_phone(phone_id):
    conn = get_db_connections()
    phone = conn.execute('SELECT * FROM phone WHERE id = ?',(phone_id,)).fetchone()
    conn.close()

    if phone is None:
        return jsonify({'error':'Phone not Found'}),404
    
    return jsonify(dict(phone))


# Update a phone
@app.route('/phone/<int:phone_id>',methods=['PUT'])
def update_phone(phone_id):
    data = request.get_json()
    brand = data.get('brand')
    model = data.get('model')
    price = data.get('price')
    stock = data.get('stock')

    conn = get_db_connections()
    phone = conn.execute('SELECT * FROM phone WHERE id = ?',(phone,id)).fetchone()

    if phone is None:
        conn.close()
        return jsonify({"error":'Phone Not Found'}),404
    

    conn.execute('''
            UPDATE phones
            SET brand = ?, model = ? ,price = ?, stock = ?

        ''',(brand,model,price,stock,phone_id))
    conn.commit()
    conn.close()

    return jsonify({'message':"Phone updated successfully"})

#delete a phone
@app.route('/phone/<int:phone_id>',methods=['DELETE'])
def delete_phone(phone_id):
    conn = get_db_connections()
    conn.execute('DELETE FROM phone WHERE id = ?',(phone_id,))
    conn.execute()
    conn.close()
    return jsonify({"message":"Phone deleted Successfully"})


if __name__ == '__main__':
    app.run(debug=True)