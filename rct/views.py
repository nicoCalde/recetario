# from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from rct.forms import *
from django.contrib import messages
from rct.models import *
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory # model form for querysets
from django.core.mail import send_mail
from django.db import IntegrityError

# Create your views here.

#PUBLIC
def index(request):
    return render(request,'rct/public/index.html',)

# content views
def recetas(request):
    recetas = Recetas.objects.all()
    archivo = None
    if  request.user.is_authenticated:
        archivo = RecetasGuardadas.objects.filter(fkuser=request.user)
    return render(request,'rct/public/recetas.html',{'recetas':recetas,'archivo':archivo})

@login_required(login_url='rct:login')
def mis_recetas(request):
    recetas = Recetas.objects.filter(fkuser=request.user)
    archivo = RecetasGuardadas.objects.filter(fkuser=request.user)
    return render(request,'rct/public/mis_recetas.html',{'recetas':recetas,'archivo':archivo})

def receta(request,id=None):
    receta = get_object_or_404(Recetas,id=id)
    ingredientes = Ingredientes.objects.filter(fkrecetas=id)
    archivo = None
    if  request.user.is_authenticated:
        try:
            archivo = RecetasGuardadas.objects.get(receta_guardada=id,fkuser=request.user)
        except RecetasGuardadas.DoesNotExist:
            archivo = None
    return render(request,'rct/public/receta.html',{'receta':receta,'ingredientes':ingredientes,'archivo':archivo})

def contact(request):
    if request.method == 'POST':
        contacto_form = ContactoForm(request.POST or None)
        if contacto_form.is_valid():
            email=contacto_form.cleaned_data['email']
            asunto=contacto_form.cleaned_data['asunto']
            nombre=contacto_form.cleaned_data['nombre']
            mensaje=contacto_form.cleaned_data['mensaje']
            data={
                'email': email,
                'asunto': asunto,
                'nombre': nombre,
                'mensaje': mensaje,
            }
            message='''
            De: {}

            Nombre: {}

            Mensaje: {}
            '''.format(data['email'],data['nombre'],data['mensaje'])
            send_mail(data['asunto'],message,'calde_kpo@hotmail.com',['calde_kpo@hotmail.com'])
            messages.success(request,'¡Gracias por comunicarte con nostros, te estaremos respondiedo a la brevedad!')
            contacto_form = ContactoForm()
            return redirect('rct:contact')
    else:
        contacto_form = ContactoForm()

    return render(request,'rct/public/contact.html',{'contacto_form':contacto_form})

# login
def registro(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request, f'Tu cuenta fue creada con exito!')
            return redirect('rct:login')
    else:
        register_form = RegisterForm()
    return render(request,'rct/public/registro.html',{'register_form':register_form})

def recetas_login(request):
    if request.method == 'POST':
        username= request.POST['username']
        password= request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            form = login(request, user)
            messages.success(request,f' ')
            return redirect('rct:index')
        else:
            messages.error(request,'El usuario o la contraseña no son validos')
    form = Logueo()
    return render(request,'rct/public/login.html',{'form':form})

# crud
@login_required(login_url='rct:login')
def crear_receta(request):
    IngredientesFormset = modelformset_factory(Ingredientes, form=IngredientesForm, fields=['fkproductos','cantidad','fkunidad_medida'], extra=0)
    qs = Ingredientes.objects.filter(fkrecetas=None)
    if request.method=='POST':
        formulario = RecetasForm(request.POST or None,request.FILES or None)
        formset = IngredientesFormset(request.POST or None)
        if all([formulario.is_valid(), formset.is_valid()]):
            form=formulario.save(commit=False)
            form.fkuser=request.user
            form.save()
            try:
                for field in formset:
                    forms = field.save(commit=False)
                    forms.fkrecetas = form
                    forms.save()
                    return redirect('rct:mis_recetas')
            except IntegrityError:
                messages.error(request,'El ingrediente no puede estar vacio, completalo o eliminalo para guardar.')
                return render(request,'rct/public/crear_receta.html',{'formulario':formulario,'formset':formset}) 
    else:
        formulario = RecetasForm()
        formset = IngredientesFormset(queryset=qs)
    return render(request,'rct/public/crear_receta.html',{'formulario':formulario,'formset':formset})

