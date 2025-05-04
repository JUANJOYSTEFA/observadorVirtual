from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('observador/<documento>/', observadorEstudianteLibro, name="observador"),
    # Mantiene la URL 'login/' pero usa la nueva vista
    path('login/', iniciar_sesion, name="login"),
    path('salones/', salones, name="salones"),
    path('', home, name="home"),
    path('cerrar-sesion/', cerrar_sesion, name="cerrarSesion"),
    # URLs para restablecimiento de contraseña
    path('restablecer-contrasena/', solicitarRestablecer, name='solicitarRestablecer'),
    path('restablecer-contrasena/<str:token>/', restablecerContrasena, name='restablecerContrasena'),
]
