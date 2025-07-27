from flask import Flask,jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to my Flask Api'

@app.route('/api/hello',methods=['GET'])
def hello():
    return jsonify({'message':'Hello,World'})

if __name__ == '__main__':
    app.run(debug=True)