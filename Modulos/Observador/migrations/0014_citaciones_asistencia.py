# Generated by Django 4.2.20 on 2025-03-27 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Observador', '0013_remove_observacion_idgrado_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='citaciones',
            name='asistencia',
            field=models.BooleanField(default=False),
        ),
    ]
