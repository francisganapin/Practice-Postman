from flask import Flask,request,jsonify

app = Flask(__name__)

quiz_data = {
    1: {"question": "What is the capital of France?", "answer": "paris"},
    2: {"question": "What is 2 + 2?", "answer": "4"},
    3: {"question": "What color is the sky?", "answer": "blue"}
}


@app.route('/quiz/<int:qid>',methods=['GET'])
def get_question(qid):
    question = quiz_data.get(qid)
    if question:
        return jsonify({'id':qid,"question":question['question']}),200
    

@app.route('/quiz/<int:qid>/answer',methods=['POST'])
def check_answer(qid):
    user_input = request.json.get("answer", "").strip().lower()
    correct_answer = quiz_data.get(qid, {}).get("answer")

    if not correct_answer:
        return jsonify({'error':f'invalid question id {qid}'}),404
    
    if user_input == correct_answer.lower():
        return jsonify({'result':"correct"})
    else:
        return jsonify({"result":'wrong answer try again'})
    
if __name__ == '__main__':
    app.run(debug=True)