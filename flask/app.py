from flask import Flask,jsonify
import requests
from datetime import datetime

app = Flask(__name__)

url = 'https://jsonplaceholder.typicode.com/comments?postId=1'

@app.route('/fetch-comments')
def fetch_comment():
    
    response = requests.get(url)

    data = response.json()

    return jsonify(data)


@app.route('/show-comment')
def show_comment():
    
    response = requests.get(url)
    data = response.json()

    result = ''
    
    for comment in data:
        result += f"Name: {comment['name']}<br> Email: {comment['email']}<br><br>"
    
    return result

@app.route('/show-body')
def show_body():

    response = requests.get(url)
    data = response.json()

    if data:
        result = ""
        for body in data:
            result += f"body:{body['body']}<br> Email:{body['email']}<br><br>"
            return result
    else:
        return 'No body found'
    

@app.route('/greet')
def greet():
    hour = datetime.now().hour

    if hour < 12:
        return "Good Morning!"
    elif 12 <= hour  <= 18:
        return 'Good Afternoon!'
    else:
        return "Good evening!"
    
@app.route('/fruits')
def show_fruits():
    my_fruits = ['apple','banana','mango']

    if "orange" in my_fruits:
        return "We have orange!"
    else:
        return "No orange in stock"



if __name__ == '__main__':
    app.run(debug=True)