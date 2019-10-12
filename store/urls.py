from django.urls import path, re_path
from . import views

app_name = 'store'
urlpatterns = [
	re_path(r'^$', views.listing, name='listing'),
	re_path(r'^(?P<album_id>[0-9]+)/$', views.detail, name='detail'),
	re_path(r'^search/$', views.search, name='search'),
]