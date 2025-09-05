import requests
from flask import Flask

app = Flask(__name__)

@app.route('/check-post')
def check_post():
    url = "https://jsonplaceholder.typicode.com/posts/1"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data.get('id'):
            return f'Post Found: {data['title']}'
        else:
            return "Post Has no ID"
    else:
        return f"Failed to fetch Api. Status: {response.status_code}"
    

if __name__ == '__main__':
    app.run(debug=True)