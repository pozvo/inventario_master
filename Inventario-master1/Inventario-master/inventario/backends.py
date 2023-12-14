from django.contrib.auth.backends import ModelBackend
from inventario.models import PerfilUsuario

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = PerfilUsuario.objects.get(username=username)
            if user.check_password(password):
                return user
        except PerfilUsuario.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return PerfilUsuario.objects.get(pk=user_id)
        except PerfilUsuario.DoesNotExist:
            return None
