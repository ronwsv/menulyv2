"""
URLs da API de pedidos.
"""
from django.urls import path
from . import api_views

app_name = 'api_pedidos'

urlpatterns = [
    path('restaurantes/', api_views.lista_restaurantes, name='lista_restaurantes'),
    path('restaurante/<int:restaurante_id>/', api_views.detalhes_restaurante, name='detalhes_restaurante'),
    path('restaurante/<int:restaurante_id>/cardapio/', api_views.cardapio_restaurante, name='cardapio_restaurante'),
    path('finalizar-pedido/', api_views.finalizar_pedido_api, name='finalizar_pedido'),
    path('pedidos/<str:numero>/status/', api_views.atualizar_status_pedido, name='atualizar_status'),
]
