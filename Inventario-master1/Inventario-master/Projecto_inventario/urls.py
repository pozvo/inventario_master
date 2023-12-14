from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from inventario.views import (
    lista_productos, 
    detalles_producto, 
    crear_producto, 
    actualizar_producto, 
    eliminar_producto,
    anadir_producto_bodega,  # Asegúrate de importar esta vista
    detalle_bodega,
    lista_bodegas,
    crear_actualizar_bodega,
    modificar_bodega,
    eliminar_bodega,
    register,
    perfil_usuario,
    set_session,
    get_session,
    realizar_movimiento,
    historial_movimientos,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('productos/', lista_productos, name='lista_productos'),
    path('productos/<int:pk>/', detalles_producto, name='detalles_producto'),
    path('productos/crear/', crear_producto, name='crear_producto'),
    path('productos/<int:pk>/actualizar/', actualizar_producto, name='actualizar_producto'),
    path('productos/<int:pk>/eliminar/', eliminar_producto, name='eliminar_producto'),
    path('productos/anadir_bodega/', anadir_producto_bodega, name='anadir_producto_bodega'),  # Nueva ruta
    path('movimientos/realizar/', realizar_movimiento, name='realizar_movimiento'),
    path('movimientos/historial/', historial_movimientos, name='historial_movimientos'),
    path('lista_bodegas/', lista_bodegas, name='lista_bodegas'),
    path('detalle_bodega/<int:bodega_id>/', detalle_bodega, name='detalle_bodega'),
    path('crear_actualizar_bodega/', crear_actualizar_bodega, name='crear_actualizar_bodega'),
    path('crear_actualizar_bodega/<int:bodega_id>/', crear_actualizar_bodega, name='actualizar_bodega'),
    path('modificar_bodega/<int:bodega_id>/', modificar_bodega, name='modificar_bodega'),
    path('eliminar_bodega/<int:bodega_id>/', eliminar_bodega, name='eliminar_bodega'),
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', register, name='register'),
    path('profile/', perfil_usuario, name='perfil_usuario'),
    path('set_session/', set_session, name='set_session'),
    path('get_session/', get_session, name='get_session'),
]
