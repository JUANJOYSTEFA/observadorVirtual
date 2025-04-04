from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('observador/<idEstudiante>/', observadorEstudianteLibro, name="observador")
]