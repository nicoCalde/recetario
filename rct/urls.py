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
    path('crear_receta',views.crear_receta,name='crear_receta'),
    path('editar_receta',views.editar_receta,name='editar_receta'),
    path('buscar_receta',views.buscar_receta,name='buscar_receta'),
    path('contact',views.contact,name='contact'),
    #ADMINISTRACION
    path('administracion',views.index_administracion,name='index_administracion'),
    path('administracion/login',views.login_administracion,name='login_admin'),
    path('administracion/register',views.register_adminitracion,name='register_admin'),
    path('administracion/forgotpassword',views.forgotpass_administracion,name='forgotpass_admin'),
]