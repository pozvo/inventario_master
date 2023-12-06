from django.contrib import admin
from .models import Producto, Bodega, Movimiento, DetalleMovimiento, PerfilUsuario

admin.site.register(PerfilUsuario)
admin.site.register(Producto)
admin.site.register(Bodega)
admin.site.register(Movimiento)
admin.site.register(DetalleMovimiento)


# Register your models here.
