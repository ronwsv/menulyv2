"""
Views dos mini-sites dos restaurantes.

Todas essas views têm acesso ao request.restaurante_atual graças ao middleware.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
import json
import requests
from .models import Restaurante, Categoria, Produto


def menu_restaurante(request, slug=None):
    """
    Página principal do mini-site - cardápio do restaurante.
    
    O slug já foi processado pelo middleware, então temos request.restaurante_atual
    """
    restaurante = request.restaurante_atual
    
    if not restaurante:
        return redirect('core:lista_restaurantes')
    
    # Busca categorias e produtos do restaurante
    categorias = restaurante.categorias.filter(ativo=True).prefetch_related('produtos')
    produtos_destaque = restaurante.produtos.filter(destaque=True, disponivel=True)[:6]
    
    context = {
        'restaurante': restaurante,
        'categorias': categorias,
        'produtos_destaque': produtos_destaque,
        'page_title': f"{restaurante.nome} - Delivery Online",
        'meta_description': f"Faça seu pedido online no {restaurante.nome}. {restaurante.slogan or 'Entrega rápida e comida deliciosa!'}",
    }
    
    return render(request, 'restaurante/menu.html', context)


def sobre_restaurante(request, slug=None):
    """
    Página sobre o restaurante.
    """
    restaurante = request.restaurante_atual
    
    if not restaurante:
        return redirect('core:lista_restaurantes')
    
    context = {
        'restaurante': restaurante,
        'page_title': f"Sobre - {restaurante.nome}",
        'meta_description': f"Conheça mais sobre o {restaurante.nome}. {restaurante.sobre_nos[:150] if restaurante.sobre_nos else ''}",
    }
    
    return render(request, 'restaurante/sobre.html', context)


def checkout(request, slug=None):
    """
    Página de finalização do pedido (checkout).
    """
    restaurante = request.restaurante_atual
    
    if not restaurante:
        return redirect('core:lista_restaurantes')
    
    if not restaurante.aceita_pedidos:
        messages.error(request, 'Este restaurante não está aceitando pedidos no momento.')
        return redirect('restaurante:menu', slug=slug)
    
    context = {
        'restaurante': restaurante,
        'page_title': f"Finalizar Pedido - {restaurante.nome}",
        'meta_description': f"Finalize seu pedido no {restaurante.nome}",
    }
    
    return render(request, 'restaurante/checkout.html', context)


def pedido_recebido(request, slug=None):
    """
    Página de confirmação após o pedido ser realizado.
    """
    restaurante = request.restaurante_atual
    
    if not restaurante:
        return redirect('core:lista_restaurantes')
    
    # Pega o número do pedido da sessão (será definido quando criar o pedido)
    numero_pedido = request.session.get('ultimo_pedido_numero')
    
    context = {
        'restaurante': restaurante,
        'numero_pedido': numero_pedido,
        'page_title': f"Pedido Recebido - {restaurante.nome}",
        'meta_description': f"Seu pedido foi recebido pelo {restaurante.nome}",
    }
    
    return render(request, 'restaurante/pedido_recebido.html', context)


def buscar_cep(request, slug=None):
    """
    API para buscar endereço pelo CEP usando ViaCEP.
    """
    if request.method != 'GET':
        return JsonResponse({'erro': 'Método não permitido'}, status=405)
    
    cep = request.GET.get('cep', '').replace('-', '').replace('.', '')
    
    if not cep or len(cep) != 8:
        return JsonResponse({'erro': 'CEP inválido'}, status=400)
    
    try:
        # Chama a API do ViaCEP
        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/', timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if 'erro' in data:
                return JsonResponse({'erro': 'CEP não encontrado'}, status=404)
            
            return JsonResponse({
                'sucesso': True,
                'endereco': {
                    'rua': data.get('logradouro', ''),
                    'bairro': data.get('bairro', ''),
                    'cidade': data.get('localidade', ''),
                    'estado': data.get('uf', ''),
                    'cep': cep
                }
            })
        else:
            return JsonResponse({'erro': 'Erro ao consultar CEP'}, status=500)
            
    except Exception as e:
        return JsonResponse({'erro': 'Erro interno do servidor'}, status=500)


@csrf_exempt
def finalizar_pedido(request, slug=None):
    """
    API para finalizar o pedido.
    """
    if request.method != 'POST':
        return JsonResponse({'erro': 'Método não permitido'}, status=405)
    
    restaurante = request.restaurante_atual
    
    if not restaurante or not restaurante.aceita_pedidos:
        return JsonResponse({'erro': 'Restaurante não aceita pedidos'}, status=400)
    
    try:
        dados = json.loads(request.body)
        
        # Aqui vamos processar o pedido
        # Por enquanto, vamos apenas simular o sucesso
        
        # Gera um número de pedido temporário
        numero_pedido = f"{restaurante.id}{len(str(hash(str(dados))))}"
        
        # Salva na sessão para mostrar na página de confirmação
        request.session['ultimo_pedido_numero'] = numero_pedido
        
        return JsonResponse({
            'sucesso': True,
            'numero_pedido': numero_pedido,
            'mensagem': 'Pedido recebido com sucesso!',
            'redirect_url': f"/{slug}/pedido-recebido/"
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'erro': 'Dados inválidos'}, status=400)
    except Exception as e:
        return JsonResponse({'erro': 'Erro interno do servidor'}, status=500)
