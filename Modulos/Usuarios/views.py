from django.shortcuts import render, get_object_or_404
import secrets
from django.urls import reverse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from Modulos.Observador.models import *
# Create your views here.


def observadorEstudianteLibro(request, documento):
    if not request.session.get('isLogged', False):
        return redirect('login')
    userType = request.session.get('userType', False)
    admin = userType ==  'profesor' or userType == 'directivo'
    documentoIniciado = request.session.get('documento', False)
    if (userType == 'estudiante' or userType == 'acudiente') and documento != documentoIniciado:
        return redirect('observador', documento=documentoIniciado)

    estudiante = get_object_or_404(Estudiante, documento=documento)
    acudiente = Acudiente.objects.filter(
        idEstudiante=estudiante.idEstudiante).first()
    observaciones = list(Observacion.objects.filter(
        idEstudiante=estudiante.idEstudiante))
    idEstudiante = estudiante.idEstudiante
    # Agrupar observaciones de a 3
    observaciones_agrupadas = [observaciones[i:i+3]
                               for i in range(0, len(observaciones), 3)]

    return render(request, 'observador/libro.html', {
        "estudiante": estudiante,
        "acudiente": acudiente,
        "observaciones_agrupadas": observaciones_agrupadas,
        "admin": admin,
        "idEstudiante" : idEstudiante
    })


def salones(request):
    if not request.session.get('isLogged', False):
        return redirect('login')
    
    userType = request.session.get('userType', False)
    documentoIniciado = request.session.get('documento', False)
    if (userType == 'estudiante' or userType == 'acudiente'):
        return redirect('observador', documento=documentoIniciado)

    salones = Grado.objects.all()
    return render(request, "observador/salones.html", {'salones': salones})


def salon(request, salon):
    if not request.session.get('isLogged', False):
        return redirect('login')
    salones = Grado.objects.all()

    userType = request.session.get('userType', False)
    documentoIniciado = request.session.get('documento', False)
    if (userType == 'estudiante' or userType == 'acudiente'):
        return redirect('observador', documento=documentoIniciado)

    if salon:
        salones = salones.filter(
            Q(grado__icontains=salon)
        )

    return render(request, "observador/salones.html", {'salones': salones})


def estudiantes(request, idGrado):
    if not request.session.get('isLogged', False):
        return redirect('login')
    
    userType = request.session.get('userType', False)
    documentoIniciado = request.session.get('documento', False)
    if (userType == 'estudiante' or userType == 'acudiente'):
        return redirect('observador', documento=documentoIniciado)

    # Obtener el grado específico o mostrar error 404 si no existe
    grado = get_object_or_404(Grado, idGrado=idGrado)
    # Obtener todos los estudiantes cuyo campo idGrado es este grado
    estudiantes = Estudiante.objects.filter(idGrado=grado)
    # Filtrar por nombre
    query = request.GET.get('search', '')
    if query:
        estudiantes = estudiantes.filter(nombre__icontains=query)
    # Ordenar
    # Por defecto, ordenar por totalFaltas (de mayor a menor)
    order_by = request.GET.get('order_by', '-totalFaltas')
    estudiantes = estudiantes.order_by(order_by)
    # Pasar grado y estudiantes al contexto para renderizar en la plantilla
    context = {
        'grado': grado,
        'estudiantes': estudiantes,
        'search_query': query,  # Pasar la consulta de búsqueda al contexto
        'order_by': order_by,   # Pasar el criterio de ordenamiento al contexto
    }
    return render(request, 'observador/estudiantes.html', context)


def buscarEstudiantes(request):
    if not request.session.get('isLogged', False):
        return redirect('login')
    
    userType = request.session.get('userType', False)
    documentoIniciado = request.session.get('documento', False)
    if (userType == 'estudiante' or userType == 'acudiente'):
        return redirect('observador', documento=documentoIniciado)

    query = request.GET.get('search', '')
    # Por defecto, ordenar por totalFaltas
    order_by = request.GET.get('order_by', '-totalFaltas')
    # Obtener todos los estudiantes
    estudiantes = Estudiante.objects.all()
    # Filtrar por nombre o apellido
    if query:
        estudiantes = estudiantes.filter(
            Q(nombre__icontains=query) | Q(apellido__icontains=query)
        )
    # Ordenar
    estudiantes = estudiantes.order_by(order_by)
    context = {
        'estudiantes': estudiantes,
        'search_query': query,
        'order_by': order_by,  # Pasar el criterio de ordenamiento al contexto
    }
    return render(request, 'observador/buscarEstudiantes.html', context)


def crearCitacion(request, idEstudiante):
    estudiante = get_object_or_404(Estudiante, idEstudiante=idEstudiante)

    if request.method == 'POST':
        fecha = request.POST['fecha']
        hora = request.POST['hora']
        acudiente = get_object_or_404(Acudiente, idEstudiante=idEstudiante)

        if not acudiente:
            messages.error(
                request, "Este estudiante no tiene acudiente registrado.")
            return redirect('observador', documento=estudiante.documento)

        citacion = Citaciones.objects.create(
            fecha=fecha,
            hora=hora,
            idEstudiante=estudiante,
            idAcudiente=acudiente
        )

        # Redirigir a Google Calendar
        dtInicio = datetime.strptime(f"{fecha} {hora}", "%Y-%m-%d %H:%M")
        dtFin = dtInicio + timedelta(minutes=30)
        print("Redireccionando a:", reverse('observador', kwargs={'documento': estudiante.documento}))
        def formatoFecha(dt):
            return dt.strftime('%Y%m%dT%H%M%S')

        url = "https://calendar.google.com/calendar/render?action=TEMPLATE"
        url += f"&text=Citación con {acudiente.nombre} {acudiente.apellido} y {estudiante.nombre} {estudiante.apellido}"
        url += f"&dates={formatoFecha(dtInicio)}/{formatoFecha(dtFin)}"
        url += "&details=Observador Virtual - Reunión con acudiente"
        url += "&location=Colegio San Francisco de Asís"
        url += "&sf=true&output=xml"

        return redirect(url)
    # ← Aquí estudiante ya está definido
    return redirect('observador', documento=estudiante.documento)



def home(request):
    """Vista de la página de inicio"""

    # Inicializa el contexto
    context = {}
    isLoggedIn = request.session.get('isLogged', False)
    id = request.session.get('userId', False)
    context['userType'] = request.session.get('userType', False)

    if isLoggedIn:
        context['userLogged'] = True
        # Asegúrate de que la clave sea correcta
        context['userNombre'] = request.session.get(
            'userNombre')  # Asegúrate de que la clave sea correcta

        user_type = context['userType']
        # Asegúrate de que la clave sea correcta
        user_id = request.session.get('userId')

        if user_type == 'estudiante':
            try:
                estudiante = Estudiante.objects.get(idEstudiante=user_id)
                context['estudiante'] = estudiante
                context['documento'] = estudiante.documento
                request.session['documento'] = context['documento']
            except Estudiante.DoesNotExist:
                pass

        elif user_type == 'acudiente':
            try:
                acudiente = Acudiente.objects.get(idAcudiente=user_id)
                context['acudiente'] = acudiente
                context['estudianteRelacionado'] = acudiente.idEstudiante
                context['documento'] = context['estudianteRelacionado'].documento
                request.session['documento'] = context['documento']
            except Acudiente.DoesNotExist:
                pass

        elif user_type == 'directivo':
            try:
                administrativo = Administrativos.objects.get(
                    idAdministrativo=user_id)
                context['administrativo'] = administrativo
                context['cargo'] = administrativo.cargo
                context['admin'] = context['cargo'] == 'directivo'
            except Administrativos.DoesNotExist:
                pass

        # Renderiza la página de bienvenida con el contexto
        return render(request, 'home.html', context)
    else:
        # Si el usuario no está autenticado, renderiza la página de inicio
        return render(request, 'home.html')


def iniciar_sesion(request):
    """Vista para manejar el inicio de sesión intentando autenticar en múltiples modelos"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Lista de modelos y sus configuraciones para intentar la autenticación
        modelos_autenticacion = [
            (Estudiante, 'estudiante', 'idEstudiante'),
            (Acudiente, 'acudiente', 'idAcudiente'),
            (Administrativos, 'administrativo', 'idAdministrativo')
        ]

        # Intentar autenticar el usuario en cada modelo secuencialmente
        for model, user_type, id_field in modelos_autenticacion:
            try:
                user = model.objects.get(correo=email)

                # Verificar la contraseña
                if check_password(password, user.contrasena):
                    # Contraseña correcta, almacenar información en la sesión
                    request.session['isLogged'] = True
                    request.session['userId'] = getattr(user, id_field)
                    request.session['userType'] = user_type
                    request.session['userEmail'] = user.correo
                    request.session['userNombre'] = f"{user.nombre} {user.apellido}"

                    # Si es administrativo, guardar el cargo
                    if user_type == 'administrativo':
                        request.session['userType'] = user.cargo

                    # Redirigir a la página de inicio
                    return redirect('home')

            except model.DoesNotExist:
                # Usuario no encontrado en este modelo, continuamos con el siguiente
                continue

        # Si llegamos aquí, el usuario no se encontró en ningún modelo o la contraseña fue incorrecta
        messages.error(request, 'Correo o contraseña incorrectos')
        return render(request, 'iniciarsesion.html')

    # Si es una solicitud GET, mostrar el formulario
    return render(request, 'iniciarsesion.html')


def cerrar_sesion(request):
    """Vista para cerrar sesión"""
    # Eliminar datos de la sesión
    request.session.flush()
    return redirect('login')

# En el archivo views.py


# Ejemplo con diferentes tipos de mensajes:


def solicitarRestablecer(request):
    """Vista para solicitar el restablecimiento de contraseña"""
    if request.method == 'POST':
        email = request.POST.get('email')

        # Lista de modelos para buscar el correo
        modelos = [Estudiante, Acudiente, Administrativos]
        usuario_encontrado = False

        # Verificar si el correo existe en alguno de los modelos
        for modelo in modelos:
            try:
                usuario = modelo.objects.get(correo=email)
                usuario_encontrado = True
                break
            except modelo.DoesNotExist:
                continue

        if usuario_encontrado:
            # Generar token único
            token = secrets.token_urlsafe(32)

            # Establecer fecha de expiración (24 horas)
            fecha_expiracion = timezone.now() + timedelta(hours=24)

            # Guardar el token en la base de datos
            TokenRestablecimiento.objects.create(
                correo=email,
                token=token,
                fecha_expiracion=fecha_expiracion
            )

            # Construir la URL de restablecimiento
            reset_url = request.build_absolute_uri(
                reverse('restablecerContrasena', args=[token])
            )

            # Enviar correo con el enlace
            try:
                send_mail(
                    'Restablecimiento de contraseña',
                    f'Haga clic en el siguiente enlace para restablecer su contraseña: {reset_url}\n'
                    f'Este enlace expirará en 24 horas.',
                    'noreplyvirttob@gmail.com',  # Remitente
                    [email],  # Destinatario
                    fail_silently=False,
                )

                # Mensaje de éxito (SUCCESS)
                messages.success(
                    request,
                    'Se ha enviado un correo con instrucciones para restablecer su contraseña.'
                )
            except Exception as e:
                # Mensaje de error (ERROR) si falla el envío
                messages.error(
                    request,
                    'Ocurrió un error al enviar el correo. Por favor intente más tarde.'
                )

            return redirect('login')
        else:
            # Mantener mensajes genéricos por seguridad (INFO)
            messages.info(
                request,
                'Si su correo está registrado, recibirá instrucciones para restablecer su contraseña.'
            )
            return redirect('login')

    return render(request, 'solicitarRestablecer.html')


def restablecerContrasena(request, token):
    """Vista para establecer nueva contraseña con el token"""
    try:
        # Buscar el token en la base de datos
        token_obj = TokenRestablecimiento.objects.get(token=token)

        # Verificar si el token es válido
        if not token_obj.esta_activo():
            # Mensaje de advertencia (WARNING)
            messages.warning(
                request, 'El enlace ha expirado o ya ha sido utilizado.')
            return redirect('login')

        if request.method == 'POST':
            # Obtener la nueva contraseña
            nuevaContrasena = request.POST.get('password')
            confirmacion = request.POST.get('confirm_password')

            # Validar que las contraseñas coincidan
            if nuevaContrasena != confirmacion:
                # Mensaje de error (ERROR)
                messages.error(request, 'Las contraseñas no coinciden.')
                return render(request, 'restablecerContrasena.html', {'token': token})

            # Hashear la contraseña antes de guardarla
            contrasenaHasheada = make_password(nuevaContrasena)

            # Actualizar la contraseña en todos los modelos donde exista el correo
            modelos = [Estudiante, Acudiente, Administrativos]
            actualizado = False

            for modelo in modelos:
                try:
                    usuario = modelo.objects.get(correo=token_obj.correo)
                    usuario.contrasena = contrasenaHasheada  # Guardar contraseña hasheada
                    usuario.save()
                    actualizado = True
                except modelo.DoesNotExist:
                    continue

            # Marcar el token como usado
            token_obj.usado = True
            token_obj.save()

            if actualizado:
                # Mensaje de éxito (SUCCESS)
                messages.success(
                    request, 'Su contraseña ha sido actualizada correctamente.')
            else:
                # Mensaje de error (ERROR)
                messages.error(request, 'No se pudo actualizar la contraseña.')

            return redirect('login')

        return render(request, 'restablecerContrasena.html', {'token': token})

    except TokenRestablecimiento.DoesNotExist:
        # Mensaje de error (ERROR)
        messages.error(request, 'El enlace no es válido.')
        return redirect('login')
