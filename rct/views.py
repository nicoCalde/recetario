# from django.http import HttpResponse
from django.shortcuts import render
from rct.forms import ContactoForm,RegisterForm,LoginForm

# Create your views here.

#PUBLIC
def index(request):
    return render(request,'rct/public/index.html',)

def recetas(request):
    listado_recetas = [
    {
        'nombre_receta' : 'Pollo al horno con papas',
        'tipo_receta' : 'carnes',
        'productos_necesarios' : 'pollo',
    },
    {
        'nombre_receta' : 'Carne al horno con papas',
        'tipo_receta' : 'carnes',
        'productos_necesarios' : 'carne',
    },
    {
        'nombre_receta' : 'Tortilla de papas',
        'tipo_receta' : 'Acompañamientos',
        'productos_necesarios' : 'Huevos',
    },
    {
        'nombre_receta' : 'Salmon a la plancha con esparragos',
        'tipo_receta' : 'Pescados',
        'productos_necesarios' : 'Salmon',
    },
]
    return render(request,'rct/public/recetas.html',{'recetas' : listado_recetas},)

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
    return render(request,'rct/public/mis_recetas.html',{'misrecetas':listado_recetas})

def contact(request):
    if(request.method == 'POST'):
        contacto_form = ContactoForm(request.POST)
        if(contacto_form.is_valid()):
            pass
    else:
        contacto_form = ContactoForm()

    return render(request,'rct/public/contact.html',{'contacto_form':contacto_form})

def registro(request):
    if(request.method == 'POST'):
        register_form = RegisterForm(request.POST)
        if(register_form.is_valid()):
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
        login_form = LoginForm()
    return render(request,'rct/public/login.html',{'login_form':login_form})

def receta(request):
    return render(request,'rct/public/receta.html',)

def crear_receta(request):
    return render(request,'rct/public/crear_receta.html',)

def editar_receta(request):
    return render(request,'rct/public/editar_receta.html',)

def buscar_receta(request):
    return render(request,'rct/public/buscar_receta.html',)

#ADMINITRACION
def index_administracion(request):
    variable = 'test variable'
    return render(request,'rct/administration/index_administracion.html',{'variable':variable})

def register_adminitracion(request):
    return render(request,'rct/administration/register_administracion.html',)

def login_administracion(request):
    return render(request,'rct/administration/login_administracion.html',)

def forgotpass_administracion(request):
    return render(request,'rct/administration/forgotpass_administracion.html',)