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
  * These processes require authentication with username=berkerol and password=group4
  * GET: Retrive a list of books
    ```
    $ curl -u berkerol:group4 -i http://localhost:5000/api/books
    ```
  * GET: Retrieve a book
    ```
    $ curl -u berkerol:group4 -i http://localhost:5000/api/books/2
    ```
  * POST: Create a book
    ```
    $ curl -u berkerol:group4 -i -H "Content-Type: application/json" -X POST -d '{"name":"1984", "author":"George Orwell", "price":11.0}' http://localhost:5000/api/books
    ```
  * PUT: Update a book
    ```
    $ curl -u berkerol:group4 -i -H "Content-Type: application/json" -X PUT -d '{"price":12.0}' http://localhost:5000/api/books/3
    ```
  * DELETE: Delete a book
    ```
    $ curl -u berkerol:group4 -X DELETE http://localhost:5000/api/books/3
    ```