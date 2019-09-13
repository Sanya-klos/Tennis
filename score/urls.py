from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^filter/$', views.filter_table, name='filter_table'),
    url(r'^schedule/$', views.create_schedule, name='create_schedule'),
]
