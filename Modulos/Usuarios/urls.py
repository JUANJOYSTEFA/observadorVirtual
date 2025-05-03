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
    path('cerrar-sesion/', cerrar_sesion, name="cerrar_sesion"),

    # Rutas para restablecimiento de contraseña
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',
        email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='password_reset_complete.html'
    ), name='password_reset_complete'),
]
