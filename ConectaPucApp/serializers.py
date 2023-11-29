from rest_framework import serializers
from ConectaPucApp.models import Forum
from ConectaPucApp.models import PerfilUsuario
from ConectaPucApp.models import Postagem
from ConectaPucApp.models import Comentario

class ConectaPucSerializer: 
    class Forum(serializers.ModelSerializer):
        class Meta:
            model = Forum # nome do modelo
            fields = '__all__' # lista de campos


    class Usuario(serializers.ModelSerializer):
        class Meta:
            model = PerfilUsuario # nome do modelo
            fields = '__all__' # lista de campos


    class Postagem(serializers.ModelSerializer):
        class Meta:
            model = Postagem # nome do modelo
            fields = '__all__' # lista de campos

    class PostagemUpdate(serializers.ModelSerializer):
        class Meta:
            model = Postagem
            fields = ["titulo", "conteudo"]


    class Comentario(serializers.ModelSerializer):
        class Meta:
            model = Comentario
            fields = "__all__"


    class ComentarioCreate(serializers.ModelSerializer):
        class Meta:
            model = Comentario # nome do modelo
            fields = ["autor", "postagem", "texto"] # lista de campos


    class ComentarioUpdate(serializers.ModelSerializer):
        class Meta:
            model = Comentario
            fields = ["texto"]
        