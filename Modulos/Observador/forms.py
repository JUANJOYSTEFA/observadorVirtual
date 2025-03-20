from django import forms
from .models import *


class ColegioForm(forms.ModelForm):

	class Meta:
		model = Colegio
		fields = "__all__"


class GradoForm(forms.ModelForm):

	class Meta:
		model = Grado
		fields = "__all__"


class EstudianteForm(forms.ModelForm):

	class Meta:
		model = Estudiante
		fields = "__all__"


class AcudienteForm(forms.ModelForm):

	class Meta:
		model = Acudiente
		fields = "__all__"


class AdministrativosForm(forms.ModelForm):

	class Meta:
		model = Administrativos
		fields = "__all__"


class FaltasForm(forms.ModelForm):

	class Meta:
		model = Faltas
		fields = "__all__"


class ObservacionForm(forms.ModelForm):

	class Meta:
		model = Observacion
		fields = "__all__"


class CitacionesForm(forms.ModelForm):

	class Meta:
		model = Citaciones
		fields = "__all__"
