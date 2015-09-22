from django.shortcuts import render

from django.http import HttpResponse

def index(request):
	context_dict = {'boldmessage': "This is my home page!"}
	return render(request, 'rango/index.html', context_dict)

def about(request):
	context_dict = {'boldmessage': "This is my about page!"}
	return render(request, 'rango/about.html', context_dict)