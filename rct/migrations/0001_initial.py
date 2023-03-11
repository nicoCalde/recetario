# Generated by Django 3.2.14 on 2023-03-09 22:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Productos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_producto', models.CharField(max_length=150, verbose_name='nombre producto')),
            ],
        ),
        migrations.CreateModel(
            name='Recetas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_receta', models.CharField(max_length=150, verbose_name='nombre receta')),
                ('imagen_receta', models.ImageField(upload_to='imagenes/', verbose_name='imagen')),
                ('tiempo_prep_receta', models.CharField(max_length=50, verbose_name='tiempo')),
                ('porciones_receta', models.IntegerField(verbose_name='porciones')),
                ('pasos_receta', models.TextField(verbose_name='instrucciones')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('public', models.BooleanField(default=True, verbose_name='Publica')),
                ('fkuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
        ),
        migrations.CreateModel(
            name='UnidadesDeMedida',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_medida', models.CharField(max_length=150, verbose_name='unidad de medida')),
            ],
        ),
        migrations.CreateModel(
            name='RecetasGuardadas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fkuser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='usuario_guardada')),
                ('receta_guardada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rct.recetas', verbose_name='receta_guardada')),
            ],
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=50, verbose_name='Asunto')),
                ('msg_content', models.TextField(verbose_name='mensaje')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('read', models.BooleanField(default=False, verbose_name='Leido')),
                ('receiver', models.ForeignKey(limit_choices_to={'is_staff': True}, on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL, verbose_name='Para')),
                ('sender', models.ForeignKey(limit_choices_to={'is_staff': True}, on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL, verbose_name='sender')),
            ],
        ),
        migrations.CreateModel(
            name='Ingredientes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.FloatField(verbose_name='cantidad')),
                ('fkproductos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rct.productos', verbose_name='prodcuto')),
                ('fkrecetas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rct.recetas', verbose_name='Receta')),
                ('fkunidad_medida', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rct.unidadesdemedida', verbose_name='medida')),
            ],
        ),
    ]