from flask import Flask,jsonify,request

from datetime import datetime

app = Flask(__name__)


@app.route('/fruits',methods=['POST'])
def show_fruits():
    my_fruits = ['apple','banana','mango']

    data = request.get_json()
    fruit_to_check = data.get('fruit') if data else None


    if fruit_to_check is None:
        return "Send a fruit in Json, e.g, {'fruit':'orange'}"
    
    if fruit_to_check in my_fruits:
        return f"We have {fruit_to_check}"
    else:
        return f"No {fruit_to_check} in stock."
    
@app.route('/age-check')
def age_check():
    age = request.args.get('age',type=int)

    if age is None:
        return 'Please provide your age in The Url, e.g., ?age=20'
    elif age >= 18:
        return 'You are an adult'
    else:
        return "Your are a minor"


@app.route('/colors')
def colors():
    favorite = request.args.get('color','none').lower()
    available_colors = ['red','blue','green']

    if favorite in available_colors:
        return f"We have {favorite}!"
    else:
        return f"Sorry, {favorite} is not available."



@app.route('/login')
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    if username:
        if password:
            if username == "admin" and password == '1234':
                return "Login successful!"
            else:
                return "Incorrect username or password."
        else:
            return "Password is required."
    else:
        return "Username is required"
if __name__ == "__main__":
    app.run(debug=True)