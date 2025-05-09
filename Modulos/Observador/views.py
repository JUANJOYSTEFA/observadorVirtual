import os
import base64
from .models import Observacion, Estudiante
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.db.models import Q
from django.contrib import messages
from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib.auth.hashers import make_password, is_password_usable
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
from googleapiclient.discovery import build
import google.auth
from datetime import datetime
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
    if not request.session.get('isLogged', False):
        return redirect('login')
    if request.session.get('userType', False) != "directivo":
        return redirect('home')
    query = request.GET.get("buscar", "")  # Obtener el valor del input
    colegios = Colegio.objects.all()

    if query:
        colegios = colegios.filter(
            Q(nombre__icontains=query) |
            Q(direccion__icontains=query) |
            Q(telefono__icontains=query) |
            Q(email__icontains=query)
        )

    return render(request, "listas/colegios.html", {"colegio": colegios, "query": query, "userType": request.session.get('userType')})


def agregarColegio(request):
    if not request.session.get('isLogged', False):
        return redirect('login')
    if request.session.get('userType', False) != "directivo":
        return redirect('home')
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
    if not request.session.get('isLogged', False):
        return redirect('login')
    if request.session.get('userType', False) != "directivo":
        return redirect('home')
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
    if not request.session.get('isLogged', False):
        return redirect('login')
    if request.session.get('userType', False) != "directivo":
        return redirect('home')
    colegio = get_object_or_404(Colegio, idColegio=idColegio)
    colegio.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="listaColegio")


def listaGrado(request):
    if not request.session.get('isLogged', False):
        return redirect('login')
    if request.session.get('userType', False) != "directivo":
        return redirect('home')
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
    if not request.session.get('isLogged', False):
        return redirect('login')
    if request.session.get('userType', False) != "directivo":
        return redirect('home')
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
    if not request.session.get('isLogged', False):
        return redirect('login')
    if request.session.get('userType', False) != "directivo":
        return redirect('home')
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
    if not request.session.get('isLogged', False):
        return redirect('login')
    if request.session.get('userType', False) != "directivo":
        return redirect('home')
    grado = get_object_or_404(Grado, idGrado=idGrado)
    grado.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="listaGrado")


def listaEstudiante(request):
    if not request.session.get('isLogged', False):
        return redirect('login')
    if request.session.get('userType', False) != "directivo":
        return redirect('home')
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
    if not request.session.get('isLogged', False):
        return redirect('login')
    if request.session.get('userType', False) != "directivo":
        return redirect('home')
    data = {
        'form': EstudianteForm(),
    }

    if request.method == 'POST':
        formulario = EstudianteForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            estudiante = formulario.save(commit=False)

            # Hashear la contraseña antes de guardar
            if hasattr(estudiante, 'contrasena') and estudiante.contrasena:
                estudiante.contrasena = make_password(estudiante.contrasena)

            imagen = request.FILES.get('imagen')
            if imagen:
                # Crea un nombre de archivo único usando el ID y timestamp
                nombre_base, extension = os.path.splitext(imagen.name)
                nombre_seguro = f"{nombre_base}_{int(time.time())}{extension}"

                # Usa la carpeta media en lugar de static
                ruta_relativa = os.path.join(
                    'img', 'estudiantes', nombre_seguro)
                ruta_absoluta = os.path.join(
                    settings.MEDIA_ROOT, 'img', 'estudiantes')

                # Asegúrate de que la carpeta existe
                os.makedirs(ruta_absoluta, exist_ok=True)
                ruta_completa = os.path.join(ruta_absoluta, nombre_seguro)

                # Guarda la imagen
                with open(ruta_completa, 'wb+') as destino:
                    for chunk in imagen.chunks():
                        destino.write(chunk)

                # Guarda la ruta relativa en el campo
                estudiante.urlImagenPerfil = os.path.join(
                    'media', ruta_relativa).replace('\\', '/')

            estudiante.save()
            messages.success(request, "Guardado Correctamente")
            return redirect('listaEstudiante')
        else:
            data["form"] = formulario
            messages.warning(request, "Hubo un error")
    return render(request, 'agregar/estudiante.html', data)


def modificarEstudiante(request, idEstudiante):
    if not request.session.get('isLogged', False):
        return redirect('login')
    if request.session.get('userType', False) != "directivo":
        return redirect('home')
    # Busca un elemento por su ID
    estudiante = get_object_or_404(Estudiante, idEstudiante=idEstudiante)
    contrasena_original = estudiante.contrasena if hasattr(
        estudiante, 'contrasena') else None

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

            # Verificar si la contraseña ha cambiado
            if hasattr(estudiante, 'contrasena') and estudiante.contrasena:

                # Si la contraseña es nueva o ha cambiado, aplicar hash
                if not contrasena_original or estudiante.contrasena != contrasena_original:
                    # Si la contraseña actual no parece un hash, aplicar hash
                    if not is_password_usable(estudiante.contrasena):
                        estudiante.contrasena = make_password(
                            estudiante.contrasena)

            imagen = request.FILES.get('imagen')
            if imagen:
                # Código para manejar la imagen (sin cambios)...
                imagen_antigua = estudiante.urlImagenPerfil
                ruta_antigua = None
                if imagen_antigua:
                    ruta_antigua = os.path.join(
                        settings.MEDIA_ROOT, imagen_antigua.replace('media/', '', 1))

                nombre_base, extension = os.path.splitext(imagen.name)
                nombre_seguro = f"{nombre_base}_{int(time.time())}{extension}"

                ruta_relativa = os.path.join(
                    'img', 'estudiantes', nombre_seguro)
                ruta_absoluta = os.path.join(
                    settings.MEDIA_ROOT, 'img', 'estudiantes')

                os.makedirs(ruta_absoluta, exist_ok=True)
                ruta_completa = os.path.join(ruta_absoluta, nombre_seguro)

                with open(ruta_completa, 'wb+') as destino:
                    for chunk in imagen.chunks():
                        destino.write(chunk)

                estudiante.urlImagenPerfil = os.path.join(
                    'media', ruta_relativa).replace('\\', '/')

                if ruta_antigua and os.path.isfile(ruta_antigua):
                    try:
                        os.remove(ruta_antigua)
                    except (OSError, PermissionError):
                        print(
                            f"No se pudo eliminar la imagen anterior: {ruta_antigua}")

            estudiante.save()
            messages.success(request, "Modificado Correctamente")
            return redirect('listaEstudiante')

        data["form"] = formulario
    return render(request, 'modificar.html', data)


def eliminarEstudiante(request, idEstudiante):
    if not request.session.get('isLogged', False):
        return redirect('login')
    if request.session.get('userType', False) != "directivo":
        return redirect('home')
    estudiante = get_object_or_404(Estudiante, idEstudiante=idEstudiante)
    estudiante.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="listaEstudiante")


def listaAcudiente(request):
    if not request.session.get('isLogged', False):
        return redirect('login')
    if request.session.get('userType', False) != "directivo":
        return redirect('home')
    query = request.GET.get("buscar", "")  # Obtener el valor del input
    acudiente = Acudiente.objects.all()  # Obtiene todos los registros

    if query:
        acudiente = acudiente.filter(  # Filtra por cada campo
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
    if not request.session.get('isLogged', False):
        return redirect('login')
    if request.session.get('userType', False) != "directivo":
        return redirect('home')
    data = {
        'form': AcudienteForm(),
    }

    if request.method == 'POST':
        formulario = AcudienteForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            acudiente = formulario.save(commit=False)

            # Aplicar hash a la contraseña antes de guardar
            if hasattr(acudiente, 'contrasena') and acudiente.contrasena:
                acudiente.contrasena = make_password(acudiente.contrasena)

            acudiente.save()
            messages.success(request, "Guardado Correctamente")
            return redirect('listaAcudiente')
        else:
            data["form"] = formulario
            messages.warning(request, "El archivo ya existe")
            # data["mensaje"]="el archivo ya existe"
    return render(request, 'agregar/acudiente.html', data)


def modificarAcudiente(request, idAcudiente):
    if not request.session.get('isLogged', False):
        return redirect('login')
    if request.session.get('userType', False) != "directivo":
        return redirect('home')
    # Busca un elemento por su ID
    acudiente = get_object_or_404(Acudiente, idAcudiente=idAcudiente)
    contrasena_original = acudiente.contrasena if hasattr(
        acudiente, 'contrasena') else None

    data = {
        'form': AcudienteForm(instance=acudiente),
        'cancel_url': 'listaAcudiente',
        'tabla': 'Acudiente'
    }

    if request.method == 'POST':
        formulario = AcudienteForm(
            data=request.POST, instance=acudiente, files=request.FILES)
        if formulario.is_valid():
            acudiente = formulario.save(commit=False)

            # Verificar si la contraseña ha cambiado
            if hasattr(acudiente, 'contrasena') and acudiente.contrasena:
                # Si la contraseña es nueva o ha cambiado, aplicar hash
                if not contrasena_original or acudiente.contrasena != contrasena_original:
                    # Si la contraseña actual no parece un hash, aplicar hash
                    if not is_password_usable(acudiente.contrasena):
                        acudiente.contrasena = make_password(
                            acudiente.contrasena)

            acudiente.save()
            messages.success(request, "Modificado Correctamente")
            return redirect('listaAcudiente')

        data["form"] = formulario
    return render(request, 'modificar.html', data)


def eliminarAcudiente(request, idAcudiente):
    if not request.session.get('isLogged', False):
        return redirect('login')
    if request.session.get('userType', False) != "directivo":
        return redirect('home')
    acudiente = get_object_or_404(Acudiente, idAcudiente=idAcudiente)
    acudiente.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="listaAcudiente")


def listaAdministrativo(request):
    if not request.session.get('isLogged', False):
        return redirect('login')
    if request.session.get('userType', False) != "directivo":
        return redirect('home')
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
    if not request.session.get('isLogged', False):
        return redirect('login')
    if request.session.get('userType', False) != "directivo":
        return redirect('home')
    data = {
        'form': AdministrativosForm()
    }

    if request.method == 'POST':
        formulario = AdministrativosForm(
            data=request.POST, files=request.FILES)
        if formulario.is_valid():
            administrativo = formulario.save(commit=False)

            # Aplicar hash a la contraseña antes de guardar
            if hasattr(administrativo, 'contrasena') and administrativo.contrasena:
                administrativo.contrasena = make_password(
                    administrativo.contrasena)

            administrativo.save()
            messages.success(request, "Guardado Correctamente")
            return redirect('listaAdministrativo')
        else:
            data["form"] = formulario
            messages.warning(request, "El archivo ya existe")
            # data["mensaje"]="el archivo ya existe"
    return render(request, 'agregar/administrativos.html', data)


def modificarAdministrativo(request, idAdministrativo):
    if not request.session.get('isLogged', False):
        return redirect('login')
    if request.session.get('userType', False) != "directivo":
        return redirect('home')
    # Busca un elemento por su ID
    administrativo = get_object_or_404(
        Administrativos, idAdministrativo=idAdministrativo)
    contrasena_original = administrativo.contrasena if hasattr(
        administrativo, 'contrasena') else None

    data = {
        'form': AdministrativosForm(instance=administrativo),
        'cancel_url': 'listaAdministrativo',
        'tabla': 'Administrativo'
    }

    if request.method == 'POST':
        formulario = AdministrativosForm(
            data=request.POST, instance=administrativo, files=request.FILES)
        if formulario.is_valid():
            administrativo = formulario.save(commit=False)

            # Verificar si la contraseña ha cambiado
            if hasattr(administrativo, 'contrasena') and administrativo.contrasena:
                # Si la contraseña es nueva o ha cambiado, aplicar hash
                if not contrasena_original or administrativo.contrasena != contrasena_original:
                    # Si la contraseña actual no parece un hash, aplicar hash
                    if not is_password_usable(administrativo.contrasena):
                        administrativo.contrasena = make_password(
                            administrativo.contrasena)

            administrativo.save()
            messages.success(request, "Modificado Correctamente")
            return redirect('listaAdministrativo')

        data["form"] = formulario
    return render(request, 'modificar.html', data)


def eliminarAdministrativo(request, idAdministrativo):
    if not request.session.get('isLogged', False):
        return redirect('login')
    if request.session.get('userType', False) != "directivo":
        return redirect('home')
    administrativos = get_object_or_404(
        Administrativos, idAdministrativo=idAdministrativo)
    administrativos.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="listaAdministrativo")


def listaFalta(request):
    if not request.session.get('isLogged', False):
        return redirect('login')
    if request.session.get('userType', False) != "directivo":
        return redirect('home')
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
    if not request.session.get('isLogged', False):
        return redirect('login')
    if request.session.get('userType', False) != "directivo":
        return redirect('home')
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
    if not request.session.get('isLogged', False):
        return redirect('login')
    if request.session.get('userType', False) != "directivo":
        return redirect('home')
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
    if not request.session.get('isLogged', False):
        return redirect('login')
    if request.session.get('userType', False) != "directivo":
        return redirect('home')
    faltas = get_object_or_404(Faltas, idFalta=idFalta)
    faltas.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="listaFalta")


def listaObservacion(request):
    if not request.session.get('isLogged', False):
        return redirect('login')
    if request.session.get('userType', False) != "directivo":
        return redirect('home')
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
            Q(idEstudiante__nombre__icontains=query) |
            Q(idEstudiante__apellido__icontains=query) |
            Q(idEstudiante__correo__icontains=query) |
            Q(idAdministrativo__nombre__icontains=query) |
            Q(idAdministrativo__apellido__icontains=query)
        )

    return render(request, 'listas/observaciones.html', {'observacion': observaciones, "query": query})


def enviar_correos(observacion, estudiante):
    ahora = datetime.now()
    horaActual = ahora.strftime('%d/%m/%Y %H:%M:%S')
    fechaActual = ahora.strftime('%d/%m/%Y')
    acudientes = Acudiente.objects.filter(idEstudiante=estudiante.idEstudiante)
    # Prepare the context for the email template
    context = {
        'horaActual': horaActual,
        'acudiente': acudientes,
        'observacion': observacion,
        'nombre_estudiante': f'{estudiante.nombre} {estudiante.apellido}',
    }
    # Render the HTML template
    html_message = render_to_string('correosTemplate.html', context)
    # This will strip the HTML to create a plain text version
    plain_message = strip_tags(html_message)
    asunto = f'Nueva Observación del Estudiante {context["nombre_estudiante"]}'
    remitente = 'noreplyvirttob@gmail.com'
    # Enviar correo al estudiante
    send_mail(
        asunto,
        plain_message,
        remitente,
        [estudiante.correo],
        html_message=html_message,
        fail_silently=False,
    )
    # Enviar correos a los acudientes
    send_mail(
        asunto,
        plain_message,
        remitente,
        [estudiante.correo],
        html_message=html_message,
        fail_silently=False,
    )
    # Enviar correos a los acudientes
    destinatariosAcudientes = [acudiente.correo for acudiente in acudientes]
    if destinatariosAcudientes:
        send_mail(
            asunto,
            plain_message,
            remitente,
            destinatariosAcudientes,
            html_message=html_message,
            fail_silently=False,
        )


def agregarObservacion(request):
    if not request.session.get('isLogged', False):
        return redirect('login')
    if request.session.get('userType', False) != "directivo":
        return redirect('home')
    data = {
        'form': ObservacionForm()
    }

    if request.method == 'POST':
        formulario = ObservacionForm(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            observacion = formulario.save()
            estudiante = observacion.idEstudiante
            tipo_falta = observacion.idFalta.tipoFalta

            # Incrementar el campo correspondiente en el estudiante
            if tipo_falta == 1:
                estudiante.faltasTipo1 += 1
            elif tipo_falta == 2:
                estudiante.faltasTipo2 += 1
            elif tipo_falta == 3:
                estudiante.faltasTipo3 += 1

            estudiante.totalFaltas += 1
            estudiante.save()  # Guardar los cambios en el estudiante
            enviar_correos(observacion, estudiante)

            messages.success(
                request, "Guardado Correctamente y falta registrada")
            return redirect('listaObservacion')
        else:
            data["form"] = formulario
            messages.warning(request, "El archivo ya existe")

    return render(request, 'agregar/observacion.html', data)


def agregarObservacionProfesor(request, idEstudiante):
    if not request.session.get('isLogged', False):
        return redirect('login')
    if request.session.get('userType', False) != "directivo":
        return redirect('home')

    # Obtener el estudiante
    estudiante = get_object_or_404(Estudiante, idEstudiante=idEstudiante)
    administrativoId = request.session.get('userId')

    data = {
        'form': ObservacionFormProfesor(estudiante_id=idEstudiante, administrativo_id=administrativoId)
    }

    if request.method == 'POST':
        formulario = ObservacionFormProfesor(
            request.POST,
            request.FILES,
            estudiante_id=idEstudiante,
            administrativo_id=administrativoId
        )

        if formulario.is_valid():
            observacion = formulario.save(commit=False)
            estudiante = get_object_or_404(
                Estudiante, idEstudiante=idEstudiante)
            # Usar los valores de los campos ocultos
            estudiante_id = formulario.cleaned_data.get(
                'estudiante_hidden', idEstudiante)
            administrativo_id = formulario.cleaned_data.get(
                'administrativo_hidden', administrativoId)

            # Asignar el estudiante y el administrativo
            observacion.idEstudiante = estudiante
            observacion.idAdministrativo_id = administrativoId

            # Si los campos de fecha y hora no están en el formulario, asignarlos automáticamente
            if not observacion.fecha:
                observacion.fecha = datetime.now().date()
            if not observacion.hora:
                observacion.hora = datetime.now().time()

            # Guardar la observación
            observacion.save()

            tipo_falta = observacion.idFalta.tipoFalta  # Obtener el tipo de falta

            # Incrementar el campo correspondiente en el estudiante
            if tipo_falta == 1:
                estudiante.faltasTipo1 += 1
            elif tipo_falta == 2:
                estudiante.faltasTipo2 += 1
            elif tipo_falta == 3:
                estudiante.faltasTipo3 += 1

            estudiante.totalFaltas += 1

            estudiante.save()  # Guardar los cambios en el estudiante
            enviar_correos(observacion, estudiante)
            messages.success(
                request, "Guardado Correctamente y falta registrada")
            return redirect('listaObservacion')
        else:
            data["form"] = formulario
            messages.warning(
                request, "Por favor corrija los errores en el formulario")

    return render(request, 'agregar/observacion.html', data)


def modificarObservacion(request, idObservacion):
    if not request.session.get('isLogged', False):
        return redirect('login')
    if request.session.get('userType', False) != "directivo":
        return redirect('home')
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
    if not request.session.get('isLogged', False):
        return redirect('login')
    if request.session.get('userType', False) != "directivo":
        return redirect('home')
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

    if estudiante.totalFaltas > 0:
        estudiante.totalFaltas -= 1

    estudiante.save()  # Guardar los cambios en el estudiante

    observacion.delete()  # Eliminar la observación
    messages.success(
        request, "Observación eliminada y falta descontada correctamente")

    return redirect(to="listaObservacion")


def listaCitacion(request):
    if not request.session.get('isLogged', False):
        return redirect('login')
    if request.session.get('userType', False) != "directivo":
        return redirect('home')
    query = request.GET.get("buscar", "")  # Obtener el valor del input
    citaciones = Citaciones.objects.all()  # Obtiene todos los registro

    if query:
        citaciones = citaciones.filter(  # Filtra por cada campo
            Q(fecha__icontains=query) |
            Q(hora__icontains=query) |
            Q(asistencia__icontains=query) |
            Q(idEstudiante__nombre__icontains=query) |
            Q(idEstudiante__apellido__icontains=query) |
            Q(idEstudiante__correo__icontains=query) |
            Q(idEstudiante__correo__icontains=query) |
            Q(idAcudiente__nombre__icontains=query) |
            Q(idAcudiente__apellido__icontains=query) |
            Q(idAcudiente__correo__icontains=query)
        )

    return render(request, 'listas/citaciones.html', {'citacion': citaciones, "query": query})


def agregarCitacion(request):
    if not request.session.get('isLogged', False):
        return redirect('login')
    if request.session.get('userType', False) != "directivo":
        return redirect('home')
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
    if not request.session.get('isLogged', False):
        return redirect('login')
    if request.session.get('userType', False) != "directivo":
        return redirect('home')
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
    if not request.session.get('isLogged', False):
        return redirect('login')
    if request.session.get('userType', False) != "directivo":
        return redirect('home')
    citaciones = get_object_or_404(Citaciones, idCitacion=idCitacion)
    citaciones.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="listaCitacion")


def observadorEstudianteLibro(request, idEstudiante):
    if not request.session.get('isLogged', False):
        return redirect('login')
    estudiante = get_object_or_404(Estudiante, idEstudiante=idEstudiante)
    acudiente = get_object_or_404(Acudiente, idEstudiante=idEstudiante)
    observacion = get_object_or_404(Observacion, idEstudiante=idEstudiante)
    return render(request, 'observador/libro.html', {"estudiante": estudiante, "acudiente": acudiente, "observacion": observacion})
