from django.urls import path
from django.conf.urls import url
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from . import views

urlpatterns = [
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico'))),
    path('', views.index, name='index'),
    # path('butacas/', views.butacas, name='butacas'),
    url(r'^api/peliculas$', views.pelicula_list),
    url(r'^api/peliculas/([a-zA-Z0-9 ]+)/(\d{4}[-/]\d{2}[-/]\d{2})/(\d{4}[-/]\d{2}[-/]\d{2})$', views.pelicula_detalle),
    url(r'^api/peliculas/(\d{4}[-/]\d{2}[-/]\d{2})/(\d{4}[-/]\d{2}[-/]\d{2})$', views.pelicula_fechas),
    url(r'^api/salas$', views.sala_list),
    url(r'^api/salas/([a-zA-Z0-9 ]+)$', views.sala_detalle),
    # Butacas Views Urls
    url(r'^api/butaca$', views.butacas_list),
    url(r'^api/butaca/([0-9]+)$', views.butaca_reservada),
    # url(r'^api/butaca/([a-zA-Z0-9]+)/([0-9]+)/([0-9]+)$', views.butaca_reserva),
]
