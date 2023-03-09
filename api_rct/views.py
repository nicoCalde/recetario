from rest_framework import viewsets,permissions
from rct.models import Recetas,Ingredientes
from api_rct import serializers

# Create your views here.
class RecetasViewSet(viewsets.ModelViewSet):
    queryset=Recetas.objects.all().order_by('id')
    serializer_class=serializers.RecetasSerializer
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]


class IngredientesViewSet(viewsets.ModelViewSet):
    queryset=Ingredientes.objects.all().order_by('fkrecetas')
    serializer_class=serializers.IngredientesSerializers
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]