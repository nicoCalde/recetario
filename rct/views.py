# from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

#PUBLIC
def index(request):
    # listado_recetas =
    return render(request,'rct/public/index.html',)#'recetas':listado_recetas )

def recetas(request):
    return render(request,'rct/public/recetas.html',)

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

#ADMINITRACION