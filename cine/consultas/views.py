from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http.response import JsonResponse
from django.db.models import Count, Sum, Q
from django.forms.models import model_to_dict

from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view

from consultas.serializers import ConsultaSerializer, SalaSerializer, ProyeccionSerializer, ButacaSerializer
from consultas.models import Pelicula, Sala, Butaca, Proyeccion

import urllib, json
# Vistas

def index(request):
    template = loader.get_template('index.html')
    context = {
        'prueba': True,
    }
    return HttpResponse(template.render(context, request))

# Endpoint de Peliculas.  <------------------------------------>
# Treaer todas las peliculas
@api_view(['GET'])
def peliculas(request):
    if request.method == 'GET':
        try:
            peliculas = Pelicula.objects.all()
        except Pelicula.DoesNotExist:
            return JsonResponse({'mensaje': 'No hay peliculas'}, status=status.HTTP_404_NOT_FOUND)
        peliculas_serializer = ConsultaSerializer(peliculas, many=True)
        return JsonResponse(peliculas_serializer.data, safe=False, status=status.HTTP_200_OK)

# Traer disponibilidad de una pelicula
@api_view(['GET'])
def pelicula_detalle(request, nombre, fechaInicio, fechaFin):
    try:
        pelicula = Pelicula.objects.get(nombre=nombre)
        proyecciones = Proyeccion.objects.filter(
            Q(pelicula=pelicula.id) &
            (Q(fechaInicio__lte=fechaFin) & Q(fechaFin__gte=fechaInicio)) |
            (Q(fechaInicio__lte=fechaInicio) & Q(fechaInicio__gte=fechaInicio)) |
            (Q(fechaFin__gte=fechaFin) & Q(fechaFin__lte=fechaFin))
        )
    except Pelicula.DoesNotExist:
        return JsonResponse({'mensaje': 'La pelicula no existe'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        disponible = []
        proyeccion_serializer = ProyeccionSerializer(proyecciones, many=True)
        
        for i in proyeccion_serializer.data:
            disponible.append(i['fechaInicio'])
        # for i in range(delta.days + 1):
        #     disponible.append(fechaInicio + datetime.timedelta(days=i))
        pelicula_serializer = ConsultaSerializer(pelicula)
        newDic = {}
        newDic.update(pelicula_serializer.data)
        newDic.update({'disponilbe': disponible})
        return JsonResponse(newDic, status=status.HTTP_200_OK)

# Traer peliculas en un rango de fechas
@api_view(['GET'])
def pelicula_fechas(request, fechaInicio, fechaFin):
    pelicula = Pelicula.objects.filter(fechaComienzo__gte=fechaInicio, fechaFinalizacion__lte=fechaFin)

    if pelicula.count() == 0:
        return JsonResponse({'mensaje': 'No hay peliculas en este rango'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        pelicula_serializer = ConsultaSerializer(pelicula, many=True)
        return JsonResponse(pelicula_serializer.data, status=status.HTTP_200_OK, safe=False)

# Endpoint de Salas.  <------------------------------------>
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

# Endpoint de Proyeccion <------------------------------------>
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
        try:
            proyeccion = Proyeccion.objects.get(
                sala=proyeccion_data['sala'],
                pelicula=proyeccion_data['pelicula'],
                hora_proyeccion=proyeccion_data['hora_proyeccion']
            )
        except:
            return JsonResponse({'mensaje':'La proyeccion no existe'}, status=status.HTTP_400_BAD_REQUEST)
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

# Endpoint de Butacas.  <------------------------------------>
# Traer todas las butacas
@api_view(['GET'])
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

    return JsonResponse(ButacaSerializer(butaca).data, safe=False, status=status.HTTP_200_OK)

# Subir una butaca o modificarla
@api_view(['POST', 'PUT'])
def butaca_reserva(request):
    try:
        butaca_data = JSONParser().parse(request)
        butaca = Butaca.objects.filter(proyeccion=butaca_data['proyeccion'])
    except Butaca.DoesNotExist:
        return JsonResponse({'mensaje': 'Esa proyeccion no existe'}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'POST':
        serializer = ButacaSerializer(data=butaca_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT': 
        butaca = Butaca.objects.get(pk=butaca_data['id'])
        butaca_serializer = ButacaSerializer(butaca, data=butaca_data) 
        if butaca_serializer.is_valid(): 
            butaca_serializer.save() 
            return JsonResponse(butaca_serializer.data, status=status.HTTP_200_OK) 
        return JsonResponse(butaca_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Endpoint reportes <------------------------------------>
# Reporte butacas rendidas en un rango de tiempo
def butacas_vendidas(request, fechaInicio, fechaFin):
    butacas = Butaca.objects.filter(fecha_venta__gte=fechaInicio, fecha_venta__lte=fechaFin)

    if butacas.count() == 0:
        return JsonResponse({'mensaje': 'No hay peliculas en este rango'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        butaca_serializer = ButacaSerializer(butacas, many=True)

        return JsonResponse(butaca_serializer.data, safe=False, status=status.HTTP_200_OK)

# Butacas vendidas de una proyeccion
@api_view(['GET'])
def butacas_vendidas_proyeccion(request, proyeccion, fechaInicio, fechaFin):
    butacas = Butaca.objects.filter(proyeccion=proyeccion, fecha_venta__gte=fechaInicio, fecha_venta__lte=fechaFin)

    if butacas.count() == 0:
        return JsonResponse({'mensaje': 'No hay peliculas en este rango'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        butaca_serializer = ButacaSerializer(butacas, many=True)

        return JsonResponse(butaca_serializer.data, safe=False, status=status.HTTP_200_OK)

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

        return JsonResponse(newDic, safe=False, status=status.HTTP_200_OK)

# Venta de peliculas
@api_view(['GET'])
def peliculas_rank(request):
    proyes = Proyeccion.objects.all().values('pelicula_id', 'id').annotate(total=Count('pelicula_id')).order_by('-total')
    
    if proyes.count() == 0:
        return JsonResponse({'mensaje': 'No hay peliculas en este rango'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        cont = 1
        newDic = {}
        for proye in proyes:
            butacas = Butaca.objects.all().filter(proyeccion=proye['id']).values('proyeccion_id').annotate(total=Count('proyeccion_id')).order_by('-total')
            
            for butaca in butacas:
                pelicula = Pelicula.objects.get(id=proye['pelicula_id'])
                pelicula_serialazer = ConsultaSerializer(pelicula)
                
                if pelicula != {}:
                    if (cont == 1):
                        name = 'Top' + str(cont)
                        newDic[name] = pelicula_serialazer.data
                        newDic[name]['Ventas'] = butaca['total']

                        cont += 1

                    elif (pelicula_serialazer.data['nombre'] != newDic['Top' + str(cont - 1)]['nombre']):
                        name = 'Top' + str(cont)
                        newDic[name] = pelicula_serialazer.data
                        newDic[name]['Ventas'] = butaca['total']

                        cont += 1

                    elif (pelicula_serialazer.data['nombre'] == newDic['Top' + str(cont - 1)]['nombre']):
                        newDic['Top' + str(cont - 1)]['Ventas'] += butaca['total']

        valores_ord = dict(sorted(newDic.items(), reverse=True))
        
        return JsonResponse(valores_ord, safe=False, status=status.HTTP_200_OK)

# Consumo endpoint de profesores

@api_view(['POST'])
def peliculas_profes(request):
    if request.method == 'POST':
        try:
            url = "http://localhost:8001/api/pelicula/"
            response = urllib.request.urlopen(url)
            datas = json.loads(response.read())
        except Exception as ex:
            return JsonResponse({'error': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if not datas:
            return JsonResponse({'mensaje':'No hay peliculas externas'}, safe=False, status=status.HTTP_200_OK)
        for peliExterna in datas:
            idP = peliExterna['id']
            peliExternaEnBase = Pelicula.objects.filter(idProveedor=idP)
            try:
                if not peliExternaEnBase:
                    # Si la peli no esta en la base, la agregamos
                    peliExterna['idProveedor'] = peliExterna['id']
                    Pelicula_serializer = ConsultaSerializer(data=peliExterna)
                    if Pelicula_serializer.is_valid():
                        Pelicula_serializer.save()
                else:
                    # Si esta en la base, actualizamos
                    peliExternaEnBaseDict = model_to_dict(peliExternaEnBase.get())
                    peliExterna.pop('id')
                    peliExternaEnBaseDict.update(peliExterna)
                    peliExternaEnBase.update(**peliExternaEnBaseDict)
            except Exception as ex:
                return JsonResponse({'error': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)             
        return JsonResponse({'mensaje':'Base de peliculas, actualizada'}, safe=False, status=status.HTTP_200_OK)
