from rest_framework import serializers
from rct.models import Recetas

class RecetasSerializer(serializers.ModelSerializer):

    class Meta:
        model=Recetas
        fields=['id','nombre_receta','tiempo_prep_receta','porciones_receta','pasos_receta']