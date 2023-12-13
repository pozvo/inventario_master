from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from inventario import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('crear_producto/', views.crear_producto, name='crear_producto'),
    path('crear_movimiento/', views.crear_movimiento, name='crear_movimiento'),
    path('lista_movimientos/', views.lista_movimientos, name='lista_movimientos'),
    path('lista_bodegas/', views.lista_bodegas, name='lista_bodegas'),
    path('detalle_bodega/<int:bodega_id>/', views.detalle_bodega, name='detalle_bodega'),
    path('crear_actualizar_bodega/', views.crear_actualizar_bodega, name='crear_actualizar_bodega'),
    path('crear_actualizar_bodega/<int:bodega_id>/', views.crear_actualizar_bodega, name='actualizar_bodega'),
    path('modificar_bodega/<int:bodega_id>/', views.modificar_bodega, name='modificar_bodega'),
    path('eliminar_bodega/<int:bodega_id>/', views.eliminar_bodega, name='eliminar_bodega'),
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),  # Redirección al login después del logout
    path('register/', views.register, name='register'),
    path('lista_productos/', views.lista_productos, name='lista_productos'),
    path('profile/', views.perfil_usuario, name='perfil_usuario'),
    path('set_session/', views.set_session, name='set_session'), 
    path('get_session/', views.get_session, name='get_session'),  
]