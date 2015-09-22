from django.shortcuts import render

from django.http import HttpResponse

def index(request):
	return HttpResponse("Rango says hello! <br/> <br/><a href='/rango/about'>About</a>")

def about(request):
	return HttpResponse("Rango says here is the about page. <br/> <br/><a href='/rango/'>Index</a>")