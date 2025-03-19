from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from .models import *  # Importa el modelo
from .forms import ColegioForm
from django.contrib import messages

def redirigirHome(request):
    return redirect('listaColegios')
class IndexView(TemplateView):
    template_name = 'index.html'

class LoginFormView(LoginView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)

def listaColegios(request):
    colegios = Colegio.objects.all()  # Obtiene todos los registros
    return render(request, 'listaColegios.html', {'colegios': colegios})

def agregarColegio(request):
	data={
		'form': ColegioForm()
	}

	if request.method =='POST':
		formulario = ColegioForm(data=request.POST, files=request.FILES)
		if formulario.is_valid():
			formulario.save()
			messages.success(request, "Guardado Correctamente")
			return redirect('listaColegios')
		else:
			data["form"]=formulario
			messages.warning(request, "El archivo ya existe")
			#data["mensaje"]="el archivo ya existe"
	return render(request, 'agregarColegio.html', data)

def modificarColegio(request, idColegio):
    colegio = get_object_or_404(Colegio, idColegio=idColegio)  # Busca un elemento por su ID

    data = {
        'form': ColegioForm(instance=colegio)
    }

    if request.method == 'POST':
        formulario = ColegioForm(data=request.POST, instance=colegio, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado Correctamente")
            return redirect('listaColegios')  

        data["form"] = formulario 
    return render(request, 'modificar.html', data)

def eliminarColegio(request, idColegio):
	carrera = get_object_or_404(Colegio, idColegio=idColegio)
	carrera.delete()
	messages.success(request, "Eliminado Correctamente")
	return redirect(to="listaColegios")

def index(request):
    return render(request, 'index.html')