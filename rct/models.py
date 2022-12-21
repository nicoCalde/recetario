from django.db import models

# Create your models here.

# class Usuarios(models.Model):
#     nombre_usuario = models.CharField(max_length=100,verbose_name='nombre_usuario')
#     apellido_usuario = models.CharField(max_length=150,verbose_name='apellido_usuario')
#     email_usuario = models.EmailField(max_length=150,verbose_name='email_usuario')

# class Administradores(models.Model):
#     nombre_adminitrador = models.CharField(max_length=100,verbose_name='nombre_administrador')
#     apellido_administrador = models.CharField(max_length=150,verbose_name='apellido_administrador')
#     email_administrador = models.EmailField(max_length=150,verbose_name='email_administrador')

class Recetas(models.Model):
    nombre_receta = models.CharField(max_length=150,verbose_name='nombre_receta')
    imagen_receta = models.ImageField(upload_to='imagenes/', verbose_name='imagen_receta')
    tiempo_prep_receta = models.DurationField(verbose_name='tiempo')
    porciones_receta = models.IntegerField(verbose_name='porciones')
    pasos_receta = models.TextField(verbose_name='pasos')
    # usuarios
    
class Productos(models.Model):
    nombre_produto = models.CharField(max_length=150,verbose_name='nombre_producto')

class UnidadesDeMedida(models.Model):
    nombre_medida = models.CharField(max_length=150,verbose_name='nombre_medida')

class Ingredientes(models.Model):
    recetas = models.ForeignKey(Recetas, verbose_name="receta_ingrediente", on_delete=models.CASCADE)
    productos = models.ForeignKey(Productos, verbose_name="producto_ingrediente", on_delete=models.CASCADE)
    cantidad = models.IntegerField(verbose_name='cantidad')
    unidad_medida = models.ForeignKey(UnidadesDeMedida, verbose_name="medida_ingresite", on_delete=models.CASCADE)

class RecetasGuardadas(models.Model):
    recetas = models.ForeignKey(Recetas, verbose_name="receta_guardada", on_delete=models.CASCADE)
    # usuarios
