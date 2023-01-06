from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Recetas(models.Model):
    nombre_receta = models.CharField(max_length=150,verbose_name='nombre receta')
    imagen_receta = models.ImageField(upload_to='imagenes/', verbose_name='imagen')
    tiempo_prep_receta = models.DurationField(verbose_name='tiempo')
    porciones_receta = models.IntegerField(verbose_name='porciones')
    pasos_receta = models.TextField(verbose_name='instrucciones')
    fkuser = models.ForeignKey(User,verbose_name="usuario_receta", on_delete=models.CASCADE)

    def delete(self,using=None,keep_parents=False):
        self.imagen_receta.delete(self.imagen_receta.name) #borrado fisico
        super().delete()
    
    #chequear metodo para salvar automaticamente el fk user del user que este logueado creando la receta. Clase 25 min 64.
    # def save(self,*args, **kwargs):
    #     self.fkuser = User(id)
    #     super().save(*args, **kwargs)

    
class Productos(models.Model):
    nombre_producto = models.CharField(max_length=150,verbose_name='nombre producto')

class UnidadesDeMedida(models.Model):
    nombre_medida = models.CharField(max_length=150,verbose_name='unidad de medida')

class Ingredientes(models.Model):
    fkrecetas = models.ForeignKey(Recetas, verbose_name="receta_ingrediente", on_delete=models.CASCADE)
    fkproductos = models.ForeignKey(Productos, verbose_name="producto_ingrediente", on_delete=models.CASCADE)
    cantidad = models.IntegerField(verbose_name='cantidad ingrediente')
    fkunidad_medida = models.ForeignKey(UnidadesDeMedida, verbose_name="medida_ingresite", on_delete=models.CASCADE)

class RecetasGuardadas(models.Model):
    receta_guardada = models.ForeignKey(Recetas, verbose_name="receta_guardada", on_delete=models.CASCADE)
    fkuser = models.ForeignKey(User,verbose_name="usuario_guardada", on_delete=models.CASCADE)
