from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http.response import JsonResponse
from django.db.models import Q
from django.db.models import Count, Sum

from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view

from consultas.serializers import ConsultaSerializer, SalaSerializer, ProyeccionSerializer, ButacaSerializer
from consultas.models import Pelicula, Sala, Butaca, Proyeccion

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
# Trear las proyecciones activas, subir una nueva proyeccion y modificar proyeccion.
@api_view(['GET', 'POST', 'PUT'])
def proyeccion_list(request):
    if request.method == 'GET':
        proyecciones = Proyeccion.objects.filter(estado="ACTIVO")
        proyecciones_serialazer = ProyeccionSerializer(proyecciones, many=True)

        for proyeccion in proyecciones_serialazer.data:
            pelicula = ConsultaSerializer(Pelicula.objects.get(id=proyeccion["pelicula"]))
            sala = SalaSerializer(Sala.objects.get(id=proyeccion["sala"]))
            if sala.data["estado"] == "HABILITADA" and pelicula.data["estado"] == "ACTIVO":
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

    elif request.method == 'PUT': 
        proyeccion_data = JSONParser().parse(request) 
        proyeccion_serializer = ProyeccionSerializer(proyeccion, data=proyeccion_data) 
        if proyeccion_serializer.is_valid(): 
            proyeccion_serializer.save() 
            return JsonResponse(proyeccion_serializer.data, status=status.HTTP_200_OK) 
        return JsonResponse(proyeccion_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Trear una proyeccion por rango de fechas
@api_view(['GET'])
def proyeccion_rango(request, fechaInicio, fechaFin):
    proyeccion = Proyeccion.objects.filter(fechaInicio__gte=fechaInicio, fechaFin__lte=fechaFin)

    if proyeccion.count() == 0:
        return JsonResponse({'mensaje': 'No hay proyecciones en este rango'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        proyeccion_serializer = ProyeccionSerializer(proyeccion, many=True)
        return JsonResponse(proyeccion_serializer.data, safe=False, status=status.HTTP_200_OK)

# Trear una proyeccion y una fecha
@api_view(['GET'])
def proyeccion_fecha(request, peli, fecha):
    try:
        nombre_pelicula = Pelicula.objects.values('id').get(nombre=peli)
        proyeccion = Proyeccion.objects.get(pelicula=nombre_pelicula['id'], hora_proyeccion=fecha)
    except Proyeccion.DoesNotExist:
        return JsonResponse({'mensaje': 'No existe proyeccion para esa pelicula'}, status=status.HTTP_404_NOT_FOUND)   
    if request.method == 'GET':
        proyeccion_serializer = ProyeccionSerializer(proyeccion)
        return JsonResponse(proyeccion_serializer.data, safe=False, status=status.HTTP_200_OK)

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

# Subir una butaca o modificarla
@api_view(['POST', 'PUT'])
def butaca_reserva(request):
    try:
        butaca = Butaca.objects.get(proyeccion)
    except Butaca.DoesNotExist:
        return JsonResponse({'mensaje': 'Esa proyeccion no existe'}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'POST':
        butaca_data = JSONParser().parse(request)
        serializer = ButacaSerializer(data=butaca_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT': 
        butaca_data = JSONParser().parse(request) 
        butaca_serializer = ButacaSerializer(butaca, data=butaca_data) 
        if butaca_serializer.is_valid(): 
            butaca_serializer.save() 
            return JsonResponse(butaca_serializer.data, status=status.HTTP_200_OK) 
        return JsonResponse(butaca_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Reporte butacas rendidas en un rango de tiempo
def butacas_vendidas(request, fechaInicio, fechaFin):
    butacas = Butaca.objects.filter(fecha_venta__gte=fechaInicio, fecha_venta__lte=fechaFin)

    if butacas.count() == 0:
        return JsonResponse({'mensaje': 'No hay peliculas en este rango'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        butaca_serializer = ButacaSerializer(butacas, many=True)

        return JsonResponse(butaca_serializer.data, safe=False)

# Butacas vendidas de una proyeccion
@api_view(['GET'])
def butacas_vendidas_proyeccion(request, proyeccion, fechaInicio, fechaFin):
    butacas = Butaca.objects.filter(proyeccion=proyeccion, fecha_venta__gte=fechaInicio, fecha_venta__lte=fechaFin)

    if butacas.count() == 0:
        return JsonResponse({'mensaje': 'No hay peliculas en este rango'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        butaca_serializer = ButacaSerializer(butacas, many=True)

        return JsonResponse(butaca_serializer.data, safe=False)

# Endpoint reportes
# La top 5 butacas mas vendidas
@api_view(['GET'])
def butacas_vendidas_rank(request, fechaInicio, fechaFin):    
    but = Butaca.objects.all().values('proyeccion_id').annotate(total=Count('proyeccion_id')).order_by('-total')[:5]    

    if but.count() == 0:
        return JsonResponse({'mensaje': 'No hay peliculas en este rango'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        cont = 1
        newDic = {}
        for butaca in but:
            proyeccion = Proyeccion.objects.get(id=butaca['proyeccion_id'])
            proyecciones_serialazer = ProyeccionSerializer(proyeccion)
            
            name = 'Top' + str(cont)
            newDic[name] = proyecciones_serialazer.data
            newDic[name]['Ventas'] = butaca['total']

            cont += 1

        return JsonResponse(newDic, safe=False)

# Venta de peliculas
@api_view(['GET'])
def peliculas_rank(request):    
    but = Butaca.objects.all().values('proyeccion_id').annotate(total=Count('proyeccion_id')).order_by('-total')   

    if but.count() == 0:
        return JsonResponse({'mensaje': 'No hay peliculas en este rango'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        cont = 1
        newDic = {}
        for butaca in but:
            proyeccion = Proyeccion.objects.get(id=butaca['proyeccion_id'])
            proyecciones_serialazer = ProyeccionSerializer(proyeccion)

            pelicula = Pelicula.objects.get(id=proyecciones_serialazer.data['pelicula_id'], estado='ACTIVO')

            if pelicula.count() != 0:
                proyecciones_serialazer = ProyeccionSerializer(proyeccion)
                pelicula_serialazer = ConsultaSerializer(pelicula)
                
                name = 'Top' + str(cont)
                newDic[name] = pelicula_serialazer.data
                newDic[name]['Ventas'] = butaca['total']
