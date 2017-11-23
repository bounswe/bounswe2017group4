from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=200)
    password = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    telegram_id = models.IntegerField(unique=True, null=True)

    def __str__(self):
        return str(self.telegram_id)

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

class State(models.Model):
    id = models.IntegerField(primary_key=True)
    description=models.CharField(max_length=500)

    def __str__(self):
        return self.description

class Edge(models.Model):
    id = models.IntegerField(primary_key=True)
    current_state_id = models.ForeignKey(State, null=True, related_name='current')
    user_response = models.CharField(max_length=200)
    next_state_id = models.ForeignKey(State, null=True, related_name='next')

    def __str__(self):
        return str(self.id)

class Response(models.Model):
    id = models.IntegerField(primary_key=True)
    state_id = models.ForeignKey(State)
    chatbot_response = models.CharField(max_length=500)

    def __str__(self):
        return str(self.id)

class History(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=500)