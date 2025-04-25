import os
from .models import Observacion, Estudiante
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.db.models import Q
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import default_storage
from .models import *
from .forms import *
import logging
import time
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

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
    query = request.GET.get("buscar", "")  # Obtener el valor del input
    colegios = Colegio.objects.all()

    if query:
        colegios = colegios.filter(
            Q(nombre__icontains=query) |
            Q(direccion__icontains=query) |
            Q(telefono__icontains=query) |
            Q(email__icontains=query)
        )

    return render(request, "listas/colegios.html", {"colegio": colegios, "query": query})


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
    query = request.GET.get("buscar", "")  # Obtener el valor del input
    grados = Grado.objects.all()

    if query:
        grados = grados.filter(
            Q(grado__icontains=query) |
            Q(ciclo__icontains=query) |
            Q(idColegio__nombre__icontains=query)
        )

    return render(request, 'listas/grados.html', {'grado': grados, "query": query})


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
    query = request.GET.get("buscar", "")  # Obtener el valor del input
    estudiante = Estudiante.objects.all()

    if query:
        estudiante = estudiante.filter(
            Q(tipoDocumento__icontains=query) |
            Q(documento__icontains=query) |
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(edad__icontains=query) |
            Q(correo__icontains=query) |
            Q(faltasTipo1__icontains=query) |
            Q(faltasTipo2__icontains=query) |
            Q(faltasTipo3__icontains=query) |
            Q(idColegio__nombre__icontains=query) |
            Q(idGrado__grado__icontains=query) |
            Q(idGrado__ciclo__icontains=query)
        )

    return render(request, 'listas/estudiantes.html', {'estudiante': estudiante, "query": query})


