from django.db import models

class Grado(models.Model):
    idGrado = models.AutoField(primary_key=True)
    grado = models.CharField(max_length=10, null=True, blank=True)
    ciclo = models.CharField(max_length=7)

    def __str__(self):
        return f"Ciclo: {self.ciclo}, Grado: {self.grado}"

class Estudiante(models.Model):
    idEstudiante = models.AutoField(primary_key=True)
    tiposDocumentos = [
        ('T.I.', 'Tarjeta de Identidad'),
        ('C.C.', 'Cedula de Ciudadanía'),
        ('C.E.', 'Cedula de Extranjería')
    ]
    tipoDocumento = models.CharField(max_length=4, choices=tiposDocumentos ,default='T.I.')
    documento = models.CharField(max_length=10, default=0)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad = models.IntegerField()
    contrasena = models.CharField(max_length=100)
    faltasTipo1 = models.IntegerField(default=0)
    faltasTipo2 = models.IntegerField(default=0)
    faltasTipo3 = models.IntegerField(default=0)
    idGrado = models.ForeignKey(Grado, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.idEstudiante}, {self.apellido} {self.nombre}, Identificación: {self.tipoDocumento} {self.documento}"




class Acudiente(models.Model):
    idAcudiente = models.AutoField(primary_key=True)
    tiposDocumentos = [
        ('T.I.', 'Tarjeta de Identidad'),
        ('C.C.', 'Cedula de Ciudadanía'),
        ('C.E.', 'Cedula de Extranjería')
    ]
    tipoDocumento = models.CharField(max_length=4, choices=tiposDocumentos ,default='C.C.')
    documento = models.CharField(max_length=10, default=0)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=10)  # Mejor CharField para conservar ceros iniciales
    correo = models.EmailField(max_length=100)  # EmailField valida automáticamente correos
    contrasena = models.CharField(max_length=100)
    idEstudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name="acudientes")

    def __str__(self):
        return f"Estudiante: {self.idEstudiante}, Apellido: {self.apellido}, Nombre: {self.nombre}"

class Administrativos(models.Model):
    idAdministrativo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    ciclo = models.CharField(max_length=12)
    correo = models.EmailField(max_length=100)
    contrasena = models.CharField(max_length=100)

class Faltas(models.Model):
    idFalta = models.AutoField(primary_key=True)
    tipoFalta = models.IntegerField()
    descripcion = models.TextField(max_length=1000)

class Observacion(models.Model):
    idObservacion = models.AutoField(primary_key=True)
    idFalta = models.ForeignKey(Faltas, on_delete=models.CASCADE, related_name="observaciones")
    idEstudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name="observaciones")
    idAdministrativo = models.ForeignKey(Administrativos, on_delete=models.CASCADE, related_name="observaciones")
    idGrado = models.ForeignKey(Grado, on_delete=models.CASCADE, related_name="observaciones")
    fecha = models.DateField()
    hora = models.TimeField()
    comentario = models.TextField(max_length=1000)

class Citaciones(models.Model):
    idCitacion = models.AutoField(primary_key=True)
    fecha = models.DateField()
    hora = models.TimeField()
    idAcudiente = models.ForeignKey(Acudiente, on_delete=models.CASCADE, related_name="citaciones")
    idEstudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name="citaciones")
