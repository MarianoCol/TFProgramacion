# Generated by Django 3.1.3 on 2021-02-24 00:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pelicula',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=300, unique=True)),
                ('duracion', models.IntegerField()),
                ('descripcion', models.TextField(max_length=1000)),
                ('detalle', models.TextField(max_length=10000)),
                ('genero', models.CharField(default='INDEFINIDO', max_length=100)),
                ('clasificacion', models.CharField(default='SINC', max_length=100)),
                ('estado', models.CharField(default='ACTIVA', max_length=10)),
                ('fechaComienzo', models.DateTimeField(auto_now=True, null=True)),
                ('fechaFinalizacion', models.DateTimeField(null=True)),
                ('idProveedor', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Sala',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=10, unique=True)),
                ('estado', models.CharField(choices=[('HABILITADA', 'Habilitada'), ('DESHABILITADA', 'Deshabilitada'), ('ELIMINADA', 'Eliminada')], default='HABILITADA', max_length=13)),
                ('filas', models.PositiveSmallIntegerField()),
                ('asientos', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Proyeccion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fechaInicio', models.DateField(default='01-01-2020')),
                ('fechaFin', models.DateField(default='01-01-2020')),
                ('hora_proyeccion', models.DateTimeField()),
                ('estado', models.CharField(choices=[('ACTIVO', 'Activo'), ('INACTIVO', 'Inactivo')], default='ACTIVO', max_length=8)),
                ('pelicula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consultas.pelicula')),
                ('sala', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consultas.sala')),
            ],
        ),
        migrations.CreateModel(
            name='Butaca',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_venta', models.DateTimeField()),
                ('fila', models.PositiveSmallIntegerField()),
                ('asiento', models.PositiveSmallIntegerField()),
                ('proyeccion', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='consultas.proyeccion')),
            ],
        ),
    ]
