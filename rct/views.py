# from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    # listado_recetas =
    return render(request,'rct/public/index.html',)#'recetas':listado_recetas )

def recetas(request):
    return render(request,'rct/public/recetas.html',)

def mis_recetas(request):
    return render(request,'rct/public/mis_recetas.html',)

def contact(request):
    return render(request,'rct/public/contact.html',)