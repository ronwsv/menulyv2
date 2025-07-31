"""
URLs do painel do super administrador.
"""
from django.urls import path
from . import views

app_name = 'superadmin'

urlpatterns = [
    # Dashboard principal
    path('', views.dashboard, name='dashboard'),
    
    # Gestão de lojistas
    path('lojistas/', views.lista_lojistas, name='lista_lojistas'),
    path('lojista/<int:lojista_id>/', views.detalhes_lojista, name='detalhes_lojista'),
    path('lojista/novo/', views.novo_lojista, name='novo_lojista'),
    path('lojista/<int:lojista_id>/editar/', views.editar_lojista, name='editar_lojista'),
    path('lojista/<int:lojista_id>/suspender/', views.suspender_lojista, name='suspender_lojista'),
    
    # Gestão de restaurantes
    path('restaurantes/', views.lista_restaurantes, name='lista_restaurantes'),
    path('restaurante/<int:restaurante_id>/', views.detalhes_restaurante, name='detalhes_restaurante'),
    path('restaurante/<int:restaurante_id>/aprovar/', views.aprovar_restaurante, name='aprovar_restaurante'),
    
    # Gestão de planos
    path('planos/', views.lista_planos, name='lista_planos'),
    path('plano/novo/', views.novo_plano, name='novo_plano'),
    path('plano/<int:plano_id>/editar/', views.editar_plano, name='editar_plano'),
    
    # Relatórios
    path('relatorios/', views.relatorios, name='relatorios'),
    path('relatorios/vendas/', views.relatorio_vendas, name='relatorio_vendas'),
    path('relatorios/lojistas/', views.relatorio_lojistas, name='relatorio_lojistas'),
    
    # Configurações
    path('configuracoes/', views.configuracoes, name='configuracoes'),
]
