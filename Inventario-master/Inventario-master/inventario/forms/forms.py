from django import forms
from inventario.models import Producto, Bodega, Movimiento, DetalleMovimiento, PerfilUsuario
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxValueValidator

class RegistroForm(UserCreationForm):
    username = forms.CharField(max_length=50)
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar contraseña'}))
    class Meta:
        model = PerfilUsuario
        fields = ('username', 'password1', 'password2', 'rol')

class DetalleMovimientoForm(forms.ModelForm):
    class Meta:
        model = DetalleMovimiento
        fields = '__all__'

class ProductoForm(forms.ModelForm): 
    nombre = forms.CharField(max_length=40)
    descripcion = forms.CharField(max_length=400)

    class Meta:
        model = Producto
        fields = ('nombre', 'descripcion') 


class BodegaForm(forms.ModelForm):
    class Meta:
        model = Bodega
        fields = '__all__'

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ('bodega_origen', 'bodega_destino', 'productos',)