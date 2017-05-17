# Installation

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

# Deployment

Deployed to [here](http://berkerol.pythonanywhere.com/)

# Endpoints

## Book Endpoints

### Get all books [GET]

**Parameters:**

None

**Request:**

`http -a username:password http://localhost:5000/api/books`

**Response:**

Code: 200, OK

```
{
    "books": [
        {
            "author": "Aldous Huxley",
            "id": 1,
            "name": "Brave New World",
            "price": 13.5
        },
        {
            "author": "Chuck Palahniuk",
            "id": 2,
            "name": "Fight Club",
            "price": 8.5
        }
    ]
}
```

### Get a Specific Book [GET]

**Parameters:**

* id (required)

**Request:**

`http -a username:password http://localhost:5000/api/books/2`

**Response:**

Code: 200, OK

```
{
    "book": {
        "author": "Chuck Palahniuk",
        "id": 2,
        "name": "Fight Club",
        "price": 8.5
    }
}
```

### Create new Book [POST]

**Parameters:**

* name (required)
* author (required)
* price (required)
* id (auto-increment)

**Request:**

`http -a username:password --json POST http://localhost:5000/api/books "name"="1984" "author"="George Orwell" "price"=11.0`

**Response:**

Code: 201, CREATED

```
{
    "book": {
        "author": "George Orwell",
        "id": 3,
        "name": "1984",
        "price": "11.0"
    }
}
```

### Update a Book [PUT]

**Parameters:**

* id (required)
* name (optional)
* author (optional)
* price (optional)

**Request:**

`curl -u username:password -i -H "Content-Type: application/json" -X PUT -d '{"price":12.0}' http://localhost:5000/api/books/3`

**Response:**

Code 200, OK

```
{
  "book": {
    "author": "George Orwell",
    "id": 3,
    "name": "1984",
    "price": 12.0
  }
}
```

### Delete a Book [DELETE]

**Parameters:**

* id (required)

**Request:**

`http -a username:password --json DELETE http://localhost:5000/api/books/3`

**Response:**

Code: 200, OK

```
{
    "result": true
}
```

### Get all comments [GET]

**Parameters:**

None

**Request:**

`curl -u username:password -i http://localhost:5000/api/comments`

**Response:**

Code: 200, OK

```
{
  "comments": [
    {
      "book": 1,
      "content": "Such an enlightening book.",
      "id": 1,
      "owner": 1
    },
    {
      "book": 1,
      "content": "Great book. Similar to 1984, only more realistic.",
      "id": 2,
      "owner": 2
    },
    {
      "book": 2,
      "content": "Very interesting.",
      "id": 3,
      "owner": 1
    }
  ]
}
```

### Get all comments of a book [GET]

**Parameters:**

* id (required)

**Request:**

`curl -u username:password -i http://localhost:5000/api/comments/book/1`

**Response:**

Code: 200, OK

```
{
  "comments": [
    {
      "book": 1,
      "content": "Such an enlightening book.",
      "id": 1,
      "owner": 1
    },
    {
      "book": 1,
      "content": "Great book. Similar to 1984, only more realistic.",
      "id": 2,
      "owner": 2
    }
  ]
}
```

### Get all comments of a user [GET]

**Parameters:**

* id (required)

**Request:**

`curl -u username:password -i http://localhost:5000/api/comments/user/1`

**Response:**

Code: 200, OK

```
{
  "comments": [
    {
      "book": 1,
      "content": "Such an enlightening book.",
      "id": 1,
      "owner": 1
    },
    {
      "book": 2,
      "content": "Very interesting.",
      "id": 3,
      "owner": 1
    }
  ]
}
```

### Get comment by id [GET]

**Parameters:**

* id (required)

**Request:**

`curl -u username:password -i http://localhost:5000/api/comments/2`

**Response:**

Code: 200, OK

```
{
  "comment": {
    "book": 1,
    "content": "Great book. Similar to 1984, only more realistic.",
    "id": 2,
    "owner": 2
  }
}
```

### Post a comment [POST]

**Parameters:**

* book (required)
* owner (required)
* content (required)
* id (auto-increment)

**Request:**

`curl -u username:password -i -H "Content-Type: application/json" -X POST -d '{"book":2, "owner":2, "content":"Wow"}' http://localhost:5000/api/comments`

**Response:**

Code: 201, CREATED

```
{
  "comment": {
    "book": 2,
    "content": "Wow",
    "id": 4,
    "owner": 2
  }
}
```



# Examples

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
* PUT: Update a template
  ```
  $ curl -u username:password -i -H "Content-Type: application/json" -X PUT -d '{"out":["Hi $UserName.", "Nice to meet you $UserName!"]}' http://localhost:5000/api/templates/3
  ```
* DELETE: Delete a template
  ```
  $ curl -u username:password -X DELETE http://localhost:5000/api/templates/3
  ```
