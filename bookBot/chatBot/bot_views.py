from django.shortcuts import render
from django.http.response import HttpResponse
from django.http.request import HttpRequest

class StartView():
	def start(request):
		import chatBot.bookBot
		return HttpResponse("started")
