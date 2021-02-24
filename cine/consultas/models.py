from django.db import models
import django.utils.timezone as tz

# Create your models here.
class Pelicula(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    nombre = models.CharField(max_length=300, unique=True)
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
    ESTADOS_PELICULAS = [
        ('ACTIVA', 'ACTIVA'),
        ('INACTIVA', 'INACTIVA'),
    ]
    estado = models.CharField(
        choices=ESTADOS_PELICULAS,
        max_length=10,
        default='ACTIVA',
    )
    fechaComienzo = models.DateTimeField(null=True)
    fechaFinalizacion = models.DateTimeField(null=True)
    idProveedor = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre

class Sala(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    nombre = models.CharField(max_length=10, unique=True) # ej. SALA1, SALA2, SALA3, ...
    ESTADOS_SALAS = [
        ('HABILITADA', 'HABILITADA'),
        ('DESHABILITADA', 'DESHABILITADA'),
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
    id = models.AutoField(primary_key=True, unique=True)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE)
    fechaInicio = models.DateField(default="01-01-2020")
    fechaFin = models.DateField(default="01-01-2020")
    hora_proyeccion = models.DateTimeField()
    ESTADOS_PROYECCION = [
        ('ACTIVO', 'ACTIVO'),
        ('INACTIVO', 'INACTIVO'),
    ]
    estado = models.CharField(
        max_length=8,
        choices=ESTADOS_PROYECCION,
        default='ACTIVO',
    )

    def __str__(self):
        return f'S:{self.sala_id}, P:{self.pelicula_id} T:{self.hora_proyeccion}'

class Butaca(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    proyeccion = models.ForeignKey(Proyeccion, on_delete=models.CASCADE, default=1)
    fecha_venta = models.DateTimeField()
    fila = models.PositiveSmallIntegerField()
    asiento = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'Proyeccion: [{self.proyeccion}] | Venta: [{self.fecha_venta} F: {self.fila} A: {self.asiento}]'

