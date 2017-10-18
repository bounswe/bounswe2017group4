from django.shortcuts import render
from django.http.response import HttpResponse
import telepot
# Create your views here.
class StartView(TemplateCommandView):
        template_text = "bot/messages/hello"
		print('hello')