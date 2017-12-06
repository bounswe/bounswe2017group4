from rest_framework import serializers
from .models import User, UserRating, UserInterest, UserComment, Response, Edge, History, State

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=('name', 'password', 'created_at', 'telegram_id')


class UserRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRating
        fields = ('user', 'rating', 'book_id')

class UserInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterest
        fields =('user', 'interest_type', 'interest')

class UserCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserComment
        fields = ('user', 'comment', 'book_id')

class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = ('id', 'edge_id', 'chatbot_response')

class EdgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Edge
        fields = ('id', 'current_state_id', 'user_response', 'next_state_id')

class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ('id', 'user', 'query')

class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ('id', 'description')