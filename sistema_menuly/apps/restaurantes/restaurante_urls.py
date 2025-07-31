"""
URLs dos mini-sites dos restaurantes.

Estas URLs são acessadas após o middleware detectar o restaurante pelo slug.
Ex: /pizzaria-do-jose/ -> chama estas views com request.restaurante_atual preenchido
"""
from django.urls import path
from . import views

app_name = 'restaurante'

urlpatterns = [
    # Mini-site principal
    path('', views.menu_restaurante, name='menu'),
    path('sobre/', views.sobre_restaurante, name='sobre'),
    path('checkout/', views.checkout, name='checkout'),
    path('pedido-recebido/', views.pedido_recebido, name='pedido_recebido'),
    
    # APIs para o mini-site
    path('api/buscar-cep/', views.buscar_cep, name='buscar_cep'),
    path('api/finalizar-pedido/', views.finalizar_pedido, name='finalizar_pedido'),
]
