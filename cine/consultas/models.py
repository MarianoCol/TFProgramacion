from django.db import models
import django.utils.timezone as tz

# Create your models here.
class Pelicula(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=300)
    duracion = models.IntegerField()
    descripcion = models.TextField(max_length=1000)
    detalle = models.TextField(max_length=10000)
    genero = models.CharField(
        max_length=100,
        default='INDEFINIDO',
        )
    clasificacion = models.CharField(
        max_length=100,
        default='SINC',
    )
    estado = models.CharField(
        max_length=10,
        default='INACTIVO',
    )
    fechaComienzo = models.DateTimeField(default=tz.now)
    fechaFinalizacion = models.DateTimeField(default=tz.now)

    def __str__(self):
        return self.nombre

class Sala(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=10) # ej. SALA1, SALA2, SALA3, ...
    ESTADOS_SALAS = [
        ('HABILITADA', 'Habilitada'),
        ('DESHABILITADA', 'Deshabilitada'),
        ('ELIMINADA', 'Eliminada'),
    ]
    estado = models.CharField(
        max_length=13,
        choices=ESTADOS_SALAS,
        default='HABILITADA',
    )
    filas = models.PositiveSmallIntegerField()
    asientos = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.nombre
    
class Proyeccion(models.Model):
    id = models.AutoField(primary_key=True)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    fechaInicio = models.DateField(default="2019-01-01")
    fechaFin = models.DateField(default="2020-01-01")
    hora_proyeccion = models.DateTimeField()
    ESTADOS_PROYECCION = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
    ]
    estado = models.CharField(
        max_length=8,
        choices=ESTADOS_PROYECCION,
        default='ACTIVO',
    )

    def __str__(self):
        return f'S:{self.sala_id}, P:{self.pelicula_id} T:{self.hora_proyeccion}'

class Butaca(models.Model):
    id = models.AutoField(primary_key=True)
    proyeccion = models.ForeignKey(Proyeccion, on_delete=models.CASCADE, default=1)
    fecha_venta = models.DateTimeField()
    # Estos lugares no pueden ser de algun lugar ya ocupado
    fila = models.PositiveSmallIntegerField()
    asiento = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'Proyeccion: [{self.proyeccion}] | Venta: [{self.fecha_venta} F: {self.fila} A: {self.asiento}]'