@login_required(login_url='rct:login')
def editar_receta(request,id=None):
    obj = get_object_or_404(Recetas, id=id)
    IngredientesFormset = modelformset_factory(Ingredientes,form=IngredientesForm,fields=['fkproductos','cantidad','fkunidad_medida'],extra=0)
    qs = obj.ingredientes_set.all()
    if request.method=='POST':
        formulario = RecetasForm(request.POST or None,request.FILES or None,instance=obj)
        formset = IngredientesFormset(request.POST or None,queryset=qs)
        if all([formulario.is_valid(), formset.is_valid()]):
            form = formulario.save(commit=False)
            form.save()
            try:
                for field in formset:
                    forms = field.save(commit=False)
                    forms.fkrecetas = form
                    forms.save()
                return redirect('rct:mis_recetas')
            except IntegrityError:
                messages.error(request,'El ingrediente no puede estar vacio, completalo o eliminalo para guardar.')
                return render(request,'rct/public/editar_receta.html',{'receta':obj,'formulario':formulario,'formset':formset})
    else:
        formulario = RecetasForm(instance=obj)
        formset = IngredientesFormset(queryset=qs)
    return render(request,'rct/public/editar_receta.html',{'receta':obj,'formulario':formulario,'formset':formset})

@login_required(login_url='rct:login')
def editar_ingrediente(request,parent_id=None,id=None):
    ingrediente = get_object_or_404(Ingredientes,fkrecetas=parent_id,id=id)
    if request.method == 'POST':
        formulario = IngredientesForm(request.POST or None, instance=ingrediente)
        if formulario.is_valid():
            formulario.save()
            success_url = reverse('rct:receta', kwargs={'id':parent_id})
            return redirect(success_url)
    else:
        formulario = IngredientesForm(instance=ingrediente)
    return render(request,'rct/public/editar_ingrediente.html',{'formulario':formulario})

@login_required(login_url='rct:login')
def eliminar_receta(request,id=None):
    try:
        receta = Recetas.objects.get(id=id)
    except Recetas.DoesNotExist:
        return render(request,'rct/public/404.html')
    receta.delete() 
    return redirect('rct:mis_recetas')

@login_required(login_url='rct:login')
def eliminar_ingrediente(request,parent_id=None,id=None):
    ingrediente = get_object_or_404(Ingredientes,fkrecetas=parent_id,id=id)
    ingrediente.delete()
    success_url = reverse('rct:receta', kwargs={'id':parent_id})
    return redirect(success_url)

@login_required(login_url='rct:login')
def crear_producto(request):
    if request.method=='POST':
        formulario = ProductosForm(request.POST or None)
        if formulario.is_valid():
            formulario.save()
            return redirect('rct:crear_receta')
    else:
        formulario = ProductosForm()
    return render(request,'rct/public/crear_producto.html',{'formulario':formulario})

@login_required(login_url='rct:login')
def crear_medida(request):
    if request.method=='POST':
        formulario = MedidasForm(request.POST or None)
        if formulario.is_valid():
            formulario.save()
            return redirect('rct:crear_receta')
    else:
        formulario = MedidasForm()
    return render(request,'rct/public/crear_medida.html',{'formulario':formulario})

@login_required(login_url='rct:login')
def guardar_receta(request,parent_id=None):
    recetas = Recetas.objects.all()
    archivo = RecetasGuardadas.objects.all()
    receta = get_object_or_404(Recetas,id=parent_id)
    if request.method=='POST':
        formulario = RecetasGuardadasForm(request.POST or None)
        if formulario.is_valid():
            form = formulario.save(commit=False)
            form.fkuser = request.user
            form.receta_guardada = receta
            form.save()
            return redirect('rct:mis_recetas')
    else:
        formulario = RecetasGuardadasForm()
    return render(request,'rct/public/guardar_receta.html',{'receta':receta,'formulario':formulario,'recetas':recetas,'archivo':archivo})

@login_required(login_url='rct:login')
def borrar_receta(request,parent_id=None,id=None):
    receta = get_object_or_404(RecetasGuardadas,receta_guardada=parent_id,id=id,fkuser=request.user)
    receta.delete()
    return redirect('rct:mis_recetas')

#----------------------------------------------------------------------------------------------------------------------------------------

