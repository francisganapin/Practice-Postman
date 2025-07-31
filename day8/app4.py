from flask import Flask,request,jsonify
import sqlite3

app = Flask(__name__)
DATABASE = 'qa.db'


def get_db_connections():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

app.route('/question',methods=['GET'])
def all_questions():
    conn = get_db_connections()
    questions = conn.execute('SELECT * FROM questions').fetchall()
    conn.close()
    return jsonify([dict(q) for q in questions])

@app.route('/questions',methods=['POST'])
def add_questions():