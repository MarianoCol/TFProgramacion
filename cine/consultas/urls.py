from django.urls import path, re_path
from django.conf.urls import url
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from . import views

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico'))),
    path('', views.index, name='index'),
    # Peliculas Views Urls
    re_path(r'^api/peliculas/([a-zA-Z0-9 ]+)/(\d{4}[-/]\d{2}[-/]\d{2})/(\d{4}[-/]\d{2}[-/]\d{2})$', views.pelicula_detalle),
    re_path(r'^api/peliculas/(\d{4}[-/]\d{2}[-/]\d{2})/(\d{4}[-/]\d{2}[-/]\d{2})$', views.pelicula_fechas),
    # Salas Views Urls
    re_path(r'^api/salas$', views.sala_list),
    re_path(r'^api/salas/([a-zA-Z0-9 ]+)$', views.sala_detalle),
    # Proyecciones Views Urls
    re_path(r'^api/proyecciones$', views.proyeccion_list),
    re_path(r'^api/proyecciones/([0-9]+)$', views.proyeccion_detalle),
    # Butacas Views Urls
    re_path(r'^api/butaca$', views.butacas_list),
    re_path(r'^api/butaca/reservar$', views.butaca_reservada),
    re_path(r'^api/butaca/(\d{4}[-/]\d{2}[-/]\d{2})/(\d{4}[-/]\d{2}[-/]\d{2})$', views.butacas_vendidas),
    re_path(r'^api/butaca/([0-9]+)/(\d{4}[-/]\d{2}[-/]\d{2})/(\d{4}[-/]\d{2}[-/]\d{2})$', views.butacas_vendidas_proyeccion),
    # Rank Views Urls
    re_path(r'^api/butacaRank/(\d{4}[-/]\d{2}[-/]\d{2})/(\d{4}[-/]\d{2}[-/]\d{2})$', views.butacas_vendidas_rank),
    re_path(r'^api/peliculasRank$', views.peliculas_rank),
    # re_path(r'^api/butaca/([a-zA-Z0-9]+)/([0-9]+)/([0-9]+)$', views.butaca_reserva),
]
