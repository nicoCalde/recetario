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
                return render(request,'rct/public/editar_receta.html',{'formulario':formulario,'formset':formset}) 
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
        formulario = ProductosForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('rct:crear_receta')
    else:
        formulario = ProductosForm()
    return render(request,'rct/public/crear_producto.html',{'formulario':formulario})

@login_required(login_url='rct:login')
def crear_medida(request):
    if(request.method=='POST'):
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
@login_required(login_url='rct:login')
def index_administracion(request):
    return render(request,'rct/administration/index_administracion.html')

def register_adminitracion(request):
    if(request.method == 'POST'):
        register_form = AdminRegisterForm(request.POST)
        if(register_form.is_valid()):
            #enviar email al administrador con los datos que recibio y guardar los datos en la base de datos
            #enviarle al usuario alguna respuesta
            pass
    else:
        register_form = AdminRegisterForm()
    return render(request,'rct/administration/register_administracion.html',{'register_form':register_form})

def login_administracion(request):
    if(request.method == 'POST'):
        login_form = AdminLoginForm(request.POST)
        if(login_form.is_valid()):
            pass
        else:
            messages.error(request,'El email y/o la contraseña no son validos')
    else:
        login_form = AdminLoginForm()
    return render(request,'rct/administration/login_administracion.html',{'login_form':login_form})

def forgotpass_administracion(request):
    if(request.method == 'POST'):
        reset_form = AdminResetForm(request.POST)
        if(reset_form.is_valid()):
            pass
        else:
            messages.error(request,'El email ingresado no es valido.')
    else:
        reset_form = AdminResetForm()
    return render(request,'rct/administration/forgotpass_administracion.html',{'reset_form':reset_form})