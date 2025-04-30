from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from Modulos.Observador.models import *
# Create your views here.
def observadorEstudianteLibro(request, idEstudiante):
    estudiante = get_object_or_404(Estudiante, idEstudiante=idEstudiante)

    # Obtener el acudiente si existe
    acudiente = Acudiente.objects.filter(idEstudiante=idEstudiante).first()

    # Obtener todas las observaciones del estudiante
    observacion = Observacion.objects.filter(idEstudiante=idEstudiante)

    return render(request, 'observador/libro.html', {
        "estudiante": estudiante,
        "acudiente": acudiente,
        "observacion": observacion
    })

def login(request):
    return render(request, "iniciosesion.html")
