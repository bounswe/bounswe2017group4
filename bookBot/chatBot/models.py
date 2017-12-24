from django.db import models
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User




class User(models.Model):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField('date published', auto_now_add=True)
    telegram_id = models.IntegerField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

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
    def __str__(self):
        return str(self.user)

class UserRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(blank=True)
    book_id = models.CharField(max_length=100)
    def __str__(self):
        return self.book_id

class UserComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500, blank=True)
    book_id = models.CharField(max_length=100)

    def __str__(self):
        return self.book_id

class State(models.Model):
    id=models.AutoField(primary_key=True)
    description=models.CharField(max_length=500)

    def __str__(self):
        return self.description

class Edge(models.Model):

    id = models.IntegerField(primary_key=True)
    current_state_id = models.ForeignKey(State, null=True, related_name='current')
    user_response = models.CharField(max_length=200)
    next_state_id = models.ForeignKey(State, null=True, related_name='next')
    recommended_response = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return str(self.current_state_id) + '->' + str(self.next_state_id)

class Response(models.Model):
    id = models.IntegerField(primary_key=True)
    state = models.ForeignKey(State)
    chatbot_response = models.CharField(max_length=500)

    def __str__(self):
        return str(self.id)

class History(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=500)

    def __str__(self):
        return str(self.id)

