# from django.http import HttpResponse
from django.shortcuts import render

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
        'imagen' : 'https://picsum.photos/200/300',
    },
    {
        'nombre_receta' : 'Carne al horno con papas',
        'tipo_receta' : 'carnes',
        'productos_necesarios' : 'carne',
        'imagen' : 'https://picsum.photos/200/300',
    },
    {
        'nombre_receta' : 'Tortilla de papas',
        'tipo_receta' : 'Acompañamientos',
        'productos_necesarios' : 'Huevos',
        'imagen' : 'https://picsum.photos/200/300',
    },
    {
        'nombre_receta' : 'Salmon a la plancha con esparragos',
        'tipo_receta' : 'Pescados',
        'productos_necesarios' : 'Salmon',
        'imagen' : 'https://picsum.photos/200/300',
    },
]
    return render(request,'rct/public/recetas.html',{'recetas' : listado_recetas},)

def mis_recetas(request):
    return render(request,'rct/public/mis_recetas.html',)

def contact(request):
    return render(request,'rct/public/contact.html',)

def registro(request):
    return render(request,'rct/public/registro.html',)

def login(request):
    return render(request,'rct/public/login.html',)

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