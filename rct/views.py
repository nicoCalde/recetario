# from django.http import HttpResponse
from django.shortcuts import render,redirect
from rct.forms import *
from django.contrib import messages
from rct.models import *

# Create your views here.

#PUBLIC
def index(request):
    return render(request,'rct/public/index.html',)

def recetas(request):
    recetas = Recetas.objects.all().order_by('nombre_receta')
    ingredientes = Ingredientes.objects.all()
    productos = Productos.objects.all()
    return render(request,'rct/public/recetas.html',{'recetas':recetas,'ingredientes':ingredientes,'productos':productos})

def mis_recetas(request):
    listado_recetas = [
    {
        'nombre_receta' : 'Fideos a la carbonara',
        'tipo_receta' : 'pasta',
        'productos_necesarios' : ['Fideos','Huevos','Aceite'],
    },
    {
        'nombre_receta' : 'Carre de cerdo al horno',
        'tipo_receta' : 'carnes',
        'productos_necesarios' : ['Cerdo','Ciruelas','Sal'],
    },
    {
        'nombre_receta' : 'Torrejas de verdura',
        'tipo_receta' : 'Acompañamientos',
        'productos_necesarios' : ['Espinaca','Huevos','Aceite'],
    },
    {
        'nombre_receta' : 'Brotola con ensalada',
        'tipo_receta' : 'Pescados',
        'productos_necesarios' : ['Brotola','Zanahoria','Lechuga','Tomate'],
    },
]
    # recetas = Recetas.objects.filter()
    return render(request,'rct/public/mis_recetas.html',{'misrecetas':listado_recetas})

def contact(request):
    if(request.method == 'POST'):
        contacto_form = ContactoForm(request.POST)
        if(contacto_form.is_valid()):
            messages.success(request,'¡Gracias por comunicarte con nostros, te estaremos respondiedo a la brevedad!')
            contacto_form = ContactoForm()
            #enviar un mail al administrador
    else:
        contacto_form = ContactoForm()

    return render(request,'rct/public/contact.html',{'contacto_form':contacto_form})

def registro(request):
    if(request.method == 'POST'):
        register_form = RegisterForm(request.POST)
        if(register_form.is_valid()):
            #enviar email al administrador con los datos que recibio y guardar los datos en la base de datos
            #enviarle al usuario alguna respuesta
            pass
    else:
        register_form = RegisterForm()
    return render(request,'rct/public/registro.html',{'register_form':register_form})

def login(request):
    if(request.method == 'POST'):
        login_form = LoginForm(request.POST)
        if(login_form.is_valid()):
            pass
        else:
            messages.error(request,'El email y/o la contraseña no son validos')
    else:
        login_form = LoginForm()
    return render(request,'rct/public/login.html',{'login_form':login_form})

def receta(request):
    return render(request,'rct/public/receta.html',)

def crear_receta(request):
    if(request.method=='POST'):
        formulario = RecetasForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('mis_recetas')
    else:
        formulario = RecetasForm()
    return render(request,'rct/public/crear_receta.html',{'formulario':formulario})

def eliminar_receta(request,id_receta):
    try:
        receta = Recetas.objects.get(pk=id_receta)
    except Recetas.DoesNotExist:
        return render(request,'rct/public/404.html')
    receta.delete() 
    return redirect('mis_recetas')

def editar_receta(request,id_receta):
    try:
        receta = Recetas.objects.get(pk=id_receta)
    except Recetas.DoesNotExist:
        return render(request,'rct/public/404.html')
    if(request.method == 'POST'):
        formulario = Recetas(request.POST,instance=receta)
        if formulario.is_Valid():
            formulario.save()
            return redirect('mis_recetas')
    else:
        formulario = Recetas(instance=receta)
    return render(request,'rct/public/editar_receta.html',{'formulario':formulario})

def crear_producto(request):
    if(request.method=='POST'):
        formulario = ProductosForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('crear_receta')
    else:
        formulario = ProductosForm()
    return render(request,'rct/public/crear_producto.html',{'formulario':formulario})

#ADMINISTRACION
def index_administracion(request):
    variable = 'test variable'
    return render(request,'rct/administration/index_administracion.html',{'variable':variable})

def register_adminitracion(request):
    if(request.method == 'POST'):
        register_form = AdminRegisterForm(request.POST)
        if(register_form.is_valid()):
            #enviar email al administrador con los datos que recibio y guardar los datos en la base de datos
            #enviarle al usuario alguna respuesta
            pass
    else:
        register_form = AdminRegisterForm()
    return render(request,'rct/administration/register_administracion.html',{'register_form':register_form})

def login_administracion(request):
    if(request.method == 'POST'):
        login_form = AdminLoginForm(request.POST)
        if(login_form.is_valid()):
            pass
        else:
            messages.error(request,'El email y/o la contraseña no son validos')
    else:
        login_form = AdminLoginForm()
    return render(request,'rct/administration/login_administracion.html',{'login_form':login_form})

def forgotpass_administracion(request):
    if(request.method == 'POST'):
        reset_form = AdminResetForm(request.POST)
        if(reset_form.is_valid()):
            pass
        else:
            messages.error(request,'El email ingresado no es valido.')
    else:
        reset_form = AdminResetForm()
    return render(request,'rct/administration/forgotpass_administracion.html',{'reset_form':reset_form})