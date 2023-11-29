from django.http import Http404
from ConectaPucApp.serializers import ConectaPucSerializer
from rest_framework.views import APIView
from django.views.generic import TemplateView
from .models import Postagem, Forum, Comentario
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import permission_classes
from rest_framework.decorators import authentication_classes

# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.autor == request.user
    

class IsAdminUserOrReadOnly(permissions.BasePermission): # Classe para permissao de adm
    def has_permission(self, request, view):
        # Apenas administradores podem criar fóruns
        if request.method == 'POST' and not request.user.is_staff:
            return False
        return True

    
class ForumListView(APIView):
    @swagger_auto_schema(
        operation_summary="Lista todos os foruns",
        operation_description="Obter informações sobre todos os foruns",
        responses={200: ConectaPucSerializer.Forum(many=True)}
    )
    def get(self, request):
        forums = Forum.objects.all().order_by('nome')
        serializer = ConectaPucSerializer.Forum(forums, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ForumUpdateView(APIView):
    @swagger_auto_schema(
            operation_summary="Atualiza Fórum", operation_description="Atualiza as informações do Fórum",
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'nome': openapi.Schema(description="Atualiza Nome do Fórum", type=openapi.TYPE_STRING),
                    'descricao' : openapi.Schema(description="Atualiza Descrição do Fórum", type=openapi.TYPE_STRING)
                },
            ),
            responses={200:ConectaPucSerializer.Forum(), 
                       400:ConectaPucSerializer.Forum()},
            manual_parameters=[
                openapi.Parameter('id_arg', openapi.IN_PATH, default=41, type=openapi.TYPE_INTEGER,
                                  required=True, description='id do fórum na URL',
                ),
            ],
    )
    def put(self, request, pk):
        forum = self.get_forum(pk)

        serializer = ConectaPucSerializer.Forum(forum, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_forum(self, pk):
        try:
            return Forum.objects.get(pk=pk)
        except Forum.DoesNotExist:
            raise Http404
        

class ForumCreateView(APIView):#Criar forum
    @swagger_auto_schema(
        operation_summary="Criar Forum",
        operation_description="Criar um Forum novo",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "nome" : openapi.Schema(description="Título do Fórum", type=openapi.TYPE_STRING),
                "descricao" : openapi.Schema(description="Descreve o intuito do fórum", type=openapi.TYPE_STRING)
            }
        ),
        responses={201: ConectaPucSerializer.Forum()},


    )
    def post(self, request):
        serializer = ConectaPucSerializer.Forum(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForumDeleteView(APIView):
    # permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

    @swagger_auto_schema(
            operation_description='Remove um Fórum',
            request_body=None,
            # ConectaPucSerializer.ConectaPucForumSerializer(),
            responses={
                204: ConectaPucSerializer.Forum(),
                404: None,
            },
    )
    def delete(self, request, pk=None):
        try:
            forum = Forum.objects.get(id=pk)
            forum.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Forum.DoesNotExist:
            return Response({'error': f'Fórum(s) com ID(s) [{pk}] não encontrado(s)'}, 
                            status=status.HTTP_404_NOT_FOUND)
        

class PostagemListView(APIView):#Ver postagem
    @swagger_auto_schema(
        operation_summary="Lista todos as postagens",
        operation_description="Obter informações sobre todas as postagens",
        request_body=None, #opcional
        responses={200: ConectaPucSerializer.Postagem()}
    )
    def get(self, request):
        postagens = Postagem.objects.all().order_by('data_postagem')
        serializer = ConectaPucSerializer.Postagem(postagens, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class PostagemCreateView(APIView):
    @swagger_auto_schema(
        operation_summary="Criar Postagem",
        operation_description="Criar uma nova postagem",
        request_body = openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "forum" : openapi.Schema(description="Id do Fórum", type=openapi.TYPE_INTEGER),
                "titulo" : openapi.Schema(description="Título da Postagem", type=openapi.TYPE_STRING),
                "conteudo" : openapi.Schema(description="Conteúdo da Postagem", type=openapi.TYPE_STRING),
                "autor" : openapi.Schema(description="Autor da Postagem", type=openapi.TYPE_STRING),
            }
        ),
        responses={201: ConectaPucSerializer.Postagem()}
    )
    def post(self, request): #Adiciona postagem
        serializer = ConectaPucSerializer.Postagem(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PostagemUpdateView(APIView):
    @swagger_auto_schema(
            operation_summary="Atualiza Postagem", operation_description="Atualiza título e Conteúdo da Postagem",
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'titulo' : openapi.Schema(description="Atualiza o título da postagem.", type=openapi.TYPE_STRING),
                    'conteudo' : openapi.Schema(description="Atualiza o conteúdo da postagem.", type=openapi.TYPE_STRING),
                },
            ),
            responses={200:ConectaPucSerializer.Postagem(),
                       400:ConectaPucSerializer.Postagem()},
            # manual_parameters=[
            #     openapi.Parameter("id_usuario", openapi.IN_PATH, default=, type=openapi.TYPE_INTEGER,
            #                       required=True, description="id do usuário responsável pela postagem.",
            #                 ),
            # ],
    )
    def put(self, request, pk):
        postagem = self.get_postagem(pk)
        
        # Verifique se o usuário é o autor da postagem

        serializer = ConectaPucSerializer.PostagemUpdate(postagem, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_postagem(self, pk):
        try:
            return Postagem.objects.get(pk=pk)
        except Postagem.DoesNotExist:
            raise Http404
        

class PostagemDeleteView(APIView):
    @swagger_auto_schema(
            operation_summary="Remove uma postagem",
            operation_description="Remove uma postagem.",
            request_body=None,
            responses={
                204: ConectaPucSerializer.Postagem(),
                404: None,
            },
    )

    def delete(self, request, pk=None):
        try:
            postagem = Postagem.objects.get(id=pk)
            postagem.delete()
            return Response({'message' : "Postagem excluída com sucesso."}, status=status.HTTP_204_NO_CONTENT)

        except Postagem.DoesNotExist:
            return Response({'error': f'Postagem com ID [{pk}] não foi encontrada'},
                            status=status.HTTP_404_NOT_FOUND)

    
class ComentarioListView(APIView): #Lista comentarios
    @swagger_auto_schema(
        operation_summary="Lista todos os comentários",
        operation_description="Obter informações sobre todos os comentários",
        request_body=None, #opcional
        responses={200: ConectaPucSerializer.Comentario()}
    )
    def get(self, request, postagem_id):
        comentarios = Comentario.objects.filter(postagem__id=postagem_id).order_by('data_criacao')
        serializer = ConectaPucSerializer.Comentario(comentarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ComentarioCreateView(APIView): #cria comentarios
    @swagger_auto_schema(
            operation_summary="Cria comentário", operation_description="Cria comentário em uma postagem",
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "autor" : openapi.Schema(description="Id do autor da postagem", type=openapi.TYPE_STRING),
                    "postagem" : openapi.Schema(description="Id da postagem a qual o comentário irá pertencer", type=openapi.TYPE_INTEGER),
                    "texto" : openapi.Schema(description="Conteúdo do comentário.", type=openapi.TYPE_STRING),
                }
            ),
            response={201: ConectaPucSerializer.ComentarioCreate()}
    )
    def post(self, request):
        serializer = ConectaPucSerializer.ComentarioCreate(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ComentarioUpdateView(APIView):
    @swagger_auto_schema(
        operation_summary = "Atualiza Comentário", operation_description="Atualiza comentário feito pelo próprio usuário",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "texto" : openapi.Schema(description="Texto para qual o comentário será alterado.", type=openapi.TYPE_STRING),
            }
        ),
        responses={201: ConectaPucSerializer.Comentario()}
    )
    def put(self, request, pk):
        comentario = self.get_comentario(pk)

        serializer = ConectaPucSerializer.ComentarioUpdate(comentario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_comentario(self, pk):
        try:
            return Comentario.objects.get(pk=pk)
        except Comentario.DoesNotExist:
            raise Http404
        

class ComentarioDeleteView(APIView):
    @swagger_auto_schema(
        operation_summary="Remove um comentário",
        operation_description="Remove um comentário caso usuário o tenha feito ou seja admin.",
        request_body=None,
        responses={
            204: ConectaPucSerializer.Comentario(),
        },
    )
    def delete(self, request, pk):
        try:
            comentario = Comentario.objects.get(id=pk)

            # Verifique se o usuário atual é o autor do comentário
            #if comentario.autor == request.user or request.user.is_superuser():
            comentario.delete()
            return Response({'message' : "Comentário excluído com sucesso."}, status=status.HTTP_204_NO_CONTENT)
            #else:
                #return Response({'error': 'Você não tem permissão para excluir este comentário.'}, status=status.HTTP_403_FORBIDDEN)

        except Comentario.DoesNotExist:
            return Response({'error': f'Comentário(s) com ID(s) [{pk}] não encontrado(s)'}, status=status.HTTP_404_NOT_FOUND)

