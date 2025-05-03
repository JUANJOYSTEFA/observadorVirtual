from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from Modulos.Observador.models import *
# Create your views here.


def observadorEstudianteLibro(request, documento):
    # Obtener el estudiante por documento
    estudiante = get_object_or_404(Estudiante, documento=documento)

    # Obtener el acudiente si existe
    acudiente = Acudiente.objects.filter(
        idEstudiante=estudiante.idEstudiante).first()

    # Obtener todas las observaciones del estudiante
    observacion = Observacion.objects.filter(
        idEstudiante=estudiante.idEstudiante)

    return render(request, 'observador/libro.html', {
        "estudiante": estudiante,
        "acudiente": acudiente,
        "observacion": observacion
    })


def salones(request):
    return render(request, "observador/salones.html")


def home(request):
    """Vista de la página de inicio"""

    # Si el usuario ha iniciado sesión, agregamos información al contexto
    context = {}

    if 'user_id' in request.session:
        context['user_logged_in'] = True
        context['user_type'] = request.session.get('user_type')
        context['user_nombre'] = request.session.get('user_nombre')

        user_type = request.session.get('user_type')
        user_id = request.session.get('user_id')

        if user_type == 'estudiante':
            try:
                estudiante = Estudiante.objects.get(idEstudiante=user_id)
                context['estudiante'] = estudiante
            except Estudiante.DoesNotExist:
                pass

        elif user_type == 'acudiente':
            try:
                acudiente = Acudiente.objects.get(idAcudiente=user_id)
                context['acudiente'] = acudiente
                context['estudiante_relacionado'] = acudiente.idEstudiante
            except Acudiente.DoesNotExist:
                pass

        elif user_type == 'administrativo':
            try:
                administrativo = Administrativos.objects.get(
                    idAdministrativo=user_id)
                context['administrativo'] = administrativo
                context['cargo'] = administrativo.cargo
            except Administrativos.DoesNotExist:
                pass

    # Aquí continúa tu lógica existente para la vista home

    return render(request, 'home.html', context)


def iniciar_sesion(request):
    """Vista para manejar el inicio de sesión intentando autenticar en múltiples modelos"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Lista de modelos y sus configuraciones para intentar la autenticación
        # Cada tupla contiene: (modelo, tipo_usuario, campo_id)
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
                if user.contrasena == password:  # Comparación directa, ajustar si usas hash
                    # Contraseña correcta, almacenar información en la sesión
                    request.session['user_id'] = getattr(user, id_field)
                    request.session['user_type'] = user_type
                    request.session['user_email'] = user.correo
                    request.session['user_nombre'] = f"{user.nombre} {user.apellido}"

                    # Si es administrativo, guardar el cargo
                    if user_type == 'administrativo':
                        request.session['user_cargo'] = user.cargo

                    # Redirigir a la página de inicio
                    return redirect('home')

                # Si encontramos el usuario pero la contraseña es incorrecta
                # No seguimos buscando en otros modelos
                messages.error(request, 'Correo o contraseña incorrectos')
                return render(request, 'iniciarsesion.html')

            except model.DoesNotExist:
                # Usuario no encontrado en este modelo, continuamos con el siguiente
                continue

        # Si llegamos aquí, el usuario no se encontró en ningún modelo
        messages.error(request, 'Correo o contraseña incorrectos')
        return render(request, 'iniciarsesion.html')

    # Si es una solicitud GET, mostrar el formulario
    return render(request, 'iniciarsesion.html')


def cerrar_sesion(request):
    """Vista para cerrar sesión"""
    # Eliminar datos de la sesión
    request.session.flush()
    return redirect('login')

# Modifica tu vista home existente para usar la información de sesión
# Si ya tienes una vista home, puedes adaptarla para que verifique la sesión

