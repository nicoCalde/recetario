from django import forms
from django.forms import ValidationError
from rct.models import *

def solo_caracteres(value):
    if any(char.isdigit() for char in value):
        raise ValidationError('No puede contener numeros: %(valor)s', code='Invalid',params={'valor':value})

#PUBLIC
class LoginForm(forms.Form):
    email = forms.EmailField(label='',max_length=50,widget= forms.TextInput(attrs={'class':"form-control",'placeholder':"Email"}))
    password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'class':"form-control",'placeholder':"Contraseña"}))

class RegisterForm(forms.Form):
    nombre = forms.CharField(label='',max_length=50,validators=(solo_caracteres,),widget= forms.TextInput(attrs={'class':"form-control",'placeholder':"Nombre"}))
    apellido = forms.CharField(label='',max_length=50,validators=(solo_caracteres,),widget= forms.TextInput(attrs={'class':"form-control",'placeholder':"Apellido"}))
    email = forms.EmailField(label='',max_length=50,error_messages={'invalid':'Por favor ingresa un email valido'},widget= forms.TextInput(attrs={'class':"form-control",'placeholder':"Email"}))
    contraseña1 = forms.CharField(label='',max_length=32, widget=forms.PasswordInput(attrs={'class':"form-control",'placeholder':"Contraseña"}))
    contraseña2 = forms.CharField(label='',max_length=32, widget=forms.PasswordInput(attrs={'class':"form-control",'placeholder':"Repetir Contraseña"}))
    # suscripcion = forms.BooleanField(
    #     label='Deseo suscribirme a las novedades de recetARIO.',
    #     required=False,
    #     widget=forms.CheckboxInput(attrs={'class':'form-check-input','value':1}))

    def clean_contraseña1(self):
        data = self.cleaned_data['contraseña1']
        if len(data) < 8:
            raise ValidationError('Debe contener al menos 8 caracteres.',code='Invalid')
        return data
    def clean(self):
        cleaned_data = super().clean()
        contraseña1 = cleaned_data.get('contraseña1')
        contraseña2 = cleaned_data.get('contraseña2')
        if contraseña1 != contraseña2:
            msg = 'Las contraseñas deben ser igules.'
            self.add_error('contraseña2',msg)

class ContactoForm(forms.Form):
    nombre = forms.CharField(label='',max_length=50,validators=(solo_caracteres,),widget= forms.TextInput(attrs={'class':"form-control",'placeholder':"Nombre"}))
    email = forms.EmailField(label='',max_length=50,widget= forms.TextInput(attrs={'class':"form-control",'placeholder':"Email"}))
    asunto = forms.CharField(label='',max_length=80,widget= forms.TextInput(attrs={'class':"form-control",'placeholder':"Asunto"}))
    mensaje = forms.CharField(label='',max_length=500,widget= forms.Textarea(attrs={'class':"form-control",'placeholder':"Mensaje",'rows':'5'}))

    def clean_mensaje(self):
        data = self.cleaned_data['mensaje']
        if len(data) < 10:
            raise ValidationError('Explayate un poco mas por favor.')
        return data

class RecetasForm(forms.ModelForm):

    class Meta:
        model=Recetas
        fields= ['nombre_receta', 'imagen_receta', 'tiempo_prep_receta', 'porciones_receta', 'pasos_receta']
        widgets={
            'nombre_receta': forms.TextInput(attrs={'class':'form-control'}),
            # 'imagen_receta': forms.ImageField(attrs={'class':'form-control'}),
            'tiempo_prep_receta': forms.TextInput(attrs={'class':'form-control'}),
            'porciones_receta': forms.TextInput(attrs={'class':'form-control'}),
            'pasos_receta': forms.Textarea(attrs={'class':'form-control'}),
        }

      

#ADMINISTRACION
class AdminLoginForm(forms.Form):
    email = forms.EmailField(label='',max_length=50,widget= forms.TextInput(attrs={'class':"form-control form-control-user",'placeholder':"Email"}))
    password = forms.CharField(label='',max_length=32, widget=forms.PasswordInput(attrs={'class':"form-control form-control-user",'placeholder':"Contraseña"}))
    recordarme = forms.BooleanField(
        label='Recordarme',
        required=False,
        widget=forms.CheckboxInput(attrs={'class':'custom-control-input','value':0}))

class AdminRegisterForm(forms.Form):
    nombre = forms.CharField(label='nombre',max_length=50,validators=(solo_caracteres,),widget= forms.TextInput(attrs={'class':"form-control form-control-user",'placeholder':"Nombre"}))
    apellido = forms.CharField(label='apellido',max_length=50,validators=(solo_caracteres,),widget= forms.TextInput(attrs={'class':"form-control form-control-user",'placeholder':"Apellido"}))
    email = forms.EmailField(label='email',max_length=50,error_messages={'invalid':'Por favor ingresa un email valido'},widget= forms.TextInput(attrs={'class':"form-control form-control-user",'placeholder':"Email"}))
    contraseña1 = forms.CharField(label='contraseña1',max_length=32, widget=forms.PasswordInput(attrs={'class':"form-control form-control-user",'placeholder':"Contraseña"}))
    contraseña2 = forms.CharField(label='contraseña2',max_length=32, widget=forms.PasswordInput(attrs={'class':"form-control form-control-user",'placeholder':"Repetir Contraseña"}))

    def clean_contraseña1(self):
        data = self.cleaned_data['contraseña1']
        if len(data) < 8:
            raise ValidationError('Debe contener al menos 8 caracteres.',code='Invalid')
        return data
    def clean(self):
        cleaned_data = super().clean()
        contraseña1 = cleaned_data.get('contraseña1')
        contraseña2 = cleaned_data.get('contraseña2')
        if contraseña1 != contraseña2:
            msg = 'Las contraseñas deben ser igules.'
            self.add_error('contraseña2',msg)

class AdminResetForm(forms.Form):
    email = forms.EmailField(label='email',max_length=50,error_messages={'invalid':'Por favor ingresa un email valido'},widget= forms.TextInput(attrs={'class':"form-control form-control-user",'placeholder':"Email"}))