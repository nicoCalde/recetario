from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Recetas(models.Model):
    nombre_receta = models.CharField(max_length=150,verbose_name='nombre receta')
    imagen_receta = models.ImageField(upload_to='imagenes/', verbose_name='imagen')
    tiempo_prep_receta = models.CharField(max_length=50,verbose_name='tiempo')
    porciones_receta = models.IntegerField(verbose_name='porciones')
    pasos_receta = models.TextField(verbose_name='instrucciones')
    fkuser = models.ForeignKey(User,verbose_name="Usuario", on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre_receta
    
    def get_absolute_url(self):
        return reverse("rct:receta", kwargs={"id": self.id})

    def get_edit_url(self):
        return reverse("rct:editar", kwargs={"id": self.id})

    def get_delete_url(self):
        return reverse("rct:eliminar", kwargs={"id": self.id})

    def get_ingredientes(self):
        return self.ingredientes_set.all()
    
    def delete(self,using=None,keep_parents=False):
        self.imagen_receta.delete(self.imagen_receta.name) # borrado fisico
        super().delete()
        
    
class Productos(models.Model):
    nombre_producto = models.CharField(max_length=150,verbose_name='nombre producto')

    def __str__(self):
        return self.nombre_producto
    
    def get_absolute_url(self):
        return reverse("rct:productos_admin", kwargs={"id": self.id})

class UnidadesDeMedida(models.Model):
    nombre_medida = models.CharField(max_length=150,verbose_name='unidad de medida')

    def __str__(self):
        return self.nombre_medida

    def get_absolute_url(self):
        return reverse("rct:medidas_admin", kwargs={"id": self.id})

class Ingredientes(models.Model):
    fkrecetas = models.ForeignKey(Recetas, verbose_name="Receta", on_delete=models.CASCADE)
    fkproductos = models.ForeignKey(Productos, verbose_name="prodcuto", on_delete=models.CASCADE)
    cantidad = models.FloatField(verbose_name='cantidad')
    fkunidad_medida = models.ForeignKey(UnidadesDeMedida, verbose_name="medida", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.fkrecetas}: {self.fkproductos}, {round(self.cantidad)} {self.fkunidad_medida}'

    def get_absolute_url(self):
        return self.fkrecetas.get_absolute_url()
    
    def get_edit_url(self):
        kwargs={
            "parent_id": self.fkrecetas.id,
            "id": self.id
        }
        return reverse("rct:editar_ingrediente", kwargs=kwargs)

    def get_delete_url(self):
        kwargs={
            "parent_id": self.fkrecetas.id,
            "id": self.id
        }
        return reverse("rct:eliminar_ingrediente", kwargs=kwargs)

class RecetasGuardadas(models.Model):
    receta_guardada = models.ForeignKey(Recetas, verbose_name="receta_guardada", on_delete=models.CASCADE)
    fkuser = models.ForeignKey(User,verbose_name="usuario_guardada", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.fkuser}: {self.receta_guardada}'

    def get_absolute_url(self):
        return self.receta_guardada.get_absolute_url()

    def get_delete_url(self):
        kwargs={
            "parent_id": self.receta_guardada.id,
            "id": self.id
        }
        return reverse("rct:borrar_receta", kwargs=kwargs)

class Messages(models.Model):
    sender = models.ForeignKey(User,verbose_name="sender",related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User,verbose_name="Para",related_name="receiver", on_delete=models.CASCADE,limit_choices_to={'is_staff':True})
    subject = models.CharField(max_length=50,verbose_name='Asunto')
    msg_content = models.TextField(verbose_name='mensaje')
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'De: {self.sender} | Para: {self.receiver} | Fecha: {self.created_at.strftime("%d-%m-%Y")} | Asunto: {self.subject}'
    
    def soft_delete(self):
        self.read=True
        super().save()
    
    def restore(self):
        self.read=False
        super().save()

    #query for views.py: 
    # Inbox: Message.objects.filter(receiver=request.user)
    # Enviados: Message.objects.filter(sender=request.user)