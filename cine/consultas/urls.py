from django.urls import path, re_path
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^peliculas/$', views.listPeliculas, name='peliculas'),
    # Rango de fecha de peliculas
    re_path(r'^peliculas/(?P<fechaC>[12][890][0-9][0-9]-[01][0-9]-[0123][0-9])/(?P<fechaF>[12][890][0-9][0-9]-[01][0-9]-[0123][0-9])$', views.listPeliculas, name='peliculas_fechas'),
    # Pelicula especifica con rango de proyeccion
    re_path(r'^pelicilas/(?P<pelicula>[0-9a-zA-Z])/(?P<fechaC>[12][890][0-9][0-9]-[01][0-9]-[0123][0-9])/(?P<fechaF>[12][890][0-9][0-9]-[01][0-9]-[0123][0-9])$', views.rangoPelicula, name='rango_pelicula')
]
