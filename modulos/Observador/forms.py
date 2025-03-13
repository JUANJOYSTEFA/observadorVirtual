from django import forms
from .models import Colegio


class ColegioForm(forms.ModelForm):

	class Meta:
		model = Colegio
		fields = "__all__"
