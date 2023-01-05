from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    #PUBLIC
    path('',views.index,name='index'),
    path('recetas',views.recetas,name='recetas'),
    path('mis_recetas/',views.mis_recetas,name='mis_recetas'),
    path('registro',views.registro,name='registro'),
    path('login',views.login,name='login'),
    path('receta',views.receta,name='receta'),
    # path('receta/<int:id_receta>',views.receta,name='receta'),
    path('mis_recetas/crear_receta',views.crear_receta,name='crear_receta'),
    path('mis_recetas/editar_receta',views.editar_receta,name='editar_receta'),
    path('mis_recetas/eliminar_receta',views.eliminar_receta,name='eliminar_receta'),
    # path('mis_recetas/editar_receta/<int:id_receta>',views.editar_receta,name='editar_receta'),
    # path('mis_recetas/eliminar_receta/<int:id_receta>',views.eliminar_receta,name='eliminar_receta'),
    path('contact',views.contact,name='contact'),
    #ADMINISTRACION
    path('administracion',views.index_administracion,name='index_administracion'),
    path('administracion/login',views.login_administracion,name='login_admin'),
    path('administracion/register',views.register_adminitracion,name='register_admin'),
    path('administracion/forgotpassword',views.forgotpass_administracion,name='forgotpass_admin'),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)