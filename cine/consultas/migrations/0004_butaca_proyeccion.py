# Generated by Django 3.1.3 on 2020-11-17 23:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('consultas', '0003_auto_20201117_2113'),
    ]

    operations = [
        migrations.AddField(
            model_name='butaca',
            name='proyeccion',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='consultas.proyeccion'),
        ),
    ]
