from django import forms
from django.forms import ValidationError

def solo_caracteres(value):
    if any(char.isdigit() for char in value):
        raise ValidationError('No puede contener numeros: %(valor)s', code='Invalid',params={'valor':value})

class LoginForm(forms.Form):
    email = forms.EmailField(label='',max_length=50,widget= forms.TextInput(attrs={'class':"form-control",'placeholder':"Email"}))
    password = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'class':"form-control",'placeholder':"Contraseña"}))

class RegisterForm(forms.Form):
    nombre = forms.CharField(label='',max_length=50,validators=(solo_caracteres,),widget= forms.TextInput(attrs={'class':"form-control",'placeholder':"Nombre"}))
    apellido = forms.CharField(label='',max_length=50,validators=(solo_caracteres,),widget= forms.TextInput(attrs={'class':"form-control",'placeholder':"Apellido"}))
    email = forms.EmailField(label='',max_length=50,widget= forms.TextInput(attrs={'class':"form-control",'placeholder':"Email"}))
    contraseña1 = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'class':"form-control",'placeholder':"Contraseña"}))
    contraseña2 = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'class':"form-control",'placeholder':"Repetir Contraseña"}))
    suscripcion = forms.BooleanField(
        label='Deseo suscribirme a las novedades de recetARIO.',
        required=False,
        widget=forms.CheckboxInput(attrs={'class':'form-check-input','value':1}))

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
    mail = forms.EmailField(label='',max_length=50,widget= forms.TextInput(attrs={'class':"form-control",'placeholder':"Email"}))
    asunto = forms.CharField(label='',max_length=80,widget= forms.TextInput(attrs={'class':"form-control",'placeholder':"Asunto"}))
    ensaje = forms.CharField(label='',max_length=500,widget= forms.Textarea(attrs={'class':"form-control",'placeholder':"Mensaje",'rows':'5'}))

    def clean_mensaje(self):
        data = self.cleaned_data['mensaje']
        if len(data) < 10:
            raise ValidationError('Explayate un poco mas por favor.')
        return data