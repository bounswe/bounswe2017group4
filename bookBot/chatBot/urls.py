from django.conf.urls import url
from chatBot import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import status, mixins, generics
from rest_framework.response import Response

urlpatterns = [
    url(r'^$', views.index),

    # GET 
    url('isAdmin', views.isAdmin),
    url('getRatings', views.getRatings),
    url('getComments', views.getComments),
    url('getStates', views.getStates),
    url('getEdges', views.getEdges),
    url('getResponses', views.getResponses),
    url('getHistories', views.getHistories),
    url('getInterests', views.getInterests),

    # POST
    url('addState', views.addState),
    url('addEdge', views.addEdge),
    url('addResponse', views.addResponse),
    url('addRating', views.addRating),
    url('addComment', views.addComment),
    url('addUser', views.addUser),
    url('addUserInterest', views.addUserInterest),

    # UPDATE
    url('editState', views.editState),
    url('editEdge', views.editEdge),
    url('editResponse', views.editResponse),

    # DELETE
    url('deleteState', views.deleteState),
    url('deleteEdge', views.deleteEdge),
    url('deleteComment', views.deleteComment),
    url('deleteResponse', views.deleteResponse),
]


urlpatterns = format_suffix_patterns(urlpatterns)
