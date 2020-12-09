from django.shortcuts import render

from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from consultas.models import Pelicula
from consultas.serializers import ConsultaSerializer
from rest_framework.decorators import api_view

# Vistas

def index(request):
    return HttpResponse("CineMerka")

def butacas(request):
    return HttpResponse('Butacas')

@api_view(['GET', 'POST'])
def pelicula_list(request):
    #GET Y POST de todas las peliculas
    if request.method == 'GET':
        peliculas = Pelicula.objects.all()

        nombre = request.GET.get('nombre', None)
        if nombre is not None:
            peliculas = peliculas.filter(nombre__icontains=nombre)

        peliculas_serializer = ConsultaSerializer(peliculas, many=True)
        return JsonResponse(peliculas_serializer.data, safe=False)

    elif request.method == 'POST':
        peliculas_data = JSONParser().parse(request)
        peliculas_serializer = ConsultaSerializer(data=peliculas_data)
        if peliculas_serializer.is_valid():
            peliculas_serializer.save()
            return JsonResponse(peliculas_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(peliculas_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def pelicula_detalle(request, nombre):
    try:
        pelicula = Pelicula.objects.get(nombre=nombre)
    except Pelicula.DoesNotExist:
        return JsonResponse({'mensaje': 'La pelicula no existe'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        pelicula_serializer = ConsultaSerializer(pelicula)
        return JsonResponse(pelicula_serializer.data)
