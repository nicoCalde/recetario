from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

app_name='rct'
urlpatterns = [
    #PUBLIC
    path('',views.index,name='index'),
    path('recetas',views.recetas,name='recetas'),
    path('mis_recetas/',views.mis_recetas,name='mis_recetas'),
    path('mis_recetas/crear_receta',views.crear_receta,name='crear_receta'),
    path('mis_recetas/editar_receta/<int:id>/',views.editar_receta,name='editar'),
    path('mis_recetas/eliminar_receta/<int:id>/',views.eliminar_receta,name='eliminar'),
    path('mis_recetas/crear_receta/crear_producto',views.crear_producto,name='crear_producto'),
    path('mis_recetas/crear_receta/crear_medida',views.crear_medida,name='crear_medida'),
    path('receta/<int:id>/',views.receta,name='receta'),
    path('receta/<int:parent_id>/editar_ingrediente/<int:id>/',views.editar_ingrediente,name='editar_ingrediente'),
    path('receta/<int:parent_id>/eliminar_ingrediente/<int:id>/',views.eliminar_ingrediente,name='eliminar_ingrediente'),
    path('receta/<int:parent_id>/guardar_receta/',views.guardar_receta,name='guardar_receta'),
    path('receta/<int:parent_id>/borrar_receta/<int:id>/',views.borrar_receta,name='borrar_receta'),
    path('registro',views.registro,name='registro'),
    path('login',views.recetas_login,name='login'),
    path('logout',auth_views.LogoutView.as_view(template_name='rct/public/index.html'),name='logout'),
    path('contact',views.contact,name='contact'),
    #ADMINISTRACION
    path('administracion',views.index_administracion,name='administracion'),
    path('administracion/usuarios',views.usuarios,name='usuarios'),
    path('administracion/staff',views.staff,name='staff'),
    path('administracion/recetas',views.recetas_admin,name='recetas_admin'),
    path('administracion/recetas/crear-receta',views.crear_recetas_admin,name='crear_receta_admin'),
    path('administracion/ingredientes',views.ingredientes_admin,name='ingredientes_admin'),
    path('administracion/productos',views.productos_admin,name='productos_admin'),
    path('administracion/productos/crear-producto',views.crear_productos_admin,name='crear_prod_admin'),
    path('administracion/unidades-medida',views.medidas_admin,name='medidas_admin'),
    path('administracion/unidades-medida/crear-medida',views.crear_medidas_admin,name='crear_med_admin'),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)