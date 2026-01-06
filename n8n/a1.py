from flask import Flask,request,jsonify

app = Flask(__name__)

@app.route("/webhook-test/477f332f-62cb-4a1e-81af-83a249d5e866", methods=["GET", "POST"])
def webhook():
    data = request.args if request.method == 'GET' else request.get_json()

    print('Webhook Triggered!')
    print("Data recieved",data)

    return jsonify({"status": "success", "message": "Webhook received!"}), 200


if __name__ == '__main__':
    app.run(port=5000,debug=True)