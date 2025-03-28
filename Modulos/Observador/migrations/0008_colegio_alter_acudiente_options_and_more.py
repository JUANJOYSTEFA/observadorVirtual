# Generated by Django 5.1.1 on 2025-02-26 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Observador', '0007_rename_identificacion_estudiante_documento'),
    ]

    operations = [
        migrations.CreateModel(
            name='Colegio',
            fields=[
                ('idColegio', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('direccion', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=13)),
                ('email', models.EmailField(max_length=100)),
            ],
            options={
                'verbose_name': 'Colegio',
            },
        ),
        migrations.AlterModelOptions(
            name='acudiente',
            options={'verbose_name': 'Acudiente'},
        ),
        migrations.AlterModelOptions(
            name='administrativos',
            options={'verbose_name': 'Administrativos'},
        ),
        migrations.AlterModelOptions(
            name='citaciones',
            options={'verbose_name': 'Citaciones'},
        ),
        migrations.AlterModelOptions(
            name='estudiante',
            options={'verbose_name': 'Estudiante'},
        ),
        migrations.AlterModelOptions(
            name='faltas',
            options={'verbose_name': 'Faltas'},
        ),
        migrations.AlterModelOptions(
            name='grado',
            options={'verbose_name': 'Grado'},
        ),
        migrations.AlterModelOptions(
            name='observacion',
            options={'verbose_name': 'Observacion'},
        ),
        migrations.AddField(
            model_name='acudiente',
            name='documento',
            field=models.CharField(default=0, max_length=10),
        ),
        migrations.AddField(
            model_name='acudiente',
            name='tipoDocumento',
            field=models.CharField(choices=[('T.I.', 'Tarjeta de Identidad'), ('C.C.', 'Cedula de Ciudadanía'), ('C.E.', 'Cedula de Extranjería')], default='C.C.', max_length=4),
        ),
        migrations.AlterField(
            model_name='acudiente',
            name='telefono',
            field=models.CharField(max_length=13),
        ),
    ]