#ADMINISTRACION
#Retrieve
@login_required(login_url='rct:login')
def index_administracion(request):
    return render(request,'rct/administration/index_administracion.html')

@login_required(login_url='rct:login')
def usuarios(request):
    usuarios = User.objects.all()
    return render(request,'rct/administration/users.html',{'usuarios':usuarios})

@login_required(login_url='rct:login')
def staff(request):
    usuarios = User.objects.all()
    return render(request,'rct/administration/staff.html',{'usuarios':usuarios})

@login_required(login_url='rct:login')
def recetas_admin(request):
    recetas = Recetas.objects.all()
    return render(request,'rct/administration/recetas_admin.html',{'recetas':recetas})

@login_required(login_url='rct:login')
def pasos_receta_admin(request,id=None):
    receta = get_object_or_404(Recetas,id=id)
    return render(request,'rct/administration/instrucciones.html',{'receta':receta})

@login_required(login_url='rct:login')
def ingredientes_receta_admin(request,parent_id=None):
    ingredientes = Ingredientes.objects.filter(fkrecetas=parent_id)
    receta = get_object_or_404(Recetas,id=parent_id)
    return render(request,'rct/administration/ingredientes_receta.html',{'ingredientes':ingredientes,'receta':receta})

@login_required(login_url='rct:login')
def ingredientes_admin(request):
    ingredientes = Ingredientes.objects.all()
    return render(request,'rct/administration/ingredientes_admin.html',{'ingredientes':ingredientes})

@login_required(login_url='rct:login')
def productos_admin(request):
    productos = Productos.objects.all()
    return render(request,'rct/administration/productos_admin.html',{'productos':productos})

@login_required(login_url='rct:login')
def medidas_admin(request):
    medidas = UnidadesDeMedida.objects.all()
    return render(request,'rct/administration/medidas_admin.html',{'medidas':medidas})

#Create
@login_required(login_url='rct:login')
def crear_recetas_admin(request):
    IngredientesFormset = modelformset_factory(Ingredientes, form=IngredientesForm, fields=['fkproductos','cantidad','fkunidad_medida'], extra=0)
    qs = Ingredientes.objects.filter(fkrecetas=None)
    if request.method=='POST':
        formulario = RecetasForm(request.POST or None,request.FILES or None)
        formset = IngredientesFormset(request.POST or None)
        if all([formulario.is_valid(), formset.is_valid()]):
            form=formulario.save(commit=False)
            form.fkuser=request.user
            form.save()
            try:
                for field in formset:
                    forms = field.save(commit=False)
                    forms.fkrecetas = form
                    forms.save()
                    return redirect('rct:recetas_admin')
            except IntegrityError:
                messages.error(request,'El ingrediente no puede estar vacio, completalo o eliminalo para guardar.')
                return render(request,'rct/public/crear_receta_admin.html',{'formulario':formulario,'formset':formset}) 
    else:
        formulario = RecetasForm()
        formset = IngredientesFormset(queryset=qs)
    return render(request,'rct/administration/crear_receta_admin.html',{'formulario':formulario,'formset':formset})

@login_required(login_url='rct:login')
def crear_ingredientes_receta_admin(request,parent_id=None):
    receta = get_object_or_404(Recetas,id=parent_id)
    if request.method == 'POST':
        formulario = IngredientesForm(request.POST or None)
        if formulario.is_valid():
            form = formulario.save(commit=False)
            form.fkrecetas = receta
            form.save()
            success_url = reverse('rct:ingredientes_receta_admin', kwargs={'parent_id':parent_id})
            return redirect(success_url)
    else:
        formulario = IngredientesForm()
    return render(request,'rct/administration/crear_ing_rec.html',{'formulario':formulario,'receta':receta})

@login_required(login_url='rct:login')
def crear_productos_admin(request):
    if request.method=='POST':
        formulario = ProductosForm(request.POST or None)
        if formulario.is_valid():
            formulario.save()
            return redirect('rct:productos_admin')
    else:
        formulario = ProductosForm()
    return render(request,'rct/administration/crear_producto_admin.html',{'formulario':formulario})

@login_required(login_url='rct:login')
def crear_medidas_admin(request):
    if request.method=='POST':
        formulario = MedidasForm(request.POST or None)
        if formulario.is_valid():
            formulario.save()
            return redirect('rct:medidas_admin')
    else:
        formulario = MedidasForm()
    return render(request,'rct/administration/crear_medida_admin.html',{'formulario':formulario})

