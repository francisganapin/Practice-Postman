from flask import Flask,request,jsonify
import sqlite3



app = Flask(__name__)
DATABASE = 'chatbot.db'



#connection util to 
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            message TEXT NOT NULL,
            response TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return 'Chatbot Api is Running'

@app.route('/chat',methods=['POST'])
def chat():
    data = request.get_json()
    user = data.get('user','anonymous')
    message = data.get('message')

    if not message:
        return jsonify({'error':'Message is required'}),400
    
    response = f'you Said:{message}'

    #Save to DB
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO messages (user,message,response) values(?,?,?)',
        (user,message,response)
    )
    conn.commit()
    conn.close()
    return jsonify({'user':user,'message':message,'response':response})

@app.route('/history',methods=['GET'])
def history():
    conn = get_db_connection()
    messages = conn.execute('SELECT * FROM message').fetchall()
    conn.close()

    result = [
        {'id': row['id'], 'user': row['user'], 'message': row['message'], 'response': row['response']}
        for row in messages
    ]
    return jsonify(result)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)