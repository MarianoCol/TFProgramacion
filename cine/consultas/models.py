from django.db import models

# Create your models here.
class Pelicula(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    duracion = models.DurationField()
    descripcion = models.TextField(max_length=250)
    detalle = models.TextField(max_length=500)
    GENEROS_DISPONIBLES = [
        ('INDEFINIDO', 'Indefinido'),
        ('ACCION', 'Accion'),
        ('CIENCIA_FICCION', 'Ciencia Ficcion'),
        ('COMEDIA', 'Comedia'),
        ('DRAMA', 'Drama'),
        ('FANTASIA', 'Fantasia'),
        ('MELODRAMA', 'Melodrama'),
        ('MUSICAL', 'Musical'),
        ('ROMANCE', 'Romance'),
        ('SUSPENSO', 'Suspenso'),
        ('TERROR', 'Terror'),
        ('DOCUMENTAL', 'Documental'),
    ]
    genero = models.CharField(
        max_length=15,
        choices=GENEROS_DISPONIBLES,
        default='INDEFINIDO',
        )
    CLASIFICACIONES = [
        ('SINC', 'Sin clasificar'),
        ('ATP', 'ATP'),
        ('PLUS13', '+13'),
        ('PLUS16', '+16'),
        ('PLUS18', '+18'),
    ]
    clasificacion = models.CharField(
        max_length=8,
        choices=CLASIFICACIONES,
        default='SINC',
    )
    ESTADOS_PELICULAS = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
    ]
    estado = models.CharField(
        max_length=8,
        choices=ESTADOS_PELICULAS,
        default='INACTIVO',
    )
    fechaComienzo = models.DateField()
    fechaFinal = models.DateField()

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
    sala_id = models.ForeignKey(Sala, on_delete=models.CASCADE, default=1)
    pelicula_id = models.ForeignKey(Pelicula, on_delete=models.CASCADE, default=1)
    # fechaInicio = # [ObjetoPelicula.fechaComienzo?]
    # fechaFin = [ObjetoPelicula.fechaFinal?]
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

class Butaca(models.Model):
    id = models.AutoField(primary_key=True)
    proyeccion = models.ForeignKey(Proyeccion, on_delete=models.CASCADE, default=1)
    fecha_venta = models.DateTimeField()
    # Estos lugares no pueden ser de algun lugar ya ocupado
    fila = models.PositiveSmallIntegerField()
    asiento = models.PositiveSmallIntegerField()

