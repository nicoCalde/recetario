from rest_framework import viewsets,permissions
from rct.models import Recetas
from api_rct import serializers

# Create your views here.
class RecetasViewSet(viewsets.ModelViewSet):
    queryset=Recetas.objects.all().order_by('id')
    serializer_class=serializers.RecetasSerializer
    permission_classes=[permissions.IsAuthenticatedOrReadOnly]
