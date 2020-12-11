from rest_framework import serializers
from consultas.models import Pelicula, Sala, Butaca, Proyeccion

class ConsultaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pelicula
        fields = ('id',
        'nombre',
        'duracion',
        'descripcion',
        'detalle',
        'genero',
        'clasificacion',
        'estado',
        'fechaComienzo',
        'fechaFinal')

class SalaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sala
        fields = ('id',
        'nombre',
        'estado',
        'filas',
        'asientos')


class ButacaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Butaca
        fields = (
            'id',
            'proyeccion',
            'fecha_venta',
            'fila',
            'asiento'
        )