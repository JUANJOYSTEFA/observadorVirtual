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
        required=False
    )
    

    class Meta:
        model = Estudiante
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields.pop('contrasena', None)


    
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

class ObservacionFormProfesor(forms.ModelForm):
    fecha = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'},
            format='%Y-%m-%d'
        ),
        input_formats=['%Y-%m-%d']
    )
    hora = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'})
    )
    
    # Campos ocultos para asegurar que los valores se envíen
    estudiante_hidden = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    administrativo_hidden = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = Observacion
        fields = ['idFalta', 'comentario', 'fecha', 'hora', 'estudiante_hidden', 'administrativo_hidden']
    
    def __init__(self, *args, **kwargs):
        estudiante_id = kwargs.pop('estudiante_id', None)
        administrativo_id = kwargs.pop('administrativo_id', None)
        super().__init__(*args, **kwargs)
        
        # Configurar campo de estudiante
        if estudiante_id:
            self.fields['idEstudiante'] = forms.ModelChoiceField(
                queryset=Estudiante.objects.filter(idEstudiante=estudiante_id),
                widget=forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
                initial=estudiante_id,
                required=False
            )
            self.initial['estudiante_hidden'] = estudiante_id
        else:
            self.fields['idEstudiante'] = forms.ModelChoiceField(
                queryset=Estudiante.objects.all(),
                widget=forms.Select(attrs={'class': 'form-control'}),
            )
        
        # Configurar campo de administrativo
        if administrativo_id:
            self.fields['idAdministrativo'] = forms.ModelChoiceField(
                queryset=Administrativos.objects.filter(idAdministrativo=administrativo_id),
                widget=forms.Select(attrs={'class': 'form-control', 'readonly': 'readonly'}),
                initial=administrativo_id,
                required=False
            )
            self.initial['administrativo_hidden'] = administrativo_id


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
