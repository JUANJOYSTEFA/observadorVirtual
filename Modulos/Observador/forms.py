from django import forms
from .models import Colegio, Grado, Estudiante, Acudiente, Administrativos, Faltas, Observacion, Citaciones

class ColegioForm(forms.ModelForm):

    class Meta:
        model = Colegio
        fields = "__all__"


class GradoForm(forms.ModelForm):

    class Meta:
        model = Grado
        fields = "__all__"


class EstudianteForm(forms.ModelForm):
    contrasena = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'id': 'password-input'}
        ),
        label="Contraseña",
        required=False  # Para que no sea obligatorio al editar
    )

    class Meta:
        model = Estudiante
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si se está editando (el objeto ya existe)
        if self.instance and self.instance.pk:
            self.fields.pop('contrasena', None)  # Quita el campo

    
class AcudienteForm(forms.ModelForm):
    contrasena = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,  # No obligatorio para que no bloquee el formulario al editar
        label="Contraseña"
    )

    class Meta:
        model = Acudiente
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si se está editando (ya existe en la BD)
        if self.instance and self.instance.pk:
            self.fields.pop('contrasena', None)  # Quita el campo


class AdministrativosForm(forms.ModelForm):
    class Meta:
        model = Administrativos
        fields = '__all__'  # Incluye todos los campos

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si el objeto ya existe (es edición)
        if self.instance and self.instance.pk:
            self.fields.pop('contrasena', None)  # Elimina el campo contraseña



class FaltasForm(forms.ModelForm):

    class Meta:
        model = Faltas
        fields = "__all__"


class ObservacionForm(forms.ModelForm):

    fecha = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'},
            format='%Y-%m-%d'  # 🔹Formato correcto para HTML5
        ),
        input_formats=['%Y-%m-%d']  # 🔹Formato que Django debe interpretar
    )
    hora = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
    )
    class Meta:
        model = Observacion
        fields = "__all__"


class CitacionesForm(forms.ModelForm):
    
    fecha = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'},
            format='%Y-%m-%d'  # 🔹Formato correcto para HTML5
        ),
        input_formats=['%Y-%m-%d']  # 🔹Formato que Django debe interpretar
    )
    hora = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
    )
    class Meta:
        model = Citaciones
        fields = "__all__"
