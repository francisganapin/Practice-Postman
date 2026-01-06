from flask import Flask,request,jsonify
import requests

app = Flask(__name__)

@app.route('/flask-webhook',methods=['POST'])
def flask_webhook():
    data = request.json
    print("Flask recieved",data)

    n8n_url = "http://localhost:5678/webhook-test/4fda613f-eb5d-4a63-9e77-84260301d87b"
    r = requests.post(n8n_url, json=data)

    return jsonify({'status':'success','n8n_response':r.text}),200

if __name__ == '__main__':
    app.run(port=5001,debug=True)