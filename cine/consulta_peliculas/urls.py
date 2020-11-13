from django.urls import path

from . import views

app_name = 'consulta_peliculas'
urlpatterns = [
    path('', views.index, name='index'),
]