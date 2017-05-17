#!flask/bin/python
import hashlib
from flask import Flask, jsonify, abort, make_response, request
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)

auth = HTTPBasicAuth()

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

comments = [
    {
        'id': 1,
        'book': 1,
        'owner': 1,
        'content': u'Such an enlightening book.'
    },
    {
        'id': 2,
        'book': 1,
        'owner': 2,
        'content': u'Great book. Similar to 1984, only more realistic.'
    },
    {
        'id': 3,
        'book': 2,
        'owner':1,
        'content': u'Very interesting.'
    }
]

users = [
    {
        'id': 1,
        'name': u'nicholasramsey'
    },
    {
        'id': 2,
        'name': u'richardterry'
    }
]

templates = [
    {
        'id': 1,
        'name': u'Asking name',
        'in': [u'My name is $UserName', u'I am $UserName'],
        'out': [u'Hello $UserName.', u'Nice to meet you $UserName!']
    },
    {
        'id': 2,
        'name': u'Asking book',
        'in': [u'I want to search books about $Genre', u'Can you show me the books about $Genre'],
        'out': [u'Here are some books about $Genre. Do you want to keep searching?']
    }
]

admins = {
    "group4": "33275a8aa48ea918bd53a9181aa975f15ab0d0645398f5918a006d08675c1cb27d5c645dbd084eee56e675e25ba4019f2ecea37ca9e2995b49fcb12c096a032e",
    "berkerol": "ba3253876aed6bc22d4a6ff53d8406c6ad864195ed144ab5c87621b6c233b548baeae6956df346ec8c17f5ea10f35ee3cbc514797ed7ddd3145464e2a0bab413"
}

@app.route('/api/books', methods=['GET'])
@auth.login_required
def get_books():
    return jsonify({'books': books})

@app.route('/api/comments', methods=['GET'])
@auth.login_required
def get_comments():
    return jsonify({'comments': comments})

@app.route('/api/users', methods=['GET'])
@auth.login_required
def get_users():
    return jsonify({'users': users})

@app.route('/api/templates', methods=['GET'])
@auth.login_required
def get_templates():
    return jsonify({'templates': templates})

@app.route('/api/comments/book/<int:book_id>', methods=['GET'])
@auth.login_required
def get_comments_of_book(book_id):
    comment = [comment for comment in comments if comment['book'] == book_id]
    if len(comment) == 0:
        abort(404)
    return jsonify({'comments': comment})

@app.route('/api/comments/user/<int:user_id>', methods=['GET'])
@auth.login_required
def get_comments_of_user(user_id):
    comment = [comment for comment in comments if comment['owner'] == user_id]
    if len(comment) == 0:
        abort(404)
    return jsonify({'comments': comment})

@app.route('/api/books/<int:book_id>', methods=['GET'])
@auth.login_required
def get_book(book_id):
    book = [book for book in books if book['id'] == book_id]
    if len(book) == 0:
        abort(404)
    return jsonify({'book': book[0]})

@app.route('/api/comments/<int:comment_id>', methods=['GET'])
@auth.login_required
def get_comment(comment_id):
    comment = [comment for comment in comments if comment['id'] == comment_id]
    if len(comment) == 0:
        abort(404)
    return jsonify({'comment': comment[0]})

@app.route('/api/users/<int:user_id>', methods=['GET'])
@auth.login_required
def get_user(user_id):
    user = [user for user in users if user['id'] == user_id]
    if len(user) == 0:
        abort(404)
    return jsonify({'user': user[0]})

@app.route('/api/templates/<int:template_id>', methods=['GET'])
@auth.login_required
def get_template(template_id):
    template = [template for template in templates if template['id'] == template_id]
    if len(template) == 0:
        abort(404)
    return jsonify({'template': template[0]})

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

@app.route('/api/comments', methods=['POST'])
@auth.login_required
def create_comment():
    if not request.json or not 'book' in request.json or not 'owner' in request.json or not 'content' in request.json:
        abort(400)
    comment = {
        'id': comments[-1]['id'] + 1,
        'book': request.json['book'],
        'owner': request.json['owner'],
        'content': request.json['content'],
    }
    comments.append(comment)
    return jsonify({'comment': comment}), 201

@app.route('/api/users', methods=['POST'])
@auth.login_required
def create_user():
    if not request.json or not 'name' in request.json:
        abort(400)
    user = {
        'id': users[-1]['id'] + 1,
        'name': request.json['name'],
    }
    users.append(user)
    return jsonify({'user': user}), 201

@app.route('/api/templates', methods=['POST'])
@auth.login_required
def create_template():
    if not request.json or not 'name' in request.json or not 'in' in request.json or not 'out' in request.json:
        abort(400)
    template = {
        'id': templates[-1]['id'] + 1,
        'name': request.json['name'],
        'in': request.json['in'],
        'out': request.json['out'],
    }
    templates.append(template)
    return jsonify({'template': template}), 201

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

@app.route('/api/templates/<int:template_id>', methods=['PUT'])
@auth.login_required
def update_template(template_id):
    template = [template for template in templates if template['id'] == template_id]
    if len(template) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) is not unicode:
        abort(400)
    if 'in' in request.json and type(request.json['in']) is not list:
        abort(400)
    if 'out' in request.json and type(request.json['out']) is not list:
        abort(400)
    template[0]['name'] = request.json.get('name', template[0]['name'])
    template[0]['in'] = request.json.get('in', template[0]['in'])
    template[0]['out'] = request.json.get('out', template[0]['out'])
    return jsonify({'template': template[0]})

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
@auth.login_required
def delete_book(book_id):
    book = [book for book in books if book['id'] == book_id]
    if len(book) == 0:
        abort(404)
    books.remove(book[0])
    return jsonify({'result': True})

@app.route('/api/templates/<int:template_id>', methods=['DELETE'])
@auth.login_required
def delete_template(template_id):
    template = [template for template in templates if template['id'] == template_id]
    if len(template) == 0:
        abort(404)
    templates.remove(template[0])
    return jsonify({'result': True})

@app.route('/api/comments/<int:comment_id>', methods=['DELETE'])
@auth.login_required
def delete_comment(comment_id):
    comment = [comment for comment in comments if comment['id'] == comment_id]
    if len(comment) == 0:
        abort(404)
    comments.remove(comment[0])
    return jsonify({'result': True})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not Found'}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad Request'}), 400)

@auth.get_password
def get_password(username):
    if username in admins:
        return admins[username]

@auth.hash_password
def hash_password(password):
    return hashlib.sha512(password.encode()).hexdigest()

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized Access'}), 401)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)