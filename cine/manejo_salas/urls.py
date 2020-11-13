from django.urls import path

from . import views

app_name = 'manejo_salas'
urlpatterns = [
    path('', views.index, name='index'),
]