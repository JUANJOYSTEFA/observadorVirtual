from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('observador/<documento>/', observadorEstudianteLibro, name="observador"),
    path('login/', iniciar_sesion, name="login"),
    path('salones/', salones, name="salones"),
    path('salones/<salon>', salon, name="salones"),
    path('estudiantes/<idGrado>', estudiantes, name="estudiantes"),    
    path('buscar/', buscarEstudiantes, name='buscarEstudiantes'),
    path('observaciones/pdf/<int:idEstudiante>/', generarPdfObservaciones, name='generarPdfObservaciones'),
    path('crear-citacion/<int:idEstudiante>/', crearCitacion, name='crearCitacion'),
    path('', home, name="home"),
    path('cerrar-sesion/', cerrar_sesion, name="cerrarSesion"),
    # URLs para restablecimiento de contraseña
    path('restablecer-contrasena/', solicitarRestablecer, name='solicitarRestablecer'),
    path('restablecer-contrasena/<str:token>/', restablecerContrasena, name='restablecerContrasena'),
]
