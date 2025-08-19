from flask import Flask,request,jsonify

app = Flask(__name__)


@app.route('/greet/<name>',methods=['GET'])
def greet(name):
    return jsonify({'message',f'hi,{name}!'})

@app.route('/echo',methods=['POST'])
def echo():
    data = request.json
    return jsonify({'you_sent':data})


if __name__ == '__main__':
    app.run(debug=True)