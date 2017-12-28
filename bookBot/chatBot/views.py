from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, mixins, generics
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import UserComment, UserInterest, UserRating, User, History, Edge, Response, State
from .serializers import UserCommentSerializer, UserInterestSerializer, UserRatingSerializer,\
    UserSerializer, ResponseSerializer, HistorySerializer, EdgeSerializer, StateSerializer

from django.core import serializers
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

#class StartView(TemplateCommandView):
#    template_text = "bot/messages/hello"
#    print('hello')

# Index view yükleniyor
def index(request):
   return render(request, 'index.html')

# Basic APIs for front-end

# Requestten name ve password parametrelerini çekiyoruz. Kullanıcılarda bu bilgilere göre filtreleme yapıyoruz
# Uygun kullanıcı çıkarsa true yoksa false dönüyoruz.
def isAdmin(request):
    name = request.GET.get('name', '')
    password = request.GET.get('password', '')
    user = User.objects.filter(name=name, password=password)

    if user:
        return JsonResponse(True, safe=False)
    else:
        return JsonResponse(False, safe=False)

# Requestten book_id parametresini çekiyoruz. Her bir rating için response birimi oluşturuyoruz.
# Bu birimleri response arrayine doldurup en son return ediyoruz.
def getRatings(request):
    book_id = request.GET.get('book_id', '')
    userRatings = UserRating.objects.filter(book_id=book_id)

    response = []
    for userRating in userRatings:
        responseSample = {}
        responseSample['rating'] = userRating.rating
        responseSample['user'] = model_to_dict(userRating.user)
        response.append(responseSample)

    return JsonResponse(response, safe=False)

##Comment'ten book_id çek. Her bir rating için response birimi oluştur. Response array'ine doldur ve return et.

def getComments(request):
    book_id = request.GET.get('book_id', '')
    userComments = UserComment.objects.filter(book_id=book_id)

    response=[]
    for userComment in userComments:
        responseSample={}
        responseSample['comment'] = userComment.comment
        responseSample['user'] = model_to_dict(userComment.user)
        response.append(responseSample)

    return JsonResponse(response, safe=False)

##getStates returns all states

def getStates(request):
    states = State.objects.all()
    response=[]
    for state in states:
        responseSample={}
        responseSample['id'] = state.id
        responseSample['description'] = state.description
        response.append(responseSample)

    return JsonResponse(response, safe=False)
#getEdges returns all Edges

def getEdges(request):
    edges = Edge.objects.all()
    response = []
    for edge in edges:
        responseSample={}
        responseSample['id'] = edge.id
        responseSample['current_state_id'] = model_to_dict(edge.current_state_id)
        responseSample['user_response'] = edge.user_response
        responseSample['next_state_id'] = model_to_dict(edge.next_state_id)
        responseSample['recommended_response'] = edge.recommended_response
        response.append(responseSample)

    return JsonResponse(response, safe=False)
#getResponse returns all Responses and post a new response

def getResponses(request):
    responses = Response.objects.all()
    response = []
    for res in responses:
        responseSample = {}
        responseSample['id'] = res.id
        responseSample['state'] = model_to_dict(res.state)
        responseSample['chatbot_response'] = res.chatbot_response
        response.append(responseSample)

    return JsonResponse(response, safe=False)

def getResponsesOfState(request):
    state_id = request.GET.get('state', '')
    state=State()
    state=State.objects.get(id=state_id)
    responses = Response.objects.filter(state=state.description)

    response = []
    for res in responses:
        responseSample = {}
        responseSample['chatbot_response'] =res.chatbot_response
        responseSample['state'] = model_to_dict(res.state)
        response.append(responseSample)

    return JsonResponse(response, safe=False)

def getHistories(request):
    responses = History.objects.all()
    response = []
    for res in responses:
        responseSample = {}
        responseSample['id'] = res.id
        responseSample['user'] = model_to_dict(res.user)
        responseSample['query'] = res.query
        response.append(responseSample)

    return JsonResponse(response, safe=False)

def getInterests(request):
    responses = UserInterest.objects.all()
    response = []
    for res in responses:
        responseSample = {}
        responseSample['user'] = model_to_dict(res.user)
        responseSample['interest_type'] = res.interest_type
        responseSample['interest'] = res.interest
        response.append(responseSample)

    return JsonResponse(response, safe=False)

# Requestten book_id parametresini çekiyoruz. Her bir rating için response birimi oluşturuyoruz.
# Bu birimleri response arrayine doldurup en son return ediyoruz.
@csrf_exempt
def addState(request):
    description = request.POST.get('description','')

    state = State()
    state.description = description
    state.save()

    return JsonResponse("OK", safe=False)

