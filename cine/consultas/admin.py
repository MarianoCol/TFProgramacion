from django.contrib import admin
from .models import Pelicula, Proyeccion, Sala, Butaca
# Register your models here.

for model in [Pelicula, Proyeccion, Sala, Butaca]:
    admin.site.register(model)