from django.shortcuts import redirect
from django.urls import reverse
from django.urls import resolve, Resolver404


class SessionAuthMiddleware:
    """
    Middleware para verificar si el usuario ha iniciado sesión.
    Puedes usar este middleware para proteger rutas específicas.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Lista de rutas que no requieren autenticación
        public_paths = [
            '/login/',
            '/password_reset/',
            '/password_reset/done/',
            '/reset/',
            '/admin/',
            # Añade aquí otras rutas públicas
        ]

        # Comprueba si la ruta actual requiere autenticación
        requires_auth = True
        for path in public_paths:
            if request.path.startswith(path):
                requires_auth = False
                break

        # Si la ruta requiere autenticación y el usuario no ha iniciado sesión, redirige al login
        if requires_auth and 'user_id' not in request.session:
            return redirect('login')

        response = self.get_response(request)
        return response


class RedirectToHomeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            # Intenta resolver la URL solicitada
            resolve(request.path_info)
        except Resolver404:
            # Si no se encuentra la URL, redirige a la página de inicio
            # Cambia 'home' por el nombre de tu URL de inicio
            return redirect('home')
        response = self.get_response(request)
        return response
