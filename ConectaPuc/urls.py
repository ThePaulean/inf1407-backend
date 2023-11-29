"""
URL configuration for ConectaPuc project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from ConectaPucApp import views
from rest_framework import routers, permissions
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from drf_yasg.views import get_schema_view as yasg_schema_view
from drf_yasg import openapi

schema_view = yasg_schema_view(
    openapi.Info(
        title="API de exemplo",
        default_version="v1",
        description='Descrição da API de exemplo',
        contact=openapi.Contact(email="paulosgmvianna@gmail.com"),
        license=openapi.License(name='GNU GPLv3'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('api/foruns/create/', views.ForumCreateView.as_view(), name='forum-create'),
    path('', views.ForumListView.as_view(), name='forum-list'),
    path('api/foruns/update/<int:pk>/', views.ForumUpdateView.as_view(), name='forum-update'),
    path('api/foruns/delete/<int:pk>', views.ForumDeleteView.as_view(), name='forum-delete'),
    ###############
    path('api/postagens/create/', views.PostagemCreateView.as_view(), name='postagem-create'),
    path('api/postagens/', views.PostagemListView.as_view(), name='postagem-list'),
    path('api/postagens/update/<int:pk>/', views.PostagemUpdateView.as_view(), name='postagem-update'),
    path('api/postagens/delete/<int:pk>', views.PostagemDeleteView.as_view(), name='postagem-delete'),
    path('api/postagens/<int:postagem_id>/comentarios/', views.ComentarioListView.as_view(), name='comentario-list'),
    ###############
    path('api/comentarios/create/', views.ComentarioCreateView.as_view(), name='comentario-create'),
    path('api/comentarios/update/<int:pk>/', views.ComentarioUpdateView.as_view(), name='comentario-update'),
    path('api/comentarios/delete/<int:pk>', views.ComentarioDeleteView.as_view(), name='comentario-delete'),
    ###############
    path('docs/', include_docs_urls(title='Documentação da API')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema_swagger-ui'),
    path('api/v1/', include(routers.DefaultRouter().urls)),
    path('openapi', get_schema_view(title="API Para Forum", description="API para obter dados dos Foruns",),
         name='openapi-schema'),
    path('contas/', include('Contas.urls')),

]
