from django.conf.urls import patterns, url
from rango import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
]