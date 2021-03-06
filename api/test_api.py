#!flask/bin/python
import os, sys, subprocess, unittest, json
from app import get_books, get_comments, get_users, get_comments_of_book, get_comments_of_user, get_templates

class TestApp(unittest.TestCase):
	def test_get_books(self):
		output = subprocess.check_output(['curl','-u','group4:1111','-i','http://localhost:5000/api/books']).partition("{")[2]
		self.assertEqual(output,"""
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
""")
<<<<<<< HEAD
<<<<<<< HEAD

	def test_get_comments(self):
		output = subprocess.check_output(['curl','-u','group4:1111','-i','http://localhost:5000/api/comments']).partition("{")[2]		
=======
	def test_get_comments(self):
		output = subprocess.check_output(['curl','-u','group4:1111','-i','http://localhost:5000/api/comments']).replace("\r\n", "\n").partition("{")[2]		
>>>>>>> refs/remotes/origin/master
=======
	def test_post_book(self):
		output = subprocess.check_output(['curl','-u','group4:1111','-i','-H','Content-Type: application/json','-X','POST',
                      '-d','{"name":"1984", "author":"George Orwell", "price":11.0}',
                      'http://localhost:5000/api/books']).partition("{")[2]
		book = json.loads("{"+output).get('book')
		id = book.get('id')
		self.assertTrue(id > 0)

	def test_get_comments(self):
		output = subprocess.check_output(['curl','-u','group4:1111','-i','http://localhost:5000/api/comments']).partition("{")[2]
>>>>>>> master
		self.assertEqual(output,"""
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
<<<<<<< HEAD
<<<<<<< HEAD
	]
=======
  ]
>>>>>>> master
}
""")

	def test_get_users(self):
		output = subprocess.check_output(['curl','-u','group4:1111','-i','http://localhost:5000/api/users']).partition("{")[2]
		self.assertEqual(output,"""
  "users": [
    {
      "id": 1, 
      "name": "nicholasramsey"
    }, 
    {
      "id": 2, 
      "name": "richardterry"
    }
  ]
}
""")

	def test_get_comments_of_book(self):
		output = subprocess.check_output(['curl','-u','group4:1111','-i','http://localhost:5000/api/comments/book/1']).partition("{")[2]
		self.assertEqual(output,"""
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
""")

	def test_get_comments_of_user(self):
		output = subprocess.check_output(['curl','-u','group4:1111','-i','http://localhost:5000/api/comments/user/1']).partition("{")[2]
		self.assertEqual(output,"""
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
""")

	def test_get_templates(self):
		output = subprocess.check_output(['curl','-u','group4:1111','-i','http://localhost:5000/api/templates']).partition("{")[2]    
		self.assertEqual(output,"""
  "templates": [
    {
      "id": 1, 
      "in": [
        "My name is $UserName", 
        "I am $UserName"
      ], 
      "name": "Asking name", 
      "out": [
        "Hello $UserName.", 
        "Nice to meet you $UserName!"
      ]
    }, 
    {
      "id": 2, 
      "in": [
        "I want to search books about $Genre", 
        "Can you show me the books about $Genre"
      ], 
      "name": "Asking book", 
      "out": [
        "Here are some books about $Genre. Do you want to keep searching?"
      ]
    }
  ]
}
<<<<<<< HEAD
=======
]
>>>>>>> refs/remotes/origin/master
=======
>>>>>>> master
""")
if __name__=='__main__':
  unittest.main(exit=False)