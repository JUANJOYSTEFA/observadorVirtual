# Generated by Django 4.2.20 on 2025-03-27 01:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Observador', '0014_citaciones_asistencia'),
    ]

    operations = [
        migrations.AddField(
            model_name='administrativos',
            name='idColegio',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='administrativos', to='Observador.colegio'),
        ),
    ]
