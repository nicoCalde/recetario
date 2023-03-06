from django import forms
from django.forms import ValidationError 
from rct.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UserChangeForm,PasswordChangeForm,PasswordResetForm,SetPasswordForm

def solo_caracteres(value):
    if any(char.isdigit() for char in value):
        raise ValidationError('No puede contener numeros: %(valor)s', code='Invalid',params={'valor':value})

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

class PassChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña Anterior'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña Nueva'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repetir Contraseña'}))

class PassResetForm(PasswordResetForm):
    email = forms.EmailField(label='',widget= forms.TextInput(attrs={'class':"form-control",'placeholder':"Ingresa tu Email"}))

class NewPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña Nueva'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repetir Contraseña'}))

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
    
    def clean(self):
        data = self.cleaned_data
        nombre_producto = data.get('nombre_producto')
        qs = Productos.objects.filter(nombre_producto=nombre_producto)
        if qs.exists():
            self.add_error('nombre_producto', f'\"{nombre_producto}\" ya existe. Por favor elegí otro nombre.')
        return data

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
    
class InstruccionesForm(forms.ModelForm):

    class Meta:
        model=Recetas
        fields=['pasos_receta']
        widgets={
            'pasos_receta': forms.Textarea(attrs={'class':'form-control'}),
        }

class MedidasForm(forms.ModelForm):

    class Meta:
        model=UnidadesDeMedida
        fields=['nombre_medida']
        widgets={
            'nombre_medida': forms.TextInput(attrs={'class':'form-control'}),
        }
    
    def clean(self):
        data = self.cleaned_data
        nombre_medida = data.get('nombre_medida')
        qs = UnidadesDeMedida.objects.filter(nombre_medida=nombre_medida)
        if qs.exists():
            self.add_error('nombre_medida', f'\"{nombre_medida}\" ya existe. Por favor elegí otro nombre.')
        return data

class IngredientesForm(forms.ModelForm):
    fkproductos = forms.ModelChoiceField(label='Producto',queryset=Productos.objects.all(),widget= forms.Select(attrs={'class':"form-control","id":"select-square"}))
    cantidad = forms.CharField(label='Cantidad',widget= forms.TextInput(attrs={'class':"form-control"}))
    fkunidad_medida = forms.ModelChoiceField(label='Medida',queryset=UnidadesDeMedida.objects.all(),widget= forms.Select(attrs={'class':"form-control","id":"select-square"}))

    class Meta:
        model=Ingredientes
        fields=['fkproductos','cantidad','fkunidad_medida']

    def clean_fkproductos(self):
        data = self.cleaned_data['fkproductos']
        if data is None:
            raise ValidationError('El ingrediente no puede ser ninguno.')
        return data
    
    def clean_cantidad(self):
        data = self.cleaned_data['cantidad']
        if len(data) < 1:
            raise ValidationError('Elige una cantidad.')
        return data
    
    def clean_fkunidad_medida(self):
        data = self.cleaned_data['fkunidad_medida']
        if data is None:
            raise ValidationError('Elige una unidad de medida.')
        return data

    def clean(self):
        data = self.cleaned_data
        return data

class RecetasGuardadasForm(forms.ModelForm):

    class Meta:
        model=RecetasGuardadas
        exclude=('id','receta_guardada','fkuser')

class EditUserForm(UserChangeForm):

    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        widgets={
            'username': forms.TextInput(attrs={'class':'form-control','placeholder':'Usuario'}),
            'first_name': forms.TextInput(attrs={'class':'form-control','placeholder':'Nombre'}),
            'last_name': forms.TextInput(attrs={'class':'form-control','placeholder':'Apellido'}),
            'email': forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}),
        }

class MessagesForm(forms.ModelForm):

    class Meta:
        model=Messages
        fields=['receiver','subject','msg_content']
        widgets={
            'receiver': forms.Select(attrs={'class':'form-control'}),
            'subject': forms.TextInput(attrs={'class':'form-control'}),
            'msg_content': forms.Textarea(attrs={'class':'form-control'}),
        }