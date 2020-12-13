from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from consultas.serializers import *
from consultas.models import *
from rest_framework.decorators import api_view
import datetime as dt
# Vistas

def index(request):
    return HttpResponse('Bienvenido')

# Endpoint - Consulta de peliculas
# GET -  Peliculas en un rango de fecha
@api_view(['GET'])
def listPeliculas(request, fechaC, fechaF):
    if request.method == 'GET':
        pelis = Pelicula.objects.filter(fechaComienzo__gte=fechaC, fechaFinal__lte=fechaF)
        if pelis.count() == 0:
            return JsonResponse({'mensaje':'no hay peliculas en ese rango'}, status=status.HTTP_404_NOT_FOUND)
        pelicula_serializer = PeliculaSerializer(pelis, many=True)
        return JsonResponse(pelicula_serializer.data, status=status.HTTP_200_OK, safe=False)

# GET - Pelicula rango de proyeccion
@api_view(['GET'])
def rangoPelicula(request, pelicula, fechaC, fechaF):
    if request.method == 'GET':
        fechaC = dt.datetime.strptime(fechaC, '%Y-%m-%d').date()
        fechaF = dt.datetime.strptime(fechaF, '%Y-%m-%d').date()
        deltaFecha = fechaF - fechaC
        try:
            pelis = Pelicula.objects.filter(nombre=pelicula, fechaComienzo__gte=fechaC, fechaFinal__lte=fechaF)
        except peli.DoesNotExist:
            return JsonResponse({'error':'la pelicula no existe'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        