from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^shorten/', views.shorten, name='shorten'),
    url(r'^list/', views.list_all, name='list_all'),
    url(r'^(?P<hash_val>[0-9a-zA-Z]{1,6})/$', views.original_url, name='original_url'),
]