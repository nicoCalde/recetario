from django.urls import path,include
from rest_framework.routers import DefaultRouter
from api_rct import views

router=DefaultRouter()
router.register(r'recetas',views.RecetasViewSet,basename='receta')

urlpatterns = [
    path('',include(router.urls)),
    path('api-auth',include('rest_framework.urls',namespace='rest_framework')),
]
