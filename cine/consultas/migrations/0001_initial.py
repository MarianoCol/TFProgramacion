# Generated by Django 2.2.12 on 2020-11-17 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Butaca',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_venta', models.DateTimeField()),
                ('fila', models.PositiveSmallIntegerField()),
                ('asiento', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Pelicula',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('duracion', models.DurationField()),
                ('descripcion', models.TextField(max_length=250)),
                ('detalle', models.TextField(max_length=500)),
                ('genero', models.CharField(choices=[('INDEFINIDO', 'Indefinido'), ('ACCION', 'Accion'), ('CIENCIA_FICCION', 'Ciencia Ficcion'), ('COMEDIA', 'Comedia'), ('DRAMA', 'Drama'), ('FANTASIA', 'Fantasia'), ('MELODRAMA', 'Melodrama'), ('MUSICAL', 'Musical'), ('ROMANCE', 'Romance'), ('SUSPENSO', 'Suspenso'), ('TERROR', 'Terror'), ('DOCUMENTAL', 'Documental')], default='INDEFINIDO', max_length=15)),
                ('clasificacion', models.CharField(choices=[('SINC', 'Sin clasificar'), ('ATP', 'ATP'), ('PLUS13', '+13'), ('PLUS16', '+16'), ('PLUS18', '+18')], default='SINC', max_length=8)),
                ('estado', models.CharField(choices=[('ACTIVO', 'Activo'), ('INACTIVO', 'Inactivo')], default='INACTIVO', max_length=8)),
                ('fechaComienzo', models.DateField()),
                ('fechaFinal', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Proyeccion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('hora_proyeccion', models.DateTimeField()),
                ('estado', models.CharField(choices=[('ACTIVO', 'Activo'), ('INACTIVO', 'Inactivo')], default='ACTIVO', max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Sala',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=10)),
                ('estado', models.CharField(choices=[('HABILITADA', 'Habilitada'), ('DESHABILITADA', 'Deshabilitada'), ('ELIMINADA', 'Eliminada')], default='HABILITADA', max_length=13)),
                ('filas', models.PositiveSmallIntegerField()),
                ('asientos', models.PositiveSmallIntegerField()),
            ],
        ),
    ]
