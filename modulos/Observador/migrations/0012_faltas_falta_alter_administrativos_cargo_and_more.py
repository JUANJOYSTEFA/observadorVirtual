# Generated by Django 5.1.1 on 2025-02-27 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Observador', '0011_alter_grado_options_alter_grado_grado'),
    ]

    operations = [
        migrations.AddField(
            model_name='faltas',
            name='falta',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='administrativos',
            name='cargo',
            field=models.CharField(choices=[('profesor', 'Profesor'), ('directivo', 'Directivo')], default='profesor', max_length=9),
        ),
        migrations.AlterField(
            model_name='administrativos',
            name='ciclo',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='faltas',
            name='tipoFalta',
            field=models.IntegerField(choices=[(1, 'Tipo 1'), (2, 'Tipo 2'), (3, 'Tipo 3')], default=1),
        ),
    ]
