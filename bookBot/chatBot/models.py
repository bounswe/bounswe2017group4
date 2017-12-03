from django.db import models
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User




class User(models.Model):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField('date published')
    telegram_id = models.IntegerField(unique=True, null=True, blank=True)




class UserInterest(models.Model):
    INTEREST_TYPE_CHOICES = (
        ('author', 'Author'),
        ('category', 'Category'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interest_type = models.CharField(
        max_length=10,
        choices=INTEREST_TYPE_CHOICES,
        default='category',
    )
    interest = models.CharField(max_length=200)

class UserRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True)
    book_id = models.CharField(max_length=100)

class UserComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500, null=True)
    book_id = models.IntegerField()

class State(models.Model):
    id=models.AutoField(primary_key=True)
    description=models.CharField(max_length=500)

class Edge(models.Model):
    id = models.AutoField(primary_key=True)
    current_state_id = models.ForeignKey(State, null=True, related_name='current')
    user_response = models.CharField(max_length=200)
    next_state_id = models.ForeignKey(State, null=True, related_name='next')

class Response(models.Model):
    id = models.AutoField(primary_key=True)
    edge_id = models.ForeignKey(Edge)
    chatbot_response = models.CharField(max_length=500)

class History(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=500)
