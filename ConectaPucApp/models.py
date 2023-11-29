from django.db import models
from django.contrib.auth.models import User

class Forum(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=200, unique=True, )
    descricao = models.TextField(blank=True, null=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Defina o valor padrão como 1 (ou o ID de outro usuário)

    imagem = models.ImageField(upload_to='forum_images/', null=True, blank=True)  # se quiser adicionar uma imagem ao f�rum

    def __str__(self):
        return self.nome
    
    
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

class Postagem(models.Model):
    autor = models.TextField(max_length=200)
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    data_postagem = models.DateTimeField(auto_now_add=True)
    
    # Forum ao qual a postagem pertence
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE, related_name="postagens")

    def __str__(self):
        return self.titulo
    
class Comentario(models.Model):
    autor = models.TextField(max_length=200)
    postagem = models.ForeignKey(Postagem, on_delete=models.CASCADE)  # Substitua "Postagem" pelo nome do seu modelo de postagem
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário por {self.autor} em {self.data_criacao}"

