from flask import Flask,request,jsonify
import sqlite3


app = Flask(__name__)
database = 'chatbot'


def get_db_connection():
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row
    return conn


#Initialize table
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXIST MESSAGE(
        
        )
    ''')