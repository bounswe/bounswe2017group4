1. Install Python 2.7, pip, virtualenv.
2. Install Flask.
```
$ virtualenv flask
$ flask/bin/pip install flask
```
3. Install Flask-HTTPAuth.
```
$ flask/bin/pip install flask-httpauth
```
4. Put app.py near flask.
5. In that directory execute app.py
```
$ chmod a+x app.py
$ ./app.py
```
6. Open a NEW console window (do not close the one where app.py is running).
  * GET: Retrive all books
    ```
    $ curl -u username:password -i http://localhost:5000/api/books
    ```
  * GET: Retrive all comments
    ```
    $ curl -u username:password -i http://localhost:5000/api/comments
    ```
  * GET: Retrive all users
    ```
    $ curl -u username:password -i http://localhost:5000/api/users
    ```
  * GET: Retrive all templates
    ```
    $ curl -u username:password -i http://localhost:5000/api/templates
    ```
  * GET: Retrive all comments of a book
    ```
    $ curl -u username:password -i http://localhost:5000/api/comments/book/1
    ```
  * GET: Retrive all comments of a user
    ```
    $ curl -u username:password -i http://localhost:5000/api/comments/user/1
    ```
  * GET: Retrieve a book
    ```
    $ curl -u username:password -i http://localhost:5000/api/books/2
    ```
  * GET: Retrieve a comment
    ```
    $ curl -u username:password -i http://localhost:5000/api/comments/2
    ```
  * GET: Retrieve a user
    ```
    $ curl -u username:password -i http://localhost:5000/api/users/2
    ```
  * GET: Retrieve a template
    ```
    $ curl -u username:password -i http://localhost:5000/api/templates/2
    ```
  * POST: Create a book
    ```
    $ curl -u username:password -i -H "Content-Type: application/json" -X POST -d '{"name":"1984", "author":"George Orwell", "price":11.0}' http://localhost:5000/api/books
    ```
  * POST: Create a comment
    ```
    $ curl -u username:password -i -H "Content-Type: application/json" -X POST -d '{"book":2, "owner":2, "content":"Wow"}' http://localhost:5000/api/comments
    ```
  * POST: Create a user
    ```
    $ curl -u username:password -i -H "Content-Type: application/json" -X POST -d '{"name":"amerty"}' http://localhost:5000/api/users
    ```
  * POST: Create a template
    ```
    $ curl -u username:password -i -H "Content-Type: application/json" -X POST -d '{"name":"Asking name", "in":["My name is $UserName", "I am $UserName"], "out":["Hello $UserName.", "Nice to meet you $UserName!"]}' http://localhost:5000/api/templates
    ```
  * PUT: Update a book
    ```
    $ curl -u username:password -i -H "Content-Type: application/json" -X PUT -d '{"price":12.0}' http://localhost:5000/api/books/3
    ```
  * PUT: Update a template
    ```
    $ curl -u username:password -i -H "Content-Type: application/json" -X PUT -d '{"out":["Hi $UserName.", "Nice to meet you $UserName!"]}' http://localhost:5000/api/templates/3
    ```
  * DELETE: Delete a book
    ```
    $ curl -u username:password -X DELETE http://localhost:5000/api/books/3
    ```
  * DELETE: Delete a template
    ```
    $ curl -u username:password -X DELETE http://localhost:5000/api/templates/3
    ```