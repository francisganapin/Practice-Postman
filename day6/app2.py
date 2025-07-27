from flask import Flask,request,jsonify


from flask_jwt_extended import JWTManager,create_access_token,jwt_required,get_jwt_identity

app =  Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
jwt = JWTManager(app)

users = {'john':'password123'}

@app.route('/login',methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    if users.get(username) == password:
        token = create_access_token(identity=username)
        return jsonify(token=token)
    return jsonify({"msg":'invalid credentials'}),401

@app.route('/protected',methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user),200

if __name__ == '__main__':
    app.run(debug=True)