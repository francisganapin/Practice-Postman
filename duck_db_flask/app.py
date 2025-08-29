from flask import Flask,request,jsonify
import sqlite3


app = Flask(__name__)
conn = sqlite3.connect('mydata.db',check_same_thread=False)
cursor = conn.cursor()


cursor.execute("""
    CREATE TABLE IF NOT EXISTS members(
    id INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    status TEXT
    )
""")


@app.route('/members',methods=['GET'])
def get_members():
    data = conn.execute('SELECT * FROM members').fetchall()
    return jsonify(data)

@app.route('/members',methods=['POST'])
def add_member():
    member = request.json
    conn.execute('INSERT INTO members VALUES (?,?,?,?)',
        [member['id'],member['name'],member['age'],member['status']])
    return jsonify({"message":"Member added succesffully"}),201


@app.route('/member/<int:member_id>',methods=['GET'])
def get_member(member_id):
    data = conn.execute('SELECT * FROM members WHERE ID = ?',[member_id]).fetchone()
    if not data:
        return jsonify({"error":"Member not found"}),404
    return jsonify(data)



if __name__ == "__main__":
    app.run(debug=True)