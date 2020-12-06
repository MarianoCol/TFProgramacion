from rest_framework import serializers
from consultas.models import Pelicula

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


