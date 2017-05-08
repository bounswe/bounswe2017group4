#!flask/bin/python
import os, sys, subprocess, unittest
from app import get_books, get_comments

class TestApp(unittest.TestCase):	
	def test_get_books(self):
		output = subprocess.check_output(['curl','-u','berkerol:group4','-i','http://localhost:5000/api/books']).replace("\r\n", "\n").partition("{")[2]		
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
if __name__=='__main__':
	unittest.main(exit=False)