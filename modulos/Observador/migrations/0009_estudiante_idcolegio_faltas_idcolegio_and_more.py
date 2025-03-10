# Generated by Django 5.1.1 on 2025-02-26 00:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Observador', '0008_colegio_alter_acudiente_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='estudiante',
            name='idColegio',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='estudiantes', to='Observador.colegio'),
        ),
        migrations.AddField(
            model_name='faltas',
            name='idColegio',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='faltas', to='Observador.colegio'),
        ),
        migrations.AddField(
            model_name='grado',
            name='idColegio',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='grado', to='Observador.colegio'),
        ),
    ]