#Update
@login_required(login_url='rct:login')
def editar_recetas_admin(request,id=None):
    obj = get_object_or_404(Recetas, id=id)
    IngredientesFormset = modelformset_factory(Ingredientes,form=IngredientesForm,fields=['fkproductos','cantidad','fkunidad_medida'],extra=0)
    qs = obj.ingredientes_set.all()
    if request.method=='POST':
        formulario = RecetasForm(request.POST or None,request.FILES or None,instance=obj)
        formset = IngredientesFormset(request.POST or None,queryset=qs)
        if all([formulario.is_valid(), formset.is_valid()]):
            form = formulario.save(commit=False)
            form.save()
            try:
                for field in formset:
                    forms = field.save(commit=False)
                    forms.fkrecetas = form
                    forms.save()
                return redirect('rct:recetas_admin')
            except IntegrityError:
                messages.error(request,'El ingrediente no puede estar vacio, completalo o eliminalo para guardar.')
                return render(request,'rct/administration/editar_receta_admin.html',{'receta':obj,'formulario':formulario,'formset':formset})
    else:
        formulario = RecetasForm(instance=obj)
        formset = IngredientesFormset(queryset=qs)
    return render(request,'rct/administration/editar_receta_admin.html',{'receta':obj,'formulario':formulario,'formset':formset})

@login_required(login_url='rct:login')
def editar_ingredientes_receta_admin(request,parent_id=None,id=None):
    receta = get_object_or_404(Recetas,id=parent_id)
    ingrediente = get_object_or_404(Ingredientes,fkrecetas=parent_id,id=id)
    if request.method == 'POST':
        formulario = IngredientesForm(request.POST or None,instance=ingrediente)
        if formulario.is_valid():
            form = formulario.save(commit=False)
            form.fkrecetas = receta
            form.save()
            success_url = reverse('rct:ingredientes_receta_admin', kwargs={'parent_id':parent_id})
            return redirect(success_url)
    else:
        formulario = IngredientesForm(instance=ingrediente)
    return render(request,'rct/administration/editar_ing_rec.html',{'formulario':formulario,'receta':receta})

@login_required(login_url='rct:login')
def editar_productos_admin(request,id=None):
    obj = get_object_or_404(Productos, id=id)
    if request.method=='POST':
        formulario = ProductosForm(request.POST or None,instance=obj)
        if formulario.is_valid():
            formulario.save()
            return redirect('rct:productos_admin')
    else:
        formulario = ProductosForm(instance=obj)
    return render(request,'rct/administration/editar_producto_admin.html',{'producto':obj,'formulario':formulario})

@login_required(login_url='rct:login')
def editar_medidas_admin(request,id=None):
    obj = get_object_or_404(UnidadesDeMedida, id=id)
    if request.method=='POST':
        formulario = MedidasForm(request.POST or None,instance=obj)
        if formulario.is_valid():
            formulario.save()
            return redirect('rct:medidas_admin')
    else:
        formulario = MedidasForm(instance=obj)
    return render(request,'rct/administration/editar_medida_admin.html',{'medida':obj,'formulario':formulario})

#Delete
@login_required(login_url='rct:login')
def eliminar_recetas_admin(request,id=None):
    receta = get_object_or_404(Recetas, id=id)
    receta.delete() 
    return redirect('rct:recetas_admin')

@login_required(login_url='rct:login')
def eliminar_ingredientes_receta_admin(request,parent_id=None,id=None):
    ingrediente = get_object_or_404(Ingredientes,fkrecetas=parent_id,id=id)
    ingrediente.delete()
    success_url = reverse('rct:ingredientes_receta_admin', kwargs={'parent_id':parent_id})
    return redirect(success_url)

@login_required(login_url='rct:login')
def eliminar_productos_admin(request,id=None):
    receta = get_object_or_404(Productos, id=id)
    receta.delete() 
    return redirect('rct:productos_admin')

@login_required(login_url='rct:login')
def eliminar_medidas_admin(request,id=None):
    receta = get_object_or_404(UnidadesDeMedida, id=id)
    receta.delete() 
    return redirect('rct:medidas_admin')
