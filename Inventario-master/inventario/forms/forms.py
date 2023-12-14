from django import forms
from inventario.models import Producto, Bodega, Movimiento, DetalleMovimiento, PerfilUsuario, ProductoBodega
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxValueValidator

class RegistroForm(UserCreationForm):
    username = forms.CharField(max_length=50)
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}))
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar contraseña'}))
    class Meta:
        model = PerfilUsuario
        fields = ('username', 'password1', 'password2', 'rol')

class PerfilUsuarioForm(forms.ModelForm):
    class Meta:
        model = PerfilUsuario
        fields = '__all__'


class ProductoBodegaForm(forms.ModelForm):
    class Meta:
        model = ProductoBodega
        fields = '__all__'

class DetalleMovimientoForm(forms.ModelForm):
    class Meta:
        model = DetalleMovimiento
        fields = ['producto', 'cantidad']

    def __init__(self, bodega_origen_id=None, *args, **kwargs):
        super(DetalleMovimientoForm, self).__init__(*args, **kwargs)
        if bodega_origen_id:
            self.fields['producto'].queryset = Producto.objects.filter(
                bodegas__id=bodega_origen_id)

class ProductoForm(forms.ModelForm): 
    nombre = forms.CharField(max_length=40)
    descripcion = forms.CharField(max_length=400)

    class Meta:
        model = Producto
        fields = ('nombre', 'descripcion' , 'cantidad_total') 

class BusquedaMovimientoForm(forms.Form):
    fecha_desde = forms.DateField(required=False)
    fecha_hasta = forms.DateField(required=False)
    usuario = forms.ModelChoiceField(queryset=PerfilUsuario.objects.all(), required=False)
    bodega = forms.ModelChoiceField(queryset=Bodega.objects.all(), required=False)


class BodegaForm(forms.ModelForm):
    class Meta:
        model = Bodega
        fields = '__all__'

class MovimientoForm(forms.ModelForm):
    class Meta:
        model = Movimiento
        fields = ['bodega_origen', 'bodega_destino']