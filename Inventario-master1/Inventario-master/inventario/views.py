from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from .models import Producto, Bodega, Movimiento, DetalleMovimiento, PerfilUsuario, ProductoBodega
from .forms.forms import ProductoForm, BodegaForm, MovimientoForm, RegistroForm, ProductoBodegaForm, DetalleMovimientoForm, BusquedaMovimientoForm
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
def anadir_producto_bodega(request):
    if request.method == 'POST':
        form = ProductoBodegaForm(request.POST)
        if form.is_valid():
            producto_bodega = form.save(commit=False)
            producto = producto_bodega.producto
            bodega = producto_bodega.bodega
            cantidad = producto_bodega.stock

            if producto.cantidad_total >= cantidad:
                producto_bodega.save()
                producto.cantidad_total -= cantidad
                producto.save()
                return redirect('detalle_bodega', bodega_id=bodega.id)
            else:
                # Manejar el caso en el que no hay suficiente stock
                pass
    else:
        form = ProductoBodegaForm()

    return render(request, 'anadir_producto_bodega.html', {'form': form})

@login_required
def realizar_movimiento(request):
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            movimiento = form.save(commit=False)
            movimiento.usuario = request.user

            # Validar que la bodega de origen tiene suficiente stock.
            producto_bodega_origen = ProductoBodega.objects.get(
                bodega=movimiento.bodega_origen, 
                producto=movimiento.producto
            )

            if producto_bodega_origen.stock >= movimiento.cantidad:
                # Realiza la transferencia
                producto_bodega_origen.stock -= movimiento.cantidad
                producto_bodega_origen.save()

                producto_bodega_destino, created = ProductoBodega.objects.get_or_create(
                    bodega=movimiento.bodega_destino, 
                    producto=movimiento.producto
                )
                producto_bodega_destino.stock += movimiento.cantidad
                producto_bodega_destino.save()

                movimiento.save()
                return redirect('historial_movimientos')
            else:
                # No hay suficiente stock. Envía un mensaje de error.
                form.add_error('cantidad', 'No hay suficiente stock en la bodega de origen.')

    else:
        form = MovimientoForm()

    return render(request, 'realizar_movimiento.html', {'form': form})


@login_required
def historial_movimientos(request):
    movimientos = Movimiento.objects.all().order_by('-fecha')
    return render(request, 'historial_movimientos.html', {'movimientos': movimientos})

@login_required
def lista_bodegas(request):
    bodegas = Bodega.objects.all()
    perfil_usuario = get_object_or_404(PerfilUsuario, pk=request.user.id)
    return render(request, 'lista_bodegas.html', {'bodegas': bodegas, 'perfil_usuario': perfil_usuario})

@login_required
def detalle_bodega(request, bodega_id):
    bodega = get_object_or_404(Bodega, pk=bodega_id)
    productos_en_bodega = bodega.producto_bodega.all()
    perfil_usuario = get_object_or_404(PerfilUsuario, pk=request.user.id)
    return render(request, 'detalle_bodega.html', {'bodega': bodega, 'productos_en_bodega': productos_en_bodega , 'perfil_usuario': perfil_usuario})

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
def perfil_usuario(request):
    # Obtener el perfil de usuario para el usuario autenticado o devolver un 404 si no existe
    perfil_usuario = get_object_or_404(PerfilUsuario, pk=request.user.id)

    # Pasar el perfil de usuario a la plantilla
    return render(request, 'profile.html', {'perfil_usuario': perfil_usuario})

def homepage(request):
    return render(request, 'homepage.html')