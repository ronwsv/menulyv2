"""
URLs do painel do lojista.
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import views_impressoras
from . import views_pedidos

app_name = 'lojista'

urlpatterns = [
    # Autenticação
    path('login/', auth_views.LoginView.as_view(template_name='lojista/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Dashboard principal
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Gestão de restaurantes
    path('restaurantes/', views.lista_restaurantes, name='lista_restaurantes'),
    path('restaurante/<int:restaurante_id>/', views.detalhes_restaurante, name='detalhes_restaurante'),
    path('restaurante/<int:restaurante_id>/editar/', views.editar_restaurante, name='editar_restaurante'),
    path('restaurante/novo/', views.novo_restaurante, name='novo_restaurante'),
    
    # Gestão de produtos
    path('restaurante/<int:restaurante_id>/produtos/', views.lista_produtos, name='lista_produtos'),
    path('restaurante/<int:restaurante_id>/produto/novo/', views.novo_produto, name='novo_produto'),
    path('produto/<int:produto_id>/editar/', views.editar_produto, name='editar_produto'),
    path('produto/<int:produto_id>/deletar/', views.deletar_produto, name='deletar_produto'),
    
    # Gestão de categorias
    path('restaurante/<int:restaurante_id>/categorias/', views.lista_categorias, name='lista_categorias'),
    path('restaurante/<int:restaurante_id>/categoria/nova/', views.nova_categoria, name='nova_categoria'),
    path('categoria/<int:categoria_id>/editar/', views.editar_categoria, name='editar_categoria'),
    
    # Gestão de pedidos
    path('pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('pedidos/tempo-real/', views_pedidos.pedidos_tempo_real, name='pedidos_tempo_real'),
    path('pedidos/metricas/', views_pedidos.dashboard_metricas, name='dashboard_metricas'),
    path('pedidos/api/estatisticas/', views_pedidos.api_pedidos_estatisticas, name='api_pedidos_estatisticas'),
    path('pedidos/criar-teste/', views_pedidos.criar_pedido_teste, name='criar_pedido_teste'),
    path('pedido/<str:numero>/', views.detalhes_pedido, name='detalhes_pedido'),
    path('pedido/<str:numero>/status/', views_pedidos.atualizar_status_pedido, name='atualizar_status_pedido'),
    
    # Gestão de impressoras
    path('impressoras/', views_impressoras.impressoras, name='impressoras'),
    path('impressoras/logs/', views_impressoras.logs_impressao, name='logs_impressao'),
    path('pedido/<int:pedido_id>/imprimir/', views_impressoras.imprimir_pedido, name='imprimir_pedido'),
    
    # Configurações
    path('configuracoes/', views.configuracoes, name='configuracoes'),
    path('plano/', views.gerenciar_plano, name='gerenciar_plano'),
]
