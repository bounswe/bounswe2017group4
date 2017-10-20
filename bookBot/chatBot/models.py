from django.db import models

# Create your models here.

class User(models.Model):
	name = models.CharField(max_length=200)
	password = models.CharField(max_length=100)
	created_at = models.DateTimeField('date published')

class UserInterest(models.Model):
	INTEREST_TYPE_CHOICES = (
		('author', 'Author'),
		('category', 'Category'),
	)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	year_in_school = models.CharField(
		max_length=10,
		choices=INTEREST_TYPE_CHOICES,
		default='category',
	)
	interest = models.CharField(max_length=200)

class UserRating(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	rating = models.IntegerField()
	book_id = models.CharField(max_length=100)