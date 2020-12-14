from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from django.http.response import JsonResponse
from django.db.models import Q
from rest_framework.parsers import JSONParser
from rest_framework import status

from consultas.serializers import ConsultaSerializer, SalaSerializer, ProyeccionSerializer, ButacaSerializer
from consultas.models import Pelicula, Sala, Butaca, Proyeccion
from rest_framework.decorators import api_view
import datetime
# Vistas

def index(request):
    template = loader.get_template('index.html')
    context = {
        'prueba': True,
    }
    return HttpResponse(template.render(context, request))

# Endpoint de Peliculas.
# Traer disponibilidad de una pelicula
@api_view(['GET'])
def pelicula_detalle(request, nombre, fechaInicio, fechaFin):
    try:
        pelicula = Pelicula.objects.get(Q(nombre=nombre))
    except Pelicula.DoesNotExist:
        return JsonResponse({'mensaje': 'La pelicula no existe'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        fechaInicio = datetime.datetime.strptime(fechaInicio, '%Y-%m-%d').date()
        fechaFin = datetime.datetime.strptime(fechaFin, '%Y-%m-%d').date()
        if fechaInicio <= pelicula.fechaComienzo:
            fechaInicio = pelicula.fechaComienzo
        if fechaFin > pelicula.fechaFinal:
            fechaFin = pelicula.fechaFinal
        delta = fechaFin - fechaInicio
        disponible = []
        for i in range(delta.days + 1):
            disponible.append(fechaInicio + datetime.timedelta(days=i))
        pelicula_serializer = ConsultaSerializer(pelicula)
        newDic = {}
        newDic.update(pelicula_serializer.data)
        newDic.update({'disponilbe': disponible})
        return JsonResponse(newDic, status=status.HTTP_200_OK)

# Traer peliculas en un rango de fechas
@api_view(['GET'])
def pelicula_fechas(request, fechaInicio, fechaFin):
    pelicula = Pelicula.objects.filter(fechaComienzo__gte=fechaInicio, fechaFinal__lte=fechaFin)

    if pelicula.count() == 0:
        return JsonResponse({'mensaje': 'No hay peliculas en este rango'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        pelicula_serializer = ConsultaSerializer(pelicula, many=True)
        return JsonResponse(pelicula_serializer.data, status=status.HTTP_200_OK, safe=False)

# Endpoint de Salas.
# Trear todas las salas y crear nueva sala
@api_view(['GET', 'POST'])
def sala_list(request):
    if request.method == 'GET':
        salas = Sala.objects.all()
        salas_serialazer = SalaSerializer(salas, many=True)
        return JsonResponse(salas_serialazer.data, safe=False, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        salas_data = JSONParser().parse(request)
        salas_serialazer = SalaSerializer(data=salas_data)
        if salas_serialazer.is_valid():
            salas_serialazer.save()
            return JsonResponse(salas_serialazer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(salas_serialazer.errors, status=status.HTTP_400_BAD_REQUEST)

# Treaer una sala, modificarla o eliminarla
@api_view(['GET', 'PUT', 'DELETE'])
def sala_detalle(request, nombre):
    try:
        sala = Sala.objects.get(nombre=nombre)
    except Sala.DoesNotExist:
        return JsonResponse({'Error': 'La sala no existe'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        sala_serializer = SalaSerializer(sala)
        return JsonResponse(sala_serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT': 
        sala_data = JSONParser().parse(request) 
        salas_serializer = SalaSerializer(sala, data=sala_data) 
        if salas_serializer.is_valid(): 
            salas_serializer.save() 
            return JsonResponse(salas_serializer.data, status=status.HTTP_200_OK) 
        return JsonResponse(salas_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE': 
        sala.delete()
        return JsonResponse({'Hecho': 'La sala ha sido eliminada satisfactoriamente!'}, status=status.HTTP_204_NO_CONTENT)

# Endpoint de Proyeccion
# Trear las proyecciones activas y subir una nueva proyeccion
@api_view(['GET', 'POST'])
def proyeccion_list(request):
    if request.method == 'GET':
        proyecciones = Proyeccion.objects.filter(estado="ACTIVO")
        proyecciones_serialazer = ProyeccionSerializer(proyecciones, many=True)

        for proyeccion in proyecciones_serialazer.data:
            pelicula = ConsultaSerializer(Pelicula.objects.get(id=proyeccion["pelicula"]))
            sala = SalaSerializer(Sala.objects.get(id=proyeccion["sala"]))
            proyeccion["pelicula"] = pelicula.data
            proyeccion["sala"] = sala.data

        return JsonResponse(proyecciones_serialazer.data, safe=False, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        proyeccion_data = JSONParser().parse(request)
        proyecciones_serialazer = ProyeccionSerializer(data=proyeccion_data)
        if proyecciones_serialazer.is_valid():
            proyecciones_serialazer.save()
            return JsonResponse(proyecciones_serialazer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(proyecciones_serialazer.errors, status=status.HTTP_400_BAD_REQUEST)

# 
@api_view(['GET', 'PUT', 'DELETE'])
def proyeccion_detalle(request, clave):
    try:
        proyeccion = Proyeccion.objects.get(id=clave)
    except Proyeccion.DoesNotExist:
        return JsonResponse({'Error': 'La sala no existe'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        proyeccion_serializer = ProyeccionSerializer(proyeccion)
        return JsonResponse(proyeccion.data)

    elif request.method == 'PUT': 
        proyeccion_data = JSONParser().parse(request) 
        proyeccion_serializer = ProyeccionSerializer(proyeccion, data=proyeccion_data) 
        if proyeccion_serializer.is_valid(): 
            proyeccion_serializer.save() 
            return JsonResponse(proyeccion_serializer.data, status=status.HTTP_200_OK) 
        return JsonResponse(proyeccion_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE': 
        proyeccion.delete()
        return JsonResponse({'Hecho': 'La proyeccion ha sido eliminada satisfactoriamente!'}, status=status.HTTP_204_NO_CONTENT)

# Endpoint de Butacas.
@api_view(['GET'])
# Traer todas las butacas
def butacas_list(request):
    butacas = Butaca.objects.all()
    butacas_serializer = ButacaSerializer(butacas, many=True)
    return JsonResponse(butacas_serializer.data, safe=False, status=status.HTTP_200_OK)

# Traer una butaca por su id
@api_view(['GET'])
def butaca_reservada(request, id):
    try:
        butaca = Butaca.objects.get(pk=id)
    except Butaca.DoesNotExist:
        return JsonResponse({'mensaje': 'Esta butaca no existe'}, status=status.HTTP_404_NOT_FOUND)

    return JsonResponse(ButacaSerializer(butaca).data, safe=False)

# Subir una butaca
@api_view(['POST'])
def butaca_reserva(request, proyeccion, fila, asiento):
    try:
        butaca = Butaca.objects.get(proyeccion)
    except Butaca.DoesNotExist:
        return JsonResponse({'mensaje': 'Esa proyeccion no existe'}, status=status.HTTP_400_BAD_REQUEST)
    # Como eligo proyec, fila y asiento?
    butaca_data = JSONParser().parse(request)
    serializer = ButacaSerializer(data=butaca_data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

