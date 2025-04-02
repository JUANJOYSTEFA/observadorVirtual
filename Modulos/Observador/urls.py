from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView
from .views import *

urlpatterns = [
    path('listaColegio/', listaColegio, name='listaColegio'),
    path('agregarColegio/', agregarColegio, name="agregarColegio"),
    path('modificarColegio/<idColegio>/', modificarColegio, name="modificarColegio"),
    path('eliminarColegio/<idColegio>/', eliminarColegio, name="eliminarColegio"),
    path('listaGrado/', listaGrado, name='listaGrado'),
    path('agregarGrado/', agregarGrado, name="agregarGrado"),
    path('modificarGrado/<idGrado>/', modificarGrado, name="modificarGrado"),
    path('eliminarGrado/<idGrado>/', eliminarGrado, name="eliminarGrado"),
    path('listaEstudiante/', listaEstudiante, name='listaEstudiante'),
    path('agregarEstudiante/', agregarEstudiante, name="agregarEstudiante"),
    path('modificarEstudiante/<idEstudiante>/', modificarEstudiante, name="modificarEstudiante"),
    path('eliminarEstudiante/<idEstudiante>/', eliminarEstudiante, name="eliminarEstudiante"),
    path('listaAcudiente/', listaAcudiente, name='listaAcudiente'),
    path('agregarAcudiente/', agregarAcudiente, name="agregarAcudiente"),
    path('modificarAcudiente/<idAcudiente>/', modificarAcudiente, name="modificarAcudiente"),
    path('eliminarAcudiente/<idAcudiente>/', eliminarAcudiente, name="eliminarAcudiente"),
    path('listaAdministrativo/', listaAdministrativo, name='listaAdministrativo'),
    path('agregarAdministrativo/', agregarAdministrativo, name="agregarAdministrativo"),
    path('modificarAdministrativo/<idAdministrativo>/', modificarAdministrativo, name="modificarAdministrativo"),
    path('eliminarAdministrativo/<idAdministrativo>/', eliminarAdministrativo, name="eliminarAdministrativo"),
    path('listaFalta/', listaFalta, name='listaFalta'),
    path('agregarFalta/', agregarFalta, name="agregarFalta"),
    path('modificarFalta/<idFalta>/', modificarFalta, name="modificarFalta"),
    path('eliminarFalta/<idFalta>/', eliminarFalta, name="eliminarFalta"),
    path('listaObservacion/', listaObservacion, name='listaObservacion'),
    path('agregarObservacion/', agregarObservacion, name="agregarObservacion"),
    path('modificarObservacion/<idObservacion>/', modificarObservacion, name="modificarObservacion"),
    path('eliminarObservacion/<idObservacion>/', eliminarObservacion, name="eliminarObservacion"),
    path('listaCitacion/', listaCitacion, name='listaCitacion'),
    path('agregarCitacion/', agregarCitacion, name="agregarCitacion"),
    path('modificarCitacion/<idCitacion>/', modificarCitacion, name="modificarCitacion"),
    path('eliminarCitacion/<idCitacion>/', eliminarCitacion, name="eliminarCitacion"),
]
