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
def pelicula_detalle(request, id, fechaInicio, fechaFin):
    try:
        pelicula = Pelicula.objects.get(pk=id)
        proyecciones = Proyeccion.objects.filter(
            pelicula=id,
            fechaInicio__range=[fechaInicio, fechaFin],
            fechaFin__range=[fechaInicio, fechaFin]
            )
    except Pelicula.DoesNotExist:
        return JsonResponse({'mensaje': 'La pelicula no existe'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        disponible = []
        proyeccion_serializer = ProyeccionSerializer(proyecciones, many=True)
        
        for i in proyeccion_serializer.data:
            disponible.append(i['fechaInicio'])
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
def sala(request):
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
def sala_detalle(request, id):
    try:
        sala = Sala.objects.get(pk=id)
    except Sala.DoesNotExist:
        return JsonResponse({'error': 'La sala no existe'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        sala_serializer = SalaSerializer(sala)
        return JsonResponse(sala_serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        sala_data = JSONParser().parse(request)
        try:
            Sala.objects.filter(pk=id).update(**sala_data)
            return JsonResponse({'update': sala_data}, status=status.HTTP_200_OK)
        except Exception as ex: 
            return JsonResponse({'error': str(ex)}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Si la sala estaba habilitada la paso deshabilitada
        if sala.estado == 'HABILITADA':
            sala = Sala.objects.filter(pk=id).update(estado='DESHABILITADA')
            return JsonResponse({'mensaje': 'estado de sala -> DESHABILITADA'}, status=status.HTTP_204_NO_CONTENT)
        # Si la sala estaba deshabilitada la elimino definitivamente
        else:
            sala.delete()
            return JsonResponse({'mensaje': 'sala eliminada definitivamente!'}, status=status.HTTP_204_NO_CONTENT)
            

# Endpoint de Proyeccion <------------------------------------>
# Trear las proyecciones activas, subir una nueva proyeccion.
@api_view(['GET', 'POST', 'PUT'])
def proyeccion_list(request):
    if request.method == 'GET':
        # Cada vez que se hace un get, se consulta si las salas estan habilitadas o estan las peliculas activas
        proyecciones = Proyeccion.objects.all()
        for proyeccion in proyecciones:
            pelicula = Pelicula.objects.get(pk=proyeccion.pelicula.id)
            sala = Sala.objects.get(pk=proyeccion.sala.id)
            pFilter = Proyeccion.objects.filter(pelicula=proyeccion.pelicula.pk, sala=proyeccion.sala.pk)
            if (sala.estado.upper() == "HABILITADA") and (pelicula.estado.upper() == "ACTIVA"):
                pFilter.update(estado='ACTIVO')
            else:
                pFilter.update(estado='INACTIVO')

        pActivs = Proyeccion.objects.filter(estado='ACTIVO')
        ret = dict()
        for ct, pA in enumerate(pActivs):
            dicPro = model_to_dict(pA)
            dicPro['pelicula'] = model_to_dict(Pelicula.objects.get(pk=pA.pelicula.id))
            dicPro['sala'] = model_to_dict(Sala.objects.get(pk=pA.sala.id))
            ret.update({str(ct): dicPro})
        return JsonResponse(ret, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # Publicar una nueva proyeccion
        proyeccion_data = JSONParser().parse(request)
        proyecciones_serialazer = ProyeccionSerializer(data=proyeccion_data)
        try:
            proyecciones_serialazer.is_valid()
            proyDic = proyecciones_serialazer.validated_data
            if not Proyeccion.objects.filter(**proyDic):
                pelicula = Pelicula.objects.get(pk=proyDic['pelicula'].pk)
                sala = Sala.objects.get(pk=proyDic['sala'].pk)
                if (sala.estado.upper() != "HABILITADA") or (pelicula.estado.upper() != "ACTIVA"):
                    return JsonResponse({'mensaje':'sala o pelicula, no activa'}, status=status.HTTP_400_BAD_REQUEST)
                elif proyDic['fechaInicio'] >= proyDic['fechaFin']:
                        return JsonResponse({'mensaje':'rango de fechas invalido'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    if proyecciones_serialazer.is_valid():
                        proyecciones_serialazer.save()
                        return JsonResponse({'mensaje':'proyeccion creada'}, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({'error':'ya existe una proyeccion igual'}, status=status.HTTP_409_CONFLICT)
        except Exception as ex:
            return JsonResponse({'error': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def proyeccion_mod(request, id):
    if request.method == 'PUT': 
        proyeccion_data = JSONParser().parse(request)
        try:
            proyeccion = Proyeccion.objects.filter(pk=id)
            if not proyeccion:
                return JsonResponse({'mensaje':'La proyeccion no existe'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                proyeccion.update(**proyeccion_data)
                return JsonResponse(model_to_dict(proyeccion.get(pk=id)), status=status.HTTP_200_OK) 
        except Exception as ex:
            return JsonResponse({'error': str(ex)}, status=status.HTTP_400_BAD_REQUEST)

# Trear una proyeccion por rango de fechas
@api_view(['GET'])
def proyeccion_rango(request, fechaInicio, fechaFin):
    fechaInicio += 'T00:00:00Z'
    fechaFin += 'T00:00:00Z'
    proyecciones = Proyeccion.objects.filter(hora_proyeccion__range=[fechaInicio, fechaFin], estado='ACTIVO')

    if not proyecciones:
        return JsonResponse({'mensaje': 'No hay proyecciones en este rango'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        ret = {}
        for ct, pA in enumerate(proyecciones):
            dicPro = model_to_dict(pA)
            dicPro['pelicula'] = model_to_dict(Pelicula.objects.get(pk=pA.pelicula.id))
            dicPro['sala'] = model_to_dict(Sala.objects.get(pk=pA.sala.id))
            ret.update({str(ct): dicPro})
        return JsonResponse(ret, status=status.HTTP_200_OK)

# Trear una proyeccion y una fecha
@api_view(['GET'])
def proyeccion_fecha(request, peliId, fecha):
    if request.method == 'GET':
        try:
            proyeccion = Proyeccion.objects.filter(pelicula=peliId, hora_proyeccion=fecha, estado='ACTIVO')
            if not proyeccion:
                return JsonResponse({'mensaje': 'no existe proyeccion'}, status=status.HTTP_404_NOT_FOUND)
            else:
                butacas = Butaca.objects.filter(proyeccion=proyeccion.get().pk)
                sala = Sala.objects.get(pk=proyeccion.get().sala.pk)
                list = []
                for n in range(sala.filas):
                    for m in range(sala.asientos):
                        for b in butacas:
                            if (b.fila == n) and (b.asiento == m):
                                list.append(tuple([n,m,'r']))
                            else:
                                list.append(tuple([n,m,'l']))
                dicPro = model_to_dict(proyeccion.get())
                dicPro['pelicula'] = model_to_dict(Pelicula.objects.get(pk=peliId))
                dicPro['sala'] = model_to_dict(sala)
                dicPro.update({'butacas': list})
                return JsonResponse(dicPro, status=status.HTTP_200_OK)
        except Exception as ex:
            return JsonResponse({'error': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
    try:
        proyeccion = Proyeccion.objects.get(pk=butaca.proyeccion.pk)
        butDic = ButacaSerializer(butaca).data
        proDic = ProyeccionSerializer(proyeccion).data
        proDic ['pelicula'] = ConsultaSerializer(Pelicula.objects.get(pk=proyeccion.pelicula.pk)).data
        butDic['proyeccion'] = proDic
        return JsonResponse(butDic, safe=False, status=status.HTTP_200_OK)
    except Exception as ex:
        return JsonResponse({'error': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Subir una butaca o modificarla
@api_view(['POST'])
def butaca_reserva(request):
    if request.method == 'POST':
        try:
            butaca_data = JSONParser().parse(request)
            proyeccion = Proyeccion.objects.filter(pk=butaca_data['proyeccion'])
            if not proyeccion:
                return JsonResponse({'error': 'proyeccion no existe'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Compruebo que no exista butaca asignada a esa proyeccion
                butaca = Butaca.objects.filter(
                    proyeccion=butaca_data['proyeccion'],
                    fila=butaca_data['fila'],
                    asiento=butaca_data['asiento']
                    )
                if not butaca:
                    serializer = ButacaSerializer(data=butaca_data)
                    if serializer.is_valid():
                        serializer.save()
                        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return JsonResponse({'error': 'butaca no disponible'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return JsonResponse({'error': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def butaca_mod(request, id):
    if request.method == 'PUT':
        butaca_data = JSONParser().parse(request)
        try:
            butaca = Butaca.objects.filter(pk=id)
            if not butaca:
                return JsonResponse({'error': 'butaca no existe'}, status=status.HTTP_404_NOT_FOUND)
            else:
                butaca.update(**butaca_data)
                return JsonResponse(model_to_dict(butaca.get(pk=id)), status=status.HTTP_200_OK) 
        except Exception as ex:
            return JsonResponse({'error': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
            peliExterna.pop('id')
            try:
                if not peliExternaEnBase:
                    # Si la peli no esta en la base, la agregamos
                    peliExterna['idProveedor'] = idP
                    peliExterna['estado'] = peliExterna['estado'].upper()
                    Pelicula_serializer = ConsultaSerializer(data=peliExterna)
                    if Pelicula_serializer.is_valid(raise_exception=True):
                        Pelicula_serializer.save()
                else:
                    # Si esta en la base, actualizamos
                    peliExternaEnBaseDict = model_to_dict(peliExternaEnBase.get())
                    peliExternaEnBaseDict.update(peliExterna)
                    peliExternaEnBase.update(**peliExternaEnBaseDict)
            except Exception as ex:
                return JsonResponse({'error': str(ex)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)             
        return JsonResponse({'mensaje':'Base de peliculas, actualizada'}, safe=False, status=status.HTTP_200_OK)
