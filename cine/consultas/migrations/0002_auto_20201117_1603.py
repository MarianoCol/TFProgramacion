# Generated by Django 2.2.12 on 2020-11-17 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consultas', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Butacas',
            new_name='Butaca',
        ),
        migrations.RenameModel(
            old_name='Peliculas',
            new_name='Pelicula',
        ),
        migrations.RenameModel(
            old_name='Salas',
            new_name='Sala',
        ),
    ]
