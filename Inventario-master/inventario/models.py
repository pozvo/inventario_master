from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinLengthValidator, MaxLengthValidator


class PerfilUsuario(AbstractUser):
    JEFEBODEGA = 'JF'
    BODEGUERO = 'BD'
    ROLES_USUARIO = [
        (JEFEBODEGA, 'Jefe de Bodega'),
        (BODEGUERO, 'Bodeguero'),
    ]
    rol = models.CharField(max_length=50, choices=ROLES_USUARIO, default=BODEGUERO)

    def es_jefe_bodega(self):
        return self.rol == self.JEFEBODEGA

    def es_bodeguero(self):
        return self.rol == self.BODEGUERO

    groups = models.ManyToManyField(Group, related_name='perfil_usuarios')
    user_permissions = models.ManyToManyField(Permission, related_name='perfil_usuarios')

class Bodega(models.Model):
    nombre = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50, default='Valor predeterminado')
    jefe_bodega = models.ForeignKey(PerfilUsuario, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre

    def stock_producto(self, producto):
        # Actualizar para usar el nuevo modelo ProductoBodega
        relacion = self.producto_bodega.filter(producto=producto).first()
        return relacion.stock if relacion else 0


class Producto(models.Model):
    nombre = models.CharField(
        max_length=50,
        validators=[
            MinLengthValidator(1),
            MaxLengthValidator(50),
        ]
    )
    descripcion = models.TextField(
        validators=[
            MaxLengthValidator(400),
        ]
    )
    cantidad_total = models.IntegerField(default=0)  # Campo añadido

    def __str__(self):
        return self.nombre.lower()
    
class ProductoBodega(models.Model):
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE, related_name='producto_bodega')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='bodega_producto')
    stock = models.IntegerField(default=0)

    class Meta:
        unique_together = ('bodega', 'producto')

    def __str__(self):
        return f"{self.producto.nombre} en {self.bodega.nombre} - Stock: {self.stock}"

class Movimiento(models.Model):
    bodega_origen = models.ForeignKey(Bodega, on_delete=models.CASCADE, related_name='movimientos_salida')
    bodega_destino = models.ForeignKey(Bodega, on_delete=models.CASCADE, related_name='movimientos_entrada')
    productos = models.ManyToManyField(Producto, through='DetalleMovimiento')
    usuario = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

class DetalleMovimiento(models.Model):
    movimiento = models.ForeignKey(Movimiento, on_delete=models.CASCADE, blank=True, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=0)