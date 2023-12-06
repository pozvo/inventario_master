from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Producto, Bodega, Movimiento, DetalleMovimiento, PerfilUsuario
from .forms.forms import ProductoForm, BodegaForm, MovimientoForm, RegistroForm
from django.views.decorators.http import require_POST
from django.http import HttpResponse


def register(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'register.html', {'form': form})

@login_required
def set_session(request):
    request.session['nombre_usuario'] = 'ejemplo_usuario'
    return HttpResponse("Valor de la sesión establecido.")

@login_required
def get_session(request):
    nombre_usuario = request.session.get('nombre_usuario', 'Invitado')
    return HttpResponse(f"Valor de la sesión: {nombre_usuario}")

@login_required 
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'lista_productos.html', {'productos': productos})

@login_required
def detalles_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'detalles_producto.html', {'producto': producto})

@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'crear_producto.html', {'form': form})

@login_required
def actualizar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'actualizar_producto.html', {'form': form , 'producto': producto})

@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    return render(request, 'eliminar_producto.html', {'producto': producto})


@login_required
def lista_bodegas(request):
    bodegas = Bodega.objects.all()
    perfil_usuario = get_object_or_404(PerfilUsuario, pk=request.user.id)
    return render(request, 'lista_bodegas.html', {'bodegas': bodegas, 'perfil_usuario': perfil_usuario})

@login_required
def detalle_bodega(request, bodega_id):
    bodega = get_object_or_404(Bodega, pk=bodega_id)
    productos = bodega.productos.all()
    perfil_usuario = get_object_or_404(PerfilUsuario, pk=request.user.id)
    return render(request, 'detalle_bodega.html', {'bodega': bodega, 'productos': productos, 'perfil_usuario': perfil_usuario})

@login_required
def crear_actualizar_bodega(request, bodega_id=None):
    if bodega_id:
        # Actualizar una bodega existente
        bodega = get_object_or_404(Bodega, pk=bodega_id)
        form = BodegaForm(instance=bodega)
    else:
        # Crear una nueva bodega
        form = BodegaForm()

    if request.method == 'POST':
        if bodega_id:
            # Actualizar una bodega existente
            form = BodegaForm(request.POST, instance=bodega)
        else:
            # Crear una nueva bodega
            form = BodegaForm(request.POST)

        if form.is_valid():
            bodega = form.save(commit=False)
            bodega.jefe_bodega = request.user
            bodega.save()
            return redirect('lista_bodegas')

    perfil_usuario = get_object_or_404(PerfilUsuario, pk=request.user.id)
    return render(request, 'crear_actualizar_bodega.html', {'form': form, 'perfil_usuario': perfil_usuario})

@login_required
def modificar_bodega(request, bodega_id):
    bodega = get_object_or_404(Bodega, id=bodega_id)

    if request.method == 'POST':
        form = BodegaForm(request.POST, instance=bodega)
        if form.is_valid():
            form.save()
            return redirect('lista_bodegas')  
    else:
        form = BodegaForm(instance=bodega)

    return render(request, 'modificar_bodega.html', {'form': form, 'bodega': bodega})

@login_required
def eliminar_bodega(request, bodega_id):
    bodega = get_object_or_404(Bodega, id=bodega_id)

    if request.method == 'POST':
        bodega.delete()
        return redirect('lista_bodegas')  

    return render(request, 'eliminar_bodega.html', {'bodega': bodega})


@login_required
def crear_movimiento(request):
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.usuario = request.user
            movimiento.save()
            form.save_m2m()
            return redirect('lista_movimientos')
    else:
        form = MovimientoForm()

    perfil_usuario = get_object_or_404(PerfilUsuario, pk=request.user.id)

    return render(request, 'crear_movimiento.html', {'form': form, 'perfil_usuario': perfil_usuario})

@login_required
def lista_movimientos(request):
    movimientos = Movimiento.objects.all()
    perfil_usuario = get_object_or_404(PerfilUsuario, pk=request.user.id)
    return render(request, 'lista_movimientos.html', {'movimientos': movimientos, 'perfil_usuario': perfil_usuario})


@login_required
def perfil_usuario(request):
    # Obtener el perfil de usuario para el usuario autenticado o devolver un 404 si no existe
    perfil_usuario = get_object_or_404(PerfilUsuario, pk=request.user.id)

    # Pasar el perfil de usuario a la plantilla
    return render(request, 'profile.html', {'perfil_usuario': perfil_usuario})

def homepage(request):
    return render(request, 'homepage.html')