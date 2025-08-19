from flask import Flask,jsonify,request


app = Flask(__name__)


books = [
    {'id':1,'title':'Python 101'},
    {'id':2,'title':'Flask for Beginners'}
]

@app.route('/books',methods=['GET'])
def get_books():
    return jsonify(books)

@app.route('/books/<int:book_id>',methods=['GET'])
def get_book(book_id):
    book = next((b for b in books if['id'] == book_id),None)
    return jsonify(book) if book else (jsonify({'error':'Not found'}),404)

@app.route('/books',methods=['POST'])
def add_book():
    data = request.json
    new_book = {
        'id':books[-1]['id'] + 1 if books else 1,
        'title':data['title']
    }
    books.append(new_book)
    return jsonify(new_book),201

@app.route('/books/<int:book_id>',methods=['PUT'])
def update_book(book_id):
    book = next((b for b in books if b['id'] == book_id),None)
    if not book:
        return jsonify({'error':'Nont found'}),404
    data = request.json
    book['title'] = data.get('title',book['title'])
    return jsonify(book)

@app.route('/books/<int:book_id>',methods=['DELETE'])
def delete_book(book_id):
    global books
    books = [b for b in books if b['id'] != book_id]
    return jsonify({'message':'Deleted'}),204

if __name__ == "__main__":
    app.run(debug=True)