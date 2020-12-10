from django.shortcuts import render

from django.http import HttpResponse
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from consultas.models import Pelicula, Sala
from consultas.serializers import ConsultaSerializer, SalaSerializer
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
def pelicula_detalle(request, nombre, fechaInicio, fechaFin):
    try:
        # fechaInicio = datetime.strptime(fechaInicio, '%Y-%m-%d')
        # fechaFin = datetime.strptime(fechaFin, '%Y-%m-%d')
        pelicula = Pelicula.objects.get(nombre=nombre, fechaComienzo=fechaInicio, fechaFinal=fechaFin)

    except Pelicula.DoesNotExist:
        return JsonResponse({'mensaje': 'La pelicula no existe o el rango de fechas es incorrecto'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        pelicula_serializer = ConsultaSerializer(pelicula)

        return JsonResponse(pelicula_serializer.data)

@api_view(['GET'])
def pelicula_fechas(request, fechaInicio, fechaFin):
    pelicula = Pelicula.objects.filter(fechaComienzo__gte=fechaInicio, fechaFinal__lte=fechaFin)

    if pelicula.count() == 0:
        return JsonResponse({'mensaje': 'No hay peliculas en este rango'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        pelicula_serializer = ConsultaSerializer(pelicula, many=True)

        return JsonResponse(pelicula_serializer.data, safe=False)

@api_view(['GET', 'POST'])
def sala_list(request):
    if request.method == 'GET':
        salas = Sala.objects.all()

        nombre = request.GET.get('nombre', None)
        if nombre is not None:
            salas = salas.filter(nombre__icontains=nombre)

        salas_serialazer = SalaSerializer(salas, many=True)
        return JsonResponse(salas_serialazer.data, safe=False)

    elif request.method == 'POST':
        salas_data = JSONParser().parse(request)
        salas_serialazer = SalaSerializer(data=salas_data)
        if salas_serialazer.is_valid():
            salas_serialazer.save()
            return JsonResponse(salas_serialazer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(salas_serialazer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def sala_detalle(request, nombre):
    try:
        sala = Sala.objects.get(nombre=nombre)
    except Sala.DoesNotExist:
        return JsonResponse({'Error': 'La sala no existe'})

    if request.method == 'GET':
        sala_serializer = SalaSerializer(sala)
        return JsonResponse(sala_serializer.data)

    elif request.method == 'PUT': 
        sala_data = JSONParser().parse(request) 
        salas_serializer = SalaSerializer(sala, data=sala_data) 
        if salas_serializer.is_valid(): 
            salas_serializer.save() 
            return JsonResponse(salas_serializer.data) 
        return JsonResponse(salas_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE': 
        sala.delete() 
        return JsonResponse({'Hecho': 'La sala ha sido eliminada satisfactoriamente!'}, status=status.HTTP_204_NO_CONTENT)
