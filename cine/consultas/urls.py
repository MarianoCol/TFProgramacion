from django.urls import path, re_path
from django.conf.urls import url
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from . import views

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico'))),
    path('', views.index, name='index'),
    # Peliculas Views Urls
    re_path(r'^api/peliculas$', views.peliculas),
    re_path(r'^api/peliculas/(?P<id>[0-9]+)/(?P<fechaInicio>\d{4}[-/]\d{2}[-/]\d{2})/(?P<fechaFin>\d{4}[-/]\d{2}[-/]\d{2})$', views.pelicula_detalle),
    re_path(r'^api/peliculas/(?P<fechaInicio>\d{4}[-/]\d{2}[-/]\d{2})/(?P<fechaFin>\d{4}[-/]\d{2}[-/]\d{2})$', views.pelicula_fechas),
    # Salas Views Urls
    re_path(r'^api/salas$', views.sala),
    re_path(r'^api/salas/(?P<id>[0-9]+)$', views.sala_detalle),
    # Proyecciones Views Urls
    re_path(r'^api/proyecciones$', views.proyeccion_list),
    re_path(r'^api/proyecciones/(?P<id>[0-9]+)$', views.proyeccion_mod),
    re_path(r'^api/proyecciones/rango/(?P<fechaInicio>\d{4}[-/]\d{2}[-/]\d{2})/(?P<fechaFin>\d{4}[-/]\d{2}[-/]\d{2})$', views.proyeccion_rango),
    re_path(r'^api/proyecciones/fecha/(?P<peliId>[0-9]+)/(?P<fecha>\d{4}[-/]\d{2}[-/]\d{2}T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]Z)$', views.proyeccion_fecha),
    # Butacas Views Urls
    re_path(r'^api/butaca$', views.butacas_list),
    re_path(r'^api/butaca/(?P<id>[0-9]+)$', views.butaca_reservada),
    re_path(r'^api/butaca/reservar$', views.butaca_reserva),
    re_path(r'^api/butaca/mod/(?P<id>[0-9]+)$', views.butaca_mod),
    re_path(r'^api/butaca/(?P<fechaInicio>\d{4}[-/]\d{2}[-/]\d{2})/(?P<fechaFin>\d{4}[-/]\d{2}[-/]\d{2})$', views.butacas_vendidas),
    re_path(r'^api/butaca/(?P<proyeccion>[0-9]+)/(?P<fechaInicio>\d{4}[-/]\d{2}[-/]\d{2})/(?P<fechaFin>\d{4}[-/]\d{2}[-/]\d{2})$', views.butacas_vendidas_proyeccion),
    # Rank Views Urls
    re_path(r'^api/butacaRank/(?P<fechaInicio>\d{4}[-/]\d{2}[-/]\d{2})/(?P<fechaFin>\d{4}[-/]\d{2}[-/]\d{2})$', views.butacas_vendidas_rank),
    re_path(r'^api/peliculasRank$', views.peliculas_rank),
    # re_path(r'^api/butaca/([a-zA-Z0-9]+)/([0-9]+)/([0-9]+)$', views.butaca_reserva),
    # Endpoint Profes
    re_path(r'^api/peliculasProfes$', views.peliculas_profes)
    ]
