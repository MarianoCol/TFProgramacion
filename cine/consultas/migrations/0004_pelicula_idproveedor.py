# Generated by Django 3.1.3 on 2021-02-19 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultas', '0003_auto_20210212_2000'),
    ]

    operations = [
        migrations.AddField(
            model_name='pelicula',
            name='idProveedor',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
