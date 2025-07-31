"""
Views principais da plataforma.
"""
from django.shortcuts import render


def home(request):
    """
    Página inicial da plataforma - lista os restaurantes em destaque.
    """
    # Aqui vamos listar restaurantes em destaque
    context = {
        'page_title': 'Menuly - Delivery Multi-Restaurante',
        'meta_description': 'Encontre os melhores restaurantes da sua região e faça seus pedidos online.',
    }
    return render(request, 'core/home.html', context)


def lista_restaurantes(request):
    """
    Lista todos os restaurantes ativos da plataforma.
    """
    # Aqui vamos buscar todos os restaurantes ativos
    context = {
        'page_title': 'Todos os Restaurantes - Menuly',
        'meta_description': 'Explore todos os restaurantes disponíveis na plataforma.',
    }
    return render(request, 'core/lista_restaurantes.html', context)
