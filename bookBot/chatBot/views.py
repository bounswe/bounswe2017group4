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

# Requestten book_id parametresini çekiyoruz. Her bir rating için response birimi oluşturuyoruz.
# Bu birimleri response arrayine doldurup en son return ediyoruz.
@csrf_exempt
def addState(request):
    description = request.POST.get('description', 'xyz')

    state = State()
    state.description = description
    state.save()

    return JsonResponse("OK", safe=False)

#User
class UserList(mixins.ListModelMixin, mixins.CreateModelMixin,
               generics.GenericAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class UserDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

#UserInterest
class UserInterestList(mixins.ListModelMixin, mixins.CreateModelMixin,
               generics.GenericAPIView):

    queryset = UserInterest.objects.all()
    serializer_class = UserInterestSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class UserInterestDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = UserInterest.objects.all()
    serializer_class = UserInterestSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

#UserRating
class UserRatingList(mixins.ListModelMixin, mixins.CreateModelMixin,
               generics.GenericAPIView):

    queryset = UserRating.objects.all()
    serializer_class = UserRatingSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class UserRatingDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = UserRating.objects.all()
    serializer_class = UserRatingSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

#UserComment
class UserCommentList(mixins.ListModelMixin, mixins.CreateModelMixin,
               generics.GenericAPIView):

    queryset = UserComment.objects.all()
    serializer_class = UserCommentSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class UserCommentDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = UserComment.objects.all()
    serializer_class = UserCommentSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
#State
class StateList(mixins.ListModelMixin, mixins.CreateModelMixin,
               generics.GenericAPIView):

    queryset = State.objects.all()
    serializer_class = StateSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class StateDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
#Edge
class EdgeList(mixins.ListModelMixin, mixins.CreateModelMixin,
               generics.GenericAPIView):

    queryset = Edge.objects.all()
    serializer_class = EdgeSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class EdgeDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Edge.objects.all()
    serializer_class = EdgeSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
#Response
class ResponseList(mixins.ListModelMixin, mixins.CreateModelMixin,
               generics.GenericAPIView):

    queryset = Response.objects.all()
    serializer_class = ResponseSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ResponseDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
#History
class HistoryList(mixins.ListModelMixin, mixins.CreateModelMixin,
               generics.GenericAPIView):

    queryset = History.objects.all()
    serializer_class = HistorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class HistoryDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = History.objects.all()
    serializer_class = HistorySerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
