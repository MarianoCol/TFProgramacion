from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from consultas.serializers import ConsultaSerializer, SalaSerializer, ProyeccionSerializer, ButacaSerializer
from consultas.models import Pelicula, Sala, Butaca, Proyeccion
from rest_framework.decorators import api_view

# Vistas

def index(request):
    template = loader.get_template('polls/index.html')
    context = {
        'prueba': True,
    }
    return HttpResponse(template.render(context, request))

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


@api_view(['GET'])
def proyeccion_list(request):
    lista_peliculas = []
    lista_salas = []
    if request.method == 'GET':
        proyecciones = Proyeccion.objects.all()
        for proyeccion in proyecciones:
            pelicula = Pelicula.objects.get(id=proyecciones.pelicula_id)
            sala = Sala.objects.get(id=proyecciones.sala_id)
            if pelicula.nombre == nombre:
                lista_peliculas.append(pelicula)
                lista_salas.append(sala)

        proyecciones_serialazer = ProyeccionSerializer(proyecciones, many=True)
        salas_serialazer = SalaSerializer(lista_salas)
        pelicula_serializer = ConsultaSerializer(lista_peliculas)
        return JsonResponse(proyecciones_serialazer.data, salas_serialazer.data, pelicula_serializer.data, safe=False)

    elif request.method == 'POST':
        proyeccion_data = JSONParser().parse(request)
        proyecciones_serialazer = ProyeccionSerializer(data=proyeccion_data)
        if proyecciones_serialazer.is_valid():
            proyecciones_serialazer.save()
            return JsonResponse(proyecciones_serialazer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(proyecciones_serialazer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
def proyeccion_detalle(request, id):
    try:
        proyeccion = Proyeccion.objects.get()
    except Sala.DoesNotExist:
        return JsonResponse({'Error': 'La sala no existe'})

# Endpoint de Butacas. ---------------------------<>
@api_view(['GET'])
# Traer todas las butacas
def butacas_list(request):
    butacas = Butaca.objects.all()
    butacas_serializer = ButacaSerializer(butacas, many=True)
    return JsonResponse(butacas_serializer.data, safe=False)

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
def butaca_reserva(request):
    if request.method == 'POST':
        try:
            p = Proyeccion.objects.get(request.estado)
        except p.estado == 'INACTIVO':
            return JsonResponse({'mensaje': 'Esa proyeccion no existe'}, status=status.HTTP_400_BAD_REQUEST)
        butaca_data = JSONParser().parse(request)
        serializer = ButacaSerializer(data=butaca_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

