from django.contrib import admin
from rct.models import *

# Register your models here.
# Inlines (tabular & stacked)
class IngredientesAdminInline(admin.TabularInline):
    model = Ingredientes
    fields = ['fkproductos','cantidad','fkunidad_medida']
    extra = 0

# models
class RecetasAdmin(admin.ModelAdmin):
    inlines = [IngredientesAdminInline]
    list_display = ['id', 'nombre_receta', 'porciones_receta', 'tiempo_prep_receta', 'fkuser']
    raw_id_fields = ['fkuser']

admin.site.register(Recetas, RecetasAdmin)
admin.site.register(Ingredientes)
admin.site.register(Productos)
admin.site.register(UnidadesDeMedida)
admin.site.register(RecetasGuardadas)
admin.site.register(Messages)