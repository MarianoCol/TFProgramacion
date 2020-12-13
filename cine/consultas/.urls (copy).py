from django.urls import path
from django.conf.urls import url
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('butacas/', views.butacas, name='butacas'),
    url(r'^peliculas$', views.pelicula_list),
    url(r'^peliculas/([a-zA-Z0-9 ]+)/(\d{4}[-/]\d{2}[-/]\d{2})/(\d{4}[-/]\d{2}[-/]\d{2})$', views.pelicula_detalle),
    url(r'^peliculas/(\d{4}[-/]\d{2}[-/]\d{2})/(\d{4}[-/]\d{2}[-/]\d{2})$', views.pelicula_fechas),
    url(r'^salas$', views.sala_list),
    url(r'^salas/([a-zA-Z0-9 ]+)$', views.sala_detalle),
    url(r'^proyecciones$', views.proyeccion_list),
    #url(r'^api/tutorials/(?P<pk>[0-9]+)$'
    # Butacas Views Urls
    url(r'^butaca$', views.butacas_list),
    url(r'^butaca/([0-9]+)$', views.butaca_reservada),
    url(r'^butaca/r/$', views.butaca_reserva),
]