@csrf_exempt
def addEdge(request):
    current_state_id = request.POST.get('current_state_id','')
    user_response = request.POST.get('user_response', '')
    next_state_id = request.POST.get('next_state_id', '')
    recommended_response = request.POST.get('recommended_response', '')

    edge= Edge()
    edge.current_state_id = State.objects.get(id=current_state_id)
    edge.user_response = user_response
    edge.next_state_id = State.objects.get(id=next_state_id)
    edge.recommended_response = recommended_response
    edge.save()

    return JsonResponse("OK", safe=False)


@csrf_exempt
def addResponse(request):
    state_id = request.POST.get('state_id','')
    chatbot_response = request.POST.get('chatbot_response', '')

    response = Response()
    response.state = State.objects.get(id=state_id)
    response.chatbot_response = chatbot_response
    response.save()

    return JsonResponse("OK", safe=False)

@csrf_exempt
def addRating(request):
    user_id = request.POST.get('user_id','')

    rating = UserRating()
    rating.user = User.objects.get(id=user_id)
    rating.rating = request.POST.get('rating','')
    rating.book_id = request.POST.get('book_id','')
    rating.save()

    return JsonResponse("OK", safe=False)

@csrf_exempt
def addComment(request):
    user_id = request.POST.get('user_id','')

    comment = UserComment()
    comment.user = User.objects.get(id=user_id)
    comment.comment = request.POST.get('comment','')
    comment.book_id = request.POST.get('book_id','')
    comment.save()

    return JsonResponse("OK", safe=False)

@csrf_exempt
def addUser(request):
    user = User()
    user.name = request.POST.get('name','')
    user.password = request.POST.get('password','')
    user.created_at = request.POST.get('created_at','')
    user.telegram_id = request.POST.get('telegram_id','')
    user.save()

    return JsonResponse("OK", safe=False)

#add user interest
@csrf_exempt
def addUserInterest(request):
    user_id = request.POST.get('user_id','')

    userinterest=UserInterest()
    userinterest.user= User.objects.get(id=user_id)
    userinterest.interest_type= request.POST.get('interest_type','')
    userinterest.interest= request.POST.get('interest','')
    userinterest.save()

    return JsonResponse("OK", safe=False)

# EDIT APIS
@csrf_exempt
def editState(request):
    state_id = request.POST.get('state_id', '')
    stateObject = State.objects.get(id=state_id)

    description = request.POST.get('next_state_id', '')

    if description != '':
        stateObject.description = description

    stateObject.save()

    return JsonResponse("OK", safe=False)

@csrf_exempt
def editEdge(request):
    edge_id = request.POST.get('edge_id', '')
    edgeObject = Edge.objects.get(id=edge_id)

    current_state_id = request.POST.get('current_state_id', '')
    user_response = request.POST.get('user_response', '')
    next_state_id = request.POST.get('next_state_id', '')
    recommended_response = request.POST.get('recommended_response', '')

    if current_state_id != '':
        edgeObject.current_state_id = State.objects.get(id=current_state_id)
    if user_response != '':
        edgeObject.user_response = user_response
    if next_state_id != '':
        edgeObject.next_state_id = State.objects.get(id=next_state_id)
    if recommended_response != '':
        edgeObject.recommended_response = recommended_response

    edgeObject.save()

    return JsonResponse("OK", safe=False)


def editResponse(request):
    response_id = request.POST.get('response_id','')
    responseObject = Response.objects.get(id=response_id)

    state=request.POST.get('state', '')
    chatbot_response = request.POST.get('chatbot_response', '')

    if state != '':
        responseObject.state = State.objects.get(id=state)
    if chatbot_response != '':
        responseObject.chatbot_response = chatbot_response

    responseObject.save()

    return JsonResponse("OK", safe=False)


# DELETE APIS

@csrf_exempt
def deleteState(request):
    state_id = request.POST.get('state_id', '')
    stateObject = State.objects.get(id=state_id)

    stateObject.delete()

    return JsonResponse("OK", safe=False)

@csrf_exempt
def deleteEdge(request):
    edge_id = request.POST.get('edge_id', '')
    edgeObject = Edge.objects.get(id=edge_id)

    edgeObject.delete()

    return JsonResponse("OK", safe=False)

@csrf_exempt
def deleteComment(request):
    comment_id = request.POST.get('comment_id', '')
    commentObject = Edge.objects.get(id=comment_id)

    commentObject.delete()

    return JsonResponse("OK", safe=False)

@csrf_exempt
def deleteResponse(request):
    response_id=request.POST.get('response_id', '')
    responseObject = Response.objects.get(id=response_id)

    responseObject.delete()

    return JsonResponse("OK", safe=False)
