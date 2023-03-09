from rest_framework import serializers
from rct.models import Recetas,Ingredientes

class RecetasSerializer(serializers.ModelSerializer):

    class Meta:
        model=Recetas
        fields=['id','nombre_receta','tiempo_prep_receta','porciones_receta','pasos_receta','fkuser','created_at','updated_at','public']

class IngredientesSerializers(serializers.ModelSerializer):

    class Meta:
        model=Ingredientes
        fields=['id','fkrecetas','fkproductos','cantidad','fkunidad_medida']