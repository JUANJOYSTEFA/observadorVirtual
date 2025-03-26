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
    return render(request, 'listas/colegios.html', {'colegio': colegios, 'query': query})


def agregarColegio(request):
    data = {
        'form': ColegioForm()
    }

    if request.method == 'POST':
        formulario = ColegioForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Guardado Correctamente")
            return redirect('listaColegio')
        else:
            data["form"] = formulario
            messages.warning(request, "El archivo ya existe")
            # data["mensaje"]="el archivo ya existe"
    return render(request, 'agregar/colegio.html', data)


def modificarColegio(request, idColegio):
    # Busca un elemento por su ID
    colegio = get_object_or_404(Colegio, idColegio=idColegio)

    data = {
        'form': ColegioForm(instance=colegio),
        'cancel_url': 'listaColegio',
        'tabla': 'Colegio'
    }

    if request.method == 'POST':
        formulario = ColegioForm(
            data=request.POST, instance=colegio, files=request.FILES)
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
    return render(request, 'listas/grados.html', {'grado': grados})


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
    return render(request, 'agregar/grado.html', data)


def modificarGrado(request, idGrado):
    # Busca un elemento por su ID
    grado = get_object_or_404(Grado, idGrado=idGrado)

    data = {
        'form': GradoForm(instance=grado),
        'cancel_url': 'listaGrado',
        'tabla': 'Grado'
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
    return render(request, 'listas/estudiantes.html', {'estudiante': estudiante})


def agregarEstudiante(request):
    data = {
        'form': EstudianteForm(),
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
    return render(request, 'agregar/estudiante.html', data)


def modificarEstudiante(request, idEstudiante):
    # Busca un elemento por su ID
    estudiante = get_object_or_404(Estudiante, idEstudiante=idEstudiante)

    data = {
        'form': EstudianteForm(instance=estudiante),
        'cancel_url': 'listaEstudiante',
        'tabla': 'Estudiante'
    }

    if request.method == 'POST':
        formulario = EstudianteForm(
            data=request.POST, instance=estudiante, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado Correctamente")
            return redirect('listaEstudiante')

        data["form"] = formulario
    return render(request, 'modificar.html', data)


def eliminarEstudiante(request, idEstudiante):
    estudiante = get_object_or_404(Estudiante, idEstudiante=idEstudiante)
    estudiante.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="listaEstudiante")


def listaAcudiente(request):
    acudiente = Acudiente.objects.all()  # Obtiene todos los registros
    return render(request, 'listas/acudientes.html', {'acudiente': acudiente})


def agregarAcudiente(request):
    data = {
        'form': AcudienteForm(),
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
    return render(request, 'agregar/acudiente.html', data)


def modificarAcudiente(request, idAcudiente):
    # Busca un elemento por su ID
    acudiente = get_object_or_404(Acudiente, idAcudiente=idAcudiente)

    data = {
        'form': AcudienteForm(instance=acudiente),
        'cancel_url': 'listaAcudiente',
        'tabla': 'Acudiente'
    }

    if request.method == 'POST':
        formulario = AcudienteForm(
            data=request.POST, instance=acudiente, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado Correctamente")
            return redirect('listaAcudiente')

        data["form"] = formulario
    return render(request, 'modificar.html', data)


def eliminarAcudiente(request, idAcudiente):
    acudiente = get_object_or_404(Acudiente, idGrado=idAcudiente)
    acudiente.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="listaAcudiente")


def listaAdministrativo(request):
    administrativos = Administrativos.objects.all()  # Obtiene todos los registros
    return render(request, 'listas/administrativos.html', {'administrativo': administrativos})


def agregarAdministrativo(request):
    data = {
        'form': AdministrativosForm()
    }

    if request.method == 'POST':
        formulario = AdministrativosForm(
            data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Guardado Correctamente")
            return redirect('listaAdministrativo')
        else:
            data["form"] = formulario
            messages.warning(request, "El archivo ya existe")
            # data["mensaje"]="el archivo ya existe"
    return render(request, 'agregar/administrativos.html', data)


def modificarAdministrativo(request, idAdministrativo):
    # Busca un elemento por su ID
    administrativos = get_object_or_404(
        Administrativos, idAdministrativo=idAdministrativo)

    data = {
        'form': AdministrativosForm(instance=administrativos),
        'cancel_url': 'listaAdministrativo',
        'tabla': 'Administrativo'
    }

    if request.method == 'POST':
        formulario = AdministrativosForm(
            data=request.POST, instance=administrativos, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado Correctamente")
            return redirect('listaAdministrativo')

        data["form"] = formulario
    return render(request, 'modificar.html', data)


def eliminarAdministrativo(request, idAdministrativo):
    administrativos = get_object_or_404(
        Administrativos, idAdministrativo=idAdministrativo)
    administrativos.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="listaAdministrativo")


def listaFalta(request):
    faltas = Faltas.objects.all()  # Obtiene todos los registros
    return render(request, 'listas/faltas.html', {'falta': faltas})


def agregarFalta(request):
    data = {
        'form': FaltasForm()
    }

    if request.method == 'POST':
        formulario = FaltasForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Guardado Correctamente")
            return redirect('listaFalta')
        else:
            data["form"] = formulario
            messages.warning(request, "El archivo ya existe")
            # data["mensaje"]="el archivo ya existe"
    return render(request, 'agregar/falta.html', data)


def modificarFalta(request, idFalta):
    # Busca un elemento por su ID
    faltas = get_object_or_404(
        Faltas, idFalta=idFalta)

    data = {
        'form': FaltasForm(instance=faltas),
        'cancel_url': 'listaFalta',
        'tabla': 'Falta'
    }

    if request.method == 'POST':
        formulario = FaltasForm(
            data=request.POST, instance=faltas, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado Correctamente")
            return redirect('listaFalta')

        data["form"] = formulario
    return render(request, 'modificar.html', data)


def eliminarFalta(request, idFalta):
    faltas = get_object_or_404(Faltas, idFalta=idFalta)
    faltas.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="listaFalta")


def listaObservacion(request):
    observaciones = Observacion.objects.all()  # Obtiene todos los registros
    return render(request, 'listas/observaciones.html', {'observacion': observaciones})


def agregarObservacion(request):
    data = {
        'form': ObservacionForm()
    }

    if request.method == 'POST':
        formulario = ObservacionForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Guardado Correctamente")
            return redirect('listaObservacion')
        else:
            data["form"] = formulario
            messages.warning(request, "El archivo ya existe")
            # data["mensaje"]="el archivo ya existe"
    return render(request, 'agregar/observacion.html', data)


def modificarObservacion(request, idObservacion):
    # Busca un elemento por su ID
    observacion = get_object_or_404(
        Observacion, idObservacion=idObservacion)

    data = {
        'form': ObservacionForm(instance=observacion),
        'cancel_url': 'listaObservacion',
        'tabla': 'Observacion'
    }

    if request.method == 'POST':
        formulario = ObservacionForm(
            data=request.POST, instance=observacion, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado Correctamente")
            return redirect('listaObservacion')

        data["form"] = formulario
    return render(request, 'modificar.html', data)


def eliminarObservacion(request, idObservacion):
    observacion = get_object_or_404(Observacion, idObservacion=idObservacion)
    observacion.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="listaObservacion")


def listaCitacion(request):
    citaciones = Citaciones.objects.all()  # Obtiene todos los registros
    return render(request, 'listas/citaciones.html', {'citacion': citaciones})


def agregarCitacion(request):
    data = {
        'form': CitacionesForm()
    }

    if request.method == 'POST':
        formulario = CitacionesForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Guardado Correctamente")
            return redirect('listaCitacion')
        else:
            data["form"] = formulario
            messages.warning(request, "El archivo ya existe")
            # data["mensaje"]="el archivo ya existe"
    return render(request, 'agregar/citacion.html', data)


def modificarCitacion(request, idCitacion):
    # Busca un elemento por su ID
    citaciones = get_object_or_404(
        Citaciones, idCitacion=idCitacion)

    data = {
        'form': CitacionesForm(instance=citaciones),
        'cancel_url': 'listaCitacion',
        'tabla': 'Citacion'
    }

    if request.method == 'POST':
        formulario = CitacionesForm(
            data=request.POST, instance=citaciones, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado Correctamente")
            return redirect('listaCitacion')

        data["form"] = formulario
    return render(request, 'modificar.html', data)


def eliminarCitacion(request, idCitacion):
    citaciones = get_object_or_404(Citaciones, idCitacion=idCitacion)
    citaciones.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="listaCitacion")
