# Generated by Django 3.1.3 on 2021-02-24 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultas', '0002_auto_20210224_0028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='butaca',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='pelicula',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='proyeccion',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='sala',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
    ]