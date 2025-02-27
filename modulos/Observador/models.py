from django.db import models

class Colegio(models.Model):
    idColegio = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=13)
    email = models.EmailField(max_length=100)

    def __str__(self):
        return f"idColegio: {self.idColegio}, Nombre: {self.nombre}"

    class Meta:
        verbose_name = 'Colegio'
    


class Grado(models.Model):
    idGrado = models.AutoField(primary_key=True)
    grado = models.CharField(max_length=16, null=True, blank=True)
    ciclo = models.CharField(max_length=7)
    idColegio = models.ForeignKey(Colegio, on_delete=models.CASCADE, related_name="grado", default= 1)

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
    idColegio = models.ForeignKey(Colegio, on_delete=models.CASCADE, related_name="estudiantes", default= 1)
    idGrado = models.ForeignKey(Grado, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.idEstudiante}, {self.apellido} {self.nombre}, Identificación: {self.tipoDocumento} {self.documento}"

    class Meta:
        verbose_name = 'Estudiante'


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
    telefono = models.CharField(max_length=13)  # Mejor CharField para conservar ceros iniciales
    correo = models.EmailField(max_length=100)  # EmailField valida automáticamente correos
    contrasena = models.CharField(max_length=100)
    idEstudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name="acudientes")

    def __str__(self):
        return f"Estudiante: {self.idEstudiante}, Nombre: {self.apellido} {self.nombre}"

    class Meta:
        verbose_name = 'Acudiente'

class Administrativos(models.Model):
    idAdministrativo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)

    cargos = [  # Lista de tuplas para choices
        ('profesor', 'Profesor'),
        ('directivo', 'Directivo'),
    ]
    
    cargo = models.CharField(max_length=9, choices=cargos, default='profesor')
    ciclo = models.CharField(max_length=12, null=True, blank=True)
    correo = models.EmailField(max_length=100)
    contrasena = models.CharField(max_length=100)

    def __str__(self):
        if self.cargo == 'profesor' and self.ciclo:
            return f"idAdministrativo: {self.idAdministrativo}, Nombre: {self.nombre} {self.apellido}, Cargo: {self.cargo}, Ciclo: {self.ciclo}"
        return f"idAdministrativo: {self.idAdministrativo}, Nombre: {self.nombre} {self.apellido}, Cargo: {self.cargo}"


    class Meta:
        verbose_name = 'Administrativos'

class Faltas(models.Model):
    idFalta = models.AutoField(primary_key=True)
    tiposFaltas = [
        (1, "Tipo 1"),
        (2, "Tipo 2"),
        (3, "Tipo 3")
    ]
    tipoFalta = models.IntegerField(choices=tiposFaltas, default= 1)
    falta = models.CharField(max_length=10, null=True, blank=True)
    descripcion = models.TextField(max_length=1000)
    idColegio = models.ForeignKey(Colegio, on_delete=models.CASCADE, related_name="faltas", default= 1)

    def __str__(self):
        return f"Falta: {self.falta}: {self.descripcion}, Falta de tipo: {self.tipoFalta}"

    class Meta:
        verbose_name = 'Faltas'

class Observacion(models.Model):
    idObservacion = models.AutoField(primary_key=True)
    idFalta = models.ForeignKey(Faltas, on_delete=models.CASCADE, related_name="observaciones")
    idEstudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name="observaciones")
    idAdministrativo = models.ForeignKey(Administrativos, on_delete=models.CASCADE, related_name="observaciones")
    idGrado = models.ForeignKey(Grado, on_delete=models.CASCADE, related_name="observaciones")
    fecha = models.DateField()
    hora = models.TimeField()
    comentario = models.TextField(max_length=1000)

    def __str__(self):
        return f"Estudiante: {self.idEstudiante}, Falta: {self.idFalta}, Fecha: {self.fecha}, Administrativo: {self.idAdministrativo}"
    
    class Meta:
        verbose_name = 'Observacion'

class Citaciones(models.Model):
    idCitacion = models.AutoField(primary_key=True)
    fecha = models.DateField()
    hora = models.TimeField()
    idAcudiente = models.ForeignKey(Acudiente, on_delete=models.CASCADE, related_name="citaciones")
    idEstudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name="citaciones")

    def __str__(self):
        return f"Fecha: {self.fecha} {self.hora}, Estudiante: {self.idEstudiante}, Acudiente: {self.idAcudiente}"

    class Meta:
        verbose_name = 'Citaciones'
