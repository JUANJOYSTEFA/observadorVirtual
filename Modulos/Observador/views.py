from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.db.models import Q
from django.contrib import messages
from .models import * 
from .forms import *
import logging
logger = logging.getLogger(__name__)  # Define un logger


def redirigirHome(request):
    return redirect('listaColegio')
class IndexView(TemplateView):
    template_name = 'index.html'

class LoginFormView(LoginView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)


def listaColegio(request):
    query = request.GET.get('buscar', '')
    logger.info(f"🔍 Búsqueda recibida: {query}")  # Esto se verá en la consola

    colegios = Colegio.objects.all()
    if query:
        colegios = colegios.filter(
            Q(nombre__icontains=query) |
            Q(direccion__icontains=query) |
            Q(telefono__icontains=query) |
            Q(email__icontains=query)
        )

    # Muestra el QuerySet filtrado
    logger.info(f"📄 Registros encontrados: {colegios}")
    return render(request, 'listaColegios.html', {'colegio': colegios, 'query': query})


def agregarColegio(request):
	data={
		'form': ColegioForm()
	}

	if request.method =='POST':
		formulario = ColegioForm(data=request.POST, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			messages.success(request, "Guardado Correctamente")
			return redirect('listaColegio')
		else:
			data["form"]=formulario
			messages.warning(request, "El archivo ya existe")
			#data["mensaje"]="el archivo ya existe"
	return render(request, 'agregarColegio.html', data)

def modificarColegio(request, idColegio):
    colegio = get_object_or_404(Colegio, idColegio=idColegio)  # Busca un elemento por su ID

    data = {
        'form': ColegioForm(instance=colegio)
    }

    if request.method == 'POST':
        formulario = ColegioForm(data=request.POST, instance=colegio, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado Correctamente")
            return redirect('listaColegio')  

        data["form"] = formulario 
    return render(request, 'modificar.html', data)

def eliminarColegio(request, idColegio):
    colegio = get_object_or_404(Colegio, idColegio=idColegio)
    colegio.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="listaColegio")

def listaGrado(request):
    grados = Grado.objects.all()  # Obtiene todos los registros
    return render(request, 'listaGrados.html', {'grado': grados})


def agregarGrado(request):
	data = {
		'form': GradoForm()
	}

	if request.method == 'POST':
		formulario = GradoForm(data=request.POST, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			messages.success(request, "Guardado Correctamente")
			return redirect('listaGrado')
		else:
			data["form"] = formulario
			messages.warning(request, "El archivo ya existe")
			# data["mensaje"]="el archivo ya existe"
	return render(request, 'agregarGrado.html', data)


def modificarGrado(request, idGrado):
    # Busca un elemento por su ID
    grado = get_object_or_404(Grado, idGrado=idGrado)

    data = {
        'form': GradoForm(instance=grado)
    }

    if request.method == 'POST':
        formulario = GradoForm(
            data=request.POST, instance=grado, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado Correctamente")
            return redirect('listaGrado')

        data["form"] = formulario
    return render(request, 'modificar.html', data)


def eliminarGrado(request, idGrado):
	grado = get_object_or_404(Grado, idGrado=idGrado)
	grado.delete()
	messages.success(request, "Eliminado Correctamente")
	return redirect(to="listaGrado")


def listaEstudiante(request):
    estudiante = Estudiante.objects.all()  # Obtiene todos los registros
    return render(request, 'listaEstudiante.html', {'estudiante': estudiante})


def agregarEstudiante(request):
	data = {
		'form': EstudianteForm()
	}

	if request.method == 'POST':
		formulario = EstudianteForm(data=request.POST, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			messages.success(request, "Guardado Correctamente")
			return redirect('listaEstudiante')
		else:
			data["form"] = formulario
			messages.warning(request, "El archivo ya existe")
			# data["mensaje"]="el archivo ya existe"
	return render(request, 'agregarEstudiante.html', data)


def modificarAcudiente(request, idEstudiante):
    # Busca un elemento por su ID
    acudiente = get_object_or_404(Estudiante, idGrado=idAcudiente)

    data = {
        'form': AcudienteForm(instance=acudiente)
    }

    if request.method == 'POST':
        formulario = AcudienteForm(
            data=request.POST, instance=acudiente, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado Correctamente")
            return redirect('listaGrado')

        data["form"] = formulario
    return render(request, 'modificar.html', data)


def eliminarAcudiente(request, idAcudiente):
	acudiente = get_object_or_404(Acudiente, idGrado=idAcudiente)
	acudiente.delete()
	messages.success(request, "Eliminado Correctamente")
	return redirect(to="listaAcudiente")

def index(request):
    return render(request, 'index.html')


def listaAcudiente(request):
    acudiente = Acudiente.objects.all()  # Obtiene todos los registros
    return render(request, 'listaAcudiente.html', {'acudiente': acudiente})


def agregarAcudiente(request):
	data = {
		'form': AcudienteForm()
	}

	if request.method == 'POST':
		formulario = AcudienteForm(data=request.POST, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			messages.success(request, "Guardado Correctamente")
			return redirect('listaAcudiente')
		else:
			data["form"] = formulario
			messages.warning(request, "El archivo ya existe")
			# data["mensaje"]="el archivo ya existe"
	return render(request, 'agregarAcudiente.html', data)


def modificarAcudiente(request, idAcudiente):
    # Busca un elemento por su ID
    acudiente = get_object_or_404(Acudiente, idGrado=idAcudiente)

    data = {
        'form': AcudienteForm(instance=acudiente)
    }

    if request.method == 'POST':
        formulario = AcudienteForm(
            data=request.POST, instance=acudiente, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado Correctamente")
            return redirect('listaGrado')

        data["form"] = formulario
    return render(request, 'modificar.html', data)


def eliminarAcudiente(request, idAcudiente):
	acudiente = get_object_or_404(Acudiente, idGrado=idAcudiente)
	acudiente.delete()
	messages.success(request, "Eliminado Correctamente")
	return redirect(to="listaAcudiente")

def index(request):
    return render(request, 'index.html')
