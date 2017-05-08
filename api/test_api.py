#!flask/bin/python
import os, sys, subprocess, unittest
from app import get_books, get_comments

class TestApp(unittest.TestCase):	
	def test_get_books(self):
		output = subprocess.check_output(['curl','-u','group4:1111','-i','http://localhost:5000/api/books']).replace("\r\n", "\n").partition("{")[2]		
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
	def test_get_comments(self):
		output = subprocess.check_output(['curl','-u','group4:1111','-i','http://localhost:5000/api/comments']).replace("\r\n", "\n").partition("{")[2]		
		self.assertEqual(output,"""
	"comments" : [
    {
        "id": 1,
        "book": 1,
        "owner": 1,
        "content": u"Such an enlightening book."
    },
    {
        "id": 2,
        "book": 1,
        "owner": 2,
        "content": u"Great book. Similar to 1984, only more realistic."
    },
    {
        "id": 3,
        "book": 2,
        "owner":1,
        "content": u"Very interesting."
    }
]
""")
if __name__=='__main__':
	unittest.main(exit=False)