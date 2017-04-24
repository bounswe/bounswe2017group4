#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__)

books = [
    {
        'id': 1,
        'name': u'Brave New World',
        'author': u'Aldous Huxley',
        'price': 13.5
    },
    {
        'id': 2,
        'name': u'Fight Club',
        'author': u'Chuck Palahniuk',
        'price': 8.5
    }
]

auth = HTTPBasicAuth()

@app.route('/api/books', methods=['GET'])
@auth.login_required
def get_books():
    return jsonify({'books': books})

@app.route('/api/books/<int:book_id>', methods=['GET'])
@auth.login_required
def get_book(book_id):
    book = [book for book in books if book['id'] == book_id]
    if len(book) == 0:
        abort(404)
    return jsonify({'book': book[0]})

@app.route('/api/books', methods=['POST'])
@auth.login_required
def create_book():
    if not request.json or not 'name' in request.json or not 'author' in request.json or not 'price' in request.json:
        abort(400)
    book = {
        'id': books[-1]['id'] + 1,
        'name': request.json['name'],
        'author': request.json['author'],
        'price': request.json['price'],
    }
    books.append(book)
    return jsonify({'book': book}), 201

@app.route('/api/books/<int:book_id>', methods=['PUT'])
@auth.login_required
def update_book(book_id):
    book = [book for book in books if book['id'] == book_id]
    if len(book) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) is not unicode:
        abort(400)
    if 'author' in request.json and type(request.json['author']) is not unicode:
        abort(400)
    if 'price' in request.json and type(request.json['price']) is not float:
        abort(400)
    book[0]['name'] = request.json.get('name', book[0]['name'])
    book[0]['author'] = request.json.get('author', book[0]['author'])
    book[0]['price'] = request.json.get('price', book[0]['price'])
    return jsonify({'book': book[0]})

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
@auth.login_required
def delete_book(book_id):
    book = [book for book in books if book['id'] == book_id]
    if len(book) == 0:
        abort(404)
    books.remove(book[0])
    return jsonify({'result': True})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

@auth.get_password
def get_password(username):
    if username == 'berkerol':
        return 'group4'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

if __name__ == '__main__':
    app.run(debug=True)