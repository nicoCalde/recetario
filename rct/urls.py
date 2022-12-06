from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('recetas',views.recetas,name='recetas'),
    path('mis_recetas',views.mis_recetas,name='mis_recetas'),
    path('contact',views.contact,name='contact'),
]