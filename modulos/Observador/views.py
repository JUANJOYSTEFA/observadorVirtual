from django.shortcuts import render
from .models import *  # Importa el modelo

def listaColegios(request):
    colegios = Colegio.objects.all()  # Obtiene todos los registros
    return render(request, 'listaColegios.html', {'colegios': colegios})
