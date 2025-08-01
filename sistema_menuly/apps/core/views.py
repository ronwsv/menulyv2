"""
Views principais da plataforma.
"""
from django.shortcuts import render
from apps.restaurantes.models import Restaurante


def home(request):
    """
    Página inicial da plataforma - lista os restaurantes em destaque.
    """
    # Busca restaurantes em destaque (limitado a 6)
    restaurantes_destaque = Restaurante.objects.filter(
        ativo=True,
        lojista__ativo=True
    ).select_related('lojista').order_by('-criado_em')[:6]
    
    context = {
        'page_title': 'Menuly - Delivery Multi-Restaurante',
        'meta_description': 'Encontre os melhores restaurantes da sua região e faça seus pedidos online.',
        'restaurantes_destaque': restaurantes_destaque,
    }
    return render(request, 'core/home.html', context)


def lista_restaurantes(request):
    """
    Lista todos os restaurantes ativos da plataforma.
    """
    # Busca todos os restaurantes ativos
    restaurantes = Restaurante.objects.filter(
        ativo=True,
        lojista__ativo=True
    ).select_related('lojista').order_by('nome')
    
    context = {
        'page_title': 'Todos os Restaurantes - Menuly',
        'meta_description': 'Explore todos os restaurantes disponíveis na plataforma.',
        'restaurantes': restaurantes,
    }
    return render(request, 'core/lista_restaurantes.html', context)