def agregarEstudiante(request):
    data = {
        'form': EstudianteForm(),
    }

    if request.method == 'POST':
        formulario = EstudianteForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            estudiante = formulario.save(commit=False)
            
            # Verificar si se subió una imagen
            if 'imagen' in request.FILES:
                imagen = request.FILES['imagen']
                
                # Procesar la imagen para hacerla cuadrada
                img = Image.open(imagen)
                
                # Determinar el tamaño del cuadrado
                ancho, alto = img.size
                tamaño = min(ancho, alto)
                
                # Calcular coordenadas para recorte centrado
                left = (ancho - tamaño) / 2
                top = (alto - tamaño) / 2
                right = (ancho + tamaño) / 2
                bottom = (alto + tamaño) / 2
                
                # Recortar la imagen
                img_recortada = img.crop((left, top, right, bottom))
                
                # Redimensionar a un tamaño estándar si lo deseas (opcional)
                tamaño_final = 300  # Pixels
                img_recortada = img_recortada.resize((tamaño_final, tamaño_final), Image.Resampling.LANCZOS)
                
                # Guardar en memoria
                output = BytesIO()
                
                # Determinar el formato de salida
                if img.format == 'JPEG' or img.format == 'JPG':
                    img_recortada.save(output, format='JPEG', quality=85)
                    extension = 'jpg'
                else:
                    img_recortada.save(output, format='PNG')
                    extension = 'png'
                    
                output.seek(0)
                
                # Crear un nuevo archivo para Django
                nueva_imagen = InMemoryUploadedFile(
                    output,
                    'ImageField',
                    f"{imagen.name.split('.')[0]}_cuadrado.{extension}",
                    'image/jpeg' if extension == 'jpg' else 'image/png',
                    sys.getsizeof(output),
                    None
                )
                
                # Asignar la nueva imagen al estudiante
                estudiante.imagen_perfil = nueva_imagen
            
            estudiante.save()
            messages.success(request, "Guardado Correctamente")
            return redirect('listaEstudiante')
        else:
            data["form"] = formulario
            messages.warning(request, "Hubo un error")
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
            estudiante = formulario.save(commit=False)
            
            # Verificar si se subió una nueva imagen
            if 'imagen' in request.FILES:
                imagen = request.FILES['imagen']
                
                # Procesar la imagen para hacerla cuadrada
                img = Image.open(imagen)
                
                # Determinar el tamaño del cuadrado
                ancho, alto = img.size
                tamaño = min(ancho, alto)
                
                # Calcular coordenadas para recorte centrado
                left = (ancho - tamaño) / 2
                top = (alto - tamaño) / 2
                right = (ancho + tamaño) / 2
                bottom = (alto + tamaño) / 2
                
                # Recortar la imagen
                img_recortada = img.crop((left, top, right, bottom))
                
                # Redimensionar a un tamaño estándar
                tamaño_final = 300  # Pixels
                img_recortada = img_recortada.resize((tamaño_final, tamaño_final), Image.Resampling.LANCZOS)
                
                # Guardar en memoria
                output = BytesIO()
                
                # Determinar el formato de salida
                if img.format == 'JPEG' or img.format == 'JPG':
                    img_recortada.save(output, format='JPEG', quality=85)
                    extension = 'jpg'
                else:
                    img_recortada.save(output, format='PNG')
                    extension = 'png'
                    
                output.seek(0)
                
                # Crear un nuevo archivo para Django
                nueva_imagen = InMemoryUploadedFile(
                    output,
                    'ImageField',
                    f"{imagen.name.split('.')[0]}_cuadrado.{extension}",
                    'image/jpeg' if extension == 'jpg' else 'image/png',
                    sys.getsizeof(output),
                    None
                )
                
                # Si había una imagen anterior, eliminarla
                if estudiante.imagen_perfil:
                    try:
                        # Guardar la ruta del archivo anterior
                        old_image_path = estudiante.imagen_perfil.path
                        
                        # Asignar la nueva imagen
                        estudiante.imagen_perfil = nueva_imagen
                        
                        # Si la asignación fue exitosa, eliminar el archivo antiguo
                        import os
                        if os.path.isfile(old_image_path):
                            os.remove(old_image_path)
                    except:
                        # Si hay algún error, simplemente asignar la nueva imagen sin eliminar la antigua
                        estudiante.imagen_perfil = nueva_imagen
                else:
                    # Si no había imagen anterior, simplemente asignar la nueva
                    estudiante.imagen_perfil = nueva_imagen
            
            estudiante.save()
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
    query = request.GET.get("buscar", "")  # Obtener el valor del input
    acudiente= Acudiente.objects.all() #Obtiene todos los registros

    if query:
        acudiente = acudiente.filter( #Filtra por cada campo
            Q(tipoDocumento__icontains=query) |
            Q(documento__icontains=query) |
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(telefono__icontains=query) |
            Q(correo__icontains=query) |
            Q(idEstudiante__nombre__icontains=query) |
            Q(idEstudiante__apellido__icontains=query) |
            Q(idEstudiante__correo__icontains=query)
        )

    return render(request, 'listas/acudientes.html', {'acudiente': acudiente, "query": query})


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
    query = request.GET.get("buscar", "")  # Obtener el valor del input
    administrativos = Administrativos.objects.all()  # Obtiene todos los registros

    if query:
        administrativos = administrativos.filter(  # Filtra por cada campo
            Q(nombre__icontains=query) |
            Q(apellido__icontains=query) |
            Q(cargo__icontains=query) |
            Q(ciclo__icontains=query) |
            Q(correo__icontains=query) |
            Q(idColegio__nombre__icontains=query)
        )

    return render(request, 'listas/administrativos.html', {'administrativo': administrativos, "query": query})

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
    query = request.GET.get("buscar", "")  # Obtener el valor del input
    faltas = Faltas.objects.all()  # Obtiene todos los registros

    if query:
        faltas = faltas.filter(  # Filtra por cada campo
            Q(tipoFalta__icontains=query) |
            Q(falta__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(idColegio__nombre__icontains=query)
        )

    return render(request, 'listas/faltas.html', {'falta': faltas, "query": query})


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
    query = request.GET.get("buscar", "")  # Obtener el valor del input
    observaciones = Observacion.objects.all()  # Obtiene todos los registro

    if query:
        observaciones = observaciones.filter(  # Filtra por cada campo
            Q(fecha__icontains=query) |
            Q(hora__icontains=query) |
            Q(comentario__icontains=query) |
            Q(idFalta__tipoFalta__icontains=query) |
            Q(idFalta__falta__icontains=query) |
            Q(idFalta__descripcion__icontains=query) |
            Q(idEstudiante__nombre__icontains = query) |
            Q(idEstudiante__apellido__icontains = query) |
            Q(idEstudiante__correo__icontains=query) |
            Q(idAdministrativo__nombre__icontains=query) |
            Q(idAdministrativo__apellido__icontains=query)
        )

    return render(request, 'listas/observaciones.html', {'observacion': observaciones, "query": query})



def agregarObservacion(request):
    data = {
        'form': ObservacionForm()
    }

    if request.method == 'POST':
        formulario = ObservacionForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            observacion = formulario.save()  # Guardar la observación y obtener el objeto

            estudiante = observacion.idEstudiante  # Obtener el estudiante
            tipo_falta = observacion.idFalta.tipoFalta  # Obtener el tipo de falta

            # Incrementar el campo correspondiente en el estudiante
            if tipo_falta == 1:
                estudiante.faltasTipo1 += 1
            elif tipo_falta == 2:
                estudiante.faltasTipo2 += 1
            elif tipo_falta == 3:
                estudiante.faltasTipo3 += 1

            estudiante.save()  # Guardar los cambios en el estudiante

            messages.success(
                request, "Guardado Correctamente y falta registrada")
            return redirect('listaObservacion')
        else:
            data["form"] = formulario
            messages.warning(request, "El archivo ya existe")

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

    estudiante = observacion.idEstudiante  # Obtener el estudiante relacionado
    tipo_falta = observacion.idFalta.tipoFalta  # Obtener el tipo de falta

    # Restar la falta correspondiente, asegurando que no sea menor que 0
    if tipo_falta == 1 and estudiante.faltasTipo1 > 0:
        estudiante.faltasTipo1 -= 1
    elif tipo_falta == 2 and estudiante.faltasTipo2 > 0:
        estudiante.faltasTipo2 -= 1
    elif tipo_falta == 3 and estudiante.faltasTipo3 > 0:
        estudiante.faltasTipo3 -= 1

    estudiante.save()  # Guardar los cambios en el estudiante

    observacion.delete()  # Eliminar la observación
    messages.success(
        request, "Observación eliminada y falta descontada correctamente")

    return redirect(to="listaObservacion")



def listaCitacion(request):
    query = request.GET.get("buscar", "")  # Obtener el valor del input
    citaciones = Citaciones.objects.all()  # Obtiene todos los registro

    if query:
        citaciones = citaciones.filter(  # Filtra por cada campo
            Q(fecha__icontains=query) |
            Q(hora__icontains=query) |
            Q(asistencia__icontains=query) |
            Q(idEstudiante__nombre__icontains = query) |
            Q(idEstudiante__apellido__icontains = query) |
            Q(idEstudiante__correo__icontains=query) |
            Q(idEstudiante__correo__icontains=query) |
            Q(idAcudiente__nombre__icontains=query) |
            Q(idAcudiente__apellido__icontains=query) |
            Q(idAcudiente__correo__icontains=query)
        )

    return render(request, 'listas/citaciones.html', {'citacion': citaciones, "query": query})


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

def observadorEstudianteLibro(request, idEstudiante):
    estudiante = get_object_or_404(Estudiante, idEstudiante=idEstudiante)
    acudiente = get_object_or_404(Acudiente, idEstudiante=idEstudiante)
    observacion = get_object_or_404(Observacion, idEstudiante=idEstudiante)
    return render(request, 'observador/libro.html', {"estudiante":estudiante, "acudiente":acudiente, "observacion":observacion})
