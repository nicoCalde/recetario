# from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from rct.forms import *
from django.contrib import messages
from rct.models import *
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory # model form for querydets

# Create your views here.

#PUBLIC
def index(request):
    return render(request,'rct/public/index.html',)

# content views
def recetas(request):
    recetas = Recetas.objects.all().order_by('nombre_receta')
    return render(request,'rct/public/recetas.html',{'recetas':recetas})

@login_required(login_url='rct:login')
def mis_recetas(request):
    recetas = Recetas.objects.filter(pk=request.user.pk)
    return render(request,'rct/public/mis_recetas.html',{'recetas':recetas})

def receta(request,id=None):
    receta = get_object_or_404(Recetas, id=id)
    return render(request,'rct/public/receta.html',{'receta':receta})

def contact(request):
    if(request.method == 'POST'):
        contacto_form = ContactoForm(request.POST)
        if(contacto_form.is_valid()):
            messages.success(request,'¡Gracias por comunicarte con nostros, te estaremos respondiedo a la brevedad!')
            contacto_form = ContactoForm()
            #enviar un mail al administrador
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
            return redirect('login')
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
            messages.success(request,f'')
            return redirect('rct:index')
        else:
            messages.error(request,'El usuario o la contraseña no son validos')
    form = Logueo()
    return render(request,'rct/public/login.html',{'form':form})

# crud
@login_required(login_url='rct:login')
def crear_receta(request):
    IngredientesFormset = modelformset_factory(Ingredientes,form=IngredientesForm,fields=['fkproductos','cantidad','fkunidad_medida'],extra=0)
    formset = IngredientesFormset()
    if request.method == 'POST':
        formulario1 = RecetasForm(request.POST or None)
        formset = IngredientesFormset(request.POST or None)
        if formulario1.is_valid() and formset.is_valid():
            form1=formulario1.save(commit=False)
            form1.fkuser = request.user
            form1.save()
            for form in formset:
                form2 = form.save(commit=False)                
                form2.fkreceta = form1
                form2.save()
            return redirect('rct:mis_recetas')
    else:
        formulario1 = RecetasForm()
        formset = IngredientesFormset()
    return render(request,'rct/public/crear_receta.html',{'form1':formulario1,'formset':formset})

@login_required(login_url='rct:login')
def editar_receta(request,id=None):
    try:
        receta = Recetas.objects.get(id=id, user=request.user)
    except Recetas.DoesNotExist:
        return render(request,'rct/public/404.html')
    if request.method == 'POST':
        formulario1 = RecetasForm(request.POST,instance=receta)
        IngredientesFormset = modelformset_factory(Ingredientes,fields='__all__',extra=0)
        qs = receta.ingredientes_set.all()
        formset = IngredientesFormset(request.POST,queryset=qs)
        if formulario1.is_valid() and formset.is_valid():
            form1=formulario1.save(commit=False)
            form1.save()
            for form in formset:
                form2 = form.save(commit=False)                
                form2.fkreceta = form1
                form2.save()
            return redirect('rct:mis_recetas')
        else:
            formulario1 = RecetasForm(instance=receta)
            formset = IngredientesFormset(queryset=qs)
    return render(request,'rct/public/editar_receta.html',{'form1':formulario1,'formset':formset})

@login_required(login_url='rct:login')
def eliminar_receta(request,id_receta):
    try:
        receta = Recetas.objects.get(pk=id_receta)
    except Recetas.DoesNotExist:
        return render(request,'rct/public/404.html')
    receta.delete() 
    return redirect('rct:mis_recetas')

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
        formulario = MedidasForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('rct:crear_receta')
    else:
        formulario = MedidasForm()
    return render(request,'rct/public/crear_medida.html',{'formulario':formulario})

#----------------------------------------------------------------------------------------------------------------------------------------

#ADMINISTRACION
def index_administracion(request):
    variable = 'test variable'
    return render(request,'rct/administration/index_administracion.html',{'variable':variable})

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