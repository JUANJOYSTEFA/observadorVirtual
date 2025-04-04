from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from Modulos.Observador.models import *
# Create your views here.
def observadorEstudianteLibro(request, idEstudiante):
    estudiante = get_object_or_404(Estudiante, idEstudiante=idEstudiante)
    acudiente = get_object_or_404(Acudiente, idEstudiante=idEstudiante)
    observacion = get_object_or_404(Observacion, idEstudiante=idEstudiante)
    return render(request, 'observador/libro.html', {"estudiante":estudiante, "acudiente":acudiente, "observacion":observacion})
