from flask import Flask,request,jsonify

app = Flask(__name__)

users  = {
    'john':"password123",
    'jane':'mypassword'
}

@app.route('/')
def home():
    return jsonify({'message':'Welcome to the flask Login API!'})


@app.route('/login',methods=['POST'])
def login():
    data = request.json

    username = data.get('username')
    password = data.get('password')


    if username in users and users[username] == password:
        return jsonify({"message":"login successful!","user":username}),200
    else:
        return jsonify({'message':"invalid username or password"}),401


if __name__ == '__main__':
    app.run(debug=True)