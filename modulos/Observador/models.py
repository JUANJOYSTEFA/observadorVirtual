from django.db import models

class Grados(models.Model):
    idGrado = models.AutoField(primary_key=True)
    grado = models.CharField(max_length=3)
    ciclo = models.CharField(max_length=7)

    def __str__(self):
        return "Id: {0}, Grado: {1}, Ciclo: {2}".format(self.idGrado, self.grado, self.ciclo)
    
    class Meta:
        db_table = 'Grados'

class Estudiantes(models.Model):
    idEstudiante = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad = models.IntegerField()
    grado = models.ForeignKey(Grados, on_delete=models.CASCADE, related_name="estudiantes")
    contrasena = models.CharField(max_length=100)
    faltasTipo1 = models.IntegerField(default=0)
    faltasTipo2 = models.IntegerField(default=0)
    faltasTipo3 = models.IntegerField(default=0)

    class Meta:
        db_table = 'Estudiantes'

class Acudientes(models.Model):
    idAcudiente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10)  # Mejor CharField para conservar ceros iniciales
    correo = models.EmailField(max_length=100)  # EmailField valida automáticamente correos
    contrasena = models.CharField(max_length=100)
    idEstudiante = models.ForeignKey(Estudiantes, on_delete=models.CASCADE, related_name="acudientes")

    class Meta:
        db_table = 'Acudientes'

class Administrativos(models.Model):
    idAdministrativo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    ciclo = models.CharField(max_length=12)
    correo = models.EmailField(max_length=100)
    contrasena = models.CharField(max_length=100)

    class Meta:
        db_table = 'Administrativos'

class Faltas(models.Model):
    idFalta = models.AutoField(primary_key=True)
    tipoFalta = models.IntegerField()
    descripcion = models.TextField(max_length=1000)

    class Meta:
        db_table = 'Faltas'

class Observaciones(models.Model):
    idObservacion = models.AutoField(primary_key=True)
    idFalta = models.ForeignKey(Faltas, on_delete=models.CASCADE, related_name="observaciones")
    idEstudiante = models.ForeignKey(Estudiantes, on_delete=models.CASCADE, related_name="observaciones")
    idAdministrativo = models.ForeignKey(Administrativos, on_delete=models.CASCADE, related_name="observaciones")
    idGrado = models.ForeignKey(Grados, on_delete=models.CASCADE, related_name="observaciones")
    fecha = models.DateField()
    hora = models.TimeField()
    comentario = models.TextField(max_length=1000)

    class Meta:
        db_table = 'Observaciones'

class Citaciones(models.Model):
    idCitacion = models.AutoField(primary_key=True)
    fecha = models.DateField()
    hora = models.TimeField()
    idAcudiente = models.ForeignKey(Acudientes, on_delete=models.CASCADE, related_name="citaciones")
    idEstudiante = models.ForeignKey(Estudiantes, on_delete=models.CASCADE, related_name="citaciones")

    class Meta:
        db_table = 'Citaciones'
