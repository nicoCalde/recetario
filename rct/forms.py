from django import forms
from django.forms import ValidationError
from rct.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

def solo_caracteres(value):
    if any(char.isdigit() for char in value):
        raise ValidationError('No puede contener numeros: %(valor)s', code='Invalid',params={'valor':value})

#PUBLIC
class RegisterForm(UserCreationForm):
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}))
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repetir Contraseña'}))
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']
        widgets={
            'username': forms.TextInput(attrs={'class':'form-control','placeholder':'Usuario'}),
            'first_name': forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre'}),
            'last_name': forms.TextInput(attrs={'class':'form-control','placeholder':'Apellido'}),
            'email': forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}),
        }

class Logueo(AuthenticationForm):
    username= forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Usuario", "class": "form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña','class': 'form-control'}))

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

class ProductosForm(forms.ModelForm):

    class Meta:
        model=Productos
        fields=['nombre_producto']
        widgets={
            'nombre_producto': forms.TextInput(attrs={'class':'form-control'}),
        }

class RecetasForm(forms.ModelForm):

    class Meta:
        model=Recetas
        fields= ['nombre_receta', 'imagen_receta', 'tiempo_prep_receta', 'porciones_receta', 'pasos_receta']
        widgets={
            'nombre_receta': forms.TextInput(attrs={'class':'form-control'}),
            'imagen_receta': forms.FileInput(attrs={'class':'form-control-file'}),
            'tiempo_prep_receta': forms.TextInput(attrs={'class':'form-control'}),
            'porciones_receta': forms.TextInput(attrs={'class':'form-control'}),
            'pasos_receta': forms.Textarea(attrs={'class':'form-control'}),
        }

    def clean(self):
        data = self.cleaned_data
        nombre_receta = data.get('nombre_receta')
        qs = Recetas.objects.filter(nombre_receta=nombre_receta)
        if qs.exists():
            self.add_error('nombre_receta', f'\"{nombre_receta}\" ya existe. Por favor elegí otro nombre.')
        return data
    
class MedidasForm(forms.ModelForm):

    class Meta:
        model=UnidadesDeMedida
        fields=['nombre_medida']
        widgets={
            'nombre_medida': forms.TextInput(attrs={'class':'form-control'}),
        }

class IngredientesForm(forms.ModelForm):
    fkproductos = forms.ModelChoiceField(label='Producto',queryset=Productos.objects.all(),widget= forms.Select(attrs={'class':"form-control"}))
    cantidad = forms.CharField(label='Cantidad',widget= forms.TextInput(attrs={'class':"form-control"}))
    fkunidad_medida = forms.ModelChoiceField(label='Medida',queryset=UnidadesDeMedida.objects.all(),widget= forms.Select(attrs={'class':"form-control"}))

    class Meta:
        model=Ingredientes
        fields=['fkproductos','cantidad','fkunidad_medida']

    def clean(self):
        data = self.cleaned_data
        return data

class RecetasGuardadasForm(forms.ModelForm):

    class Meta:
        model=RecetasGuardadas
        exclude=('id','receta_guardada','fkuser')

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