from django.urls import path
from . import views

urlpatterns = [
    #PUBLIC
    path('',views.index,name='index'),
    path('recetas',views.recetas,name='recetas'),
    path('mis_recetas',views.mis_recetas,name='mis_recetas'),
    path('registro',views.registro,name='registro'),
    path('login',views.login,name='login'),
    path('receta',views.receta,name='receta'),
    path('contact',views.contact,name='contact'),
]