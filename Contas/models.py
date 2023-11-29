from django.db import models

# Create your models here.
class User(models.Model):
    # username
    # first_name
    # last_name
    # email
    # password
    # groups
    # user_permissions
    # is_staff
    # is_active
    # is_superuser
    # last_login
    # date_joined

    # is_authenticated
    # is_anonymous
    pass


class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    foto_perfil = models.ImageField(upload_to='perfil/', blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    biografia = models.TextField(blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    banido = models.BooleanField(default=False)

    def __str__(self):
        return self.usuario.username