from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField('date published')
    telegram_id = models.IntegerField(unique=True, null=True)

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
    rating = models.IntegerField()
    book_id = models.CharField(max_length=100)

class UserComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    book_id = models.IntegerField()

class Edge(models.Model):
    id = models.IntegerField(primary_key=True)
    current_state_id = models.IntegerField()
    user_response = models.CharField(max_length=200)
    next_state_id = models.IntegerField()

class Response(models.Model):
    id = models.IntegerField(primary_key=True)
    edge_id = models.ForeignKey(Edge)
    chatbot_response = models.CharField(max_length=500)

class History(models.Model):
    hist_id = models.IntegerField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=500)

class State(models.Model):
    id=models.ForeignKey(Edge, on_delete=models.CASCADE)
    description=models.CharField(max_length=500)