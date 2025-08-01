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
    Cria o cliente, endereço e pedido no banco de dados.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    
    restaurante = request.restaurante_atual
    
    if not restaurante or not restaurante.aceita_pedidos:
        return JsonResponse({'error': 'Restaurante não aceita pedidos'}, status=400)
    
    try:
        from django.db import transaction
        from apps.accounts.models import Cliente, EnderecoCliente
        from apps.pedidos.models import Pedido, ItemPedido
        from apps.restaurantes.models import Produto
        import uuid
        import re
        
        dados = json.loads(request.body)
        
        # Validar dados obrigatórios
        required_fields = ['celular', 'nome', 'cep', 'rua', 'numero', 'bairro', 'forma_pagamento', 'itens']
        for field in required_fields:
            if not dados.get(field):
                return JsonResponse({'error': f'Campo {field} é obrigatório'}, status=400)
        
        with transaction.atomic():
            # 1. Buscar ou criar cliente
            celular_limpo = re.sub(r'\D', '', dados['celular'])
            
            cliente, created = Cliente.objects.get_or_create(
                celular=celular_limpo,
                defaults={
                    'nome': dados['nome'],
                    'email': dados.get('email', ''),
                }
            )
            
            # Atualizar dados se cliente já existe
            if not created:
                if dados['nome']:
                    cliente.nome = dados['nome']
                if dados.get('email'):
                    cliente.email = dados['email']
                cliente.save()
            
            # 2. Criar endereço de entrega
            endereco = EnderecoCliente.objects.create(
                cliente=cliente,
                apelido='Entrega',
                endereco=dados['rua'],
                numero=dados['numero'],
                complemento=dados.get('complemento', ''),
                bairro=dados['bairro'],
                cidade=dados.get('cidade', 'São Paulo'),
                estado=dados.get('estado', 'SP'),
                cep=re.sub(r'\D', '', dados['cep']),
                referencia=dados.get('referencia', ''),
                eh_principal=False
            )
            
            # 3. Calcular totais
            subtotal = 0
            itens_validados = []
            
            for item_data in dados['itens']:
                try:
                    produto = Produto.objects.get(
                        id=item_data['id'], 
                        restaurante=restaurante,
                        disponivel=True
                    )
                    
                    quantidade = int(item_data['quantidade'])
                    if quantidade <= 0:
                        continue
                        
                    item_total = produto.preco * quantidade
                    subtotal += item_total
                    
                    itens_validados.append({
                        'produto': produto,
                        'quantidade': quantidade,
                        'preco_unitario': produto.preco,
                        'subtotal': item_total
                    })
                    
                except (Produto.DoesNotExist, ValueError, KeyError):
                    continue
            
            if not itens_validados:
                return JsonResponse({'error': 'Nenhum item válido no carrinho'}, status=400)
            
            # Verificar pedido mínimo
            if restaurante.pedido_minimo > 0 and subtotal < restaurante.pedido_minimo:
                return JsonResponse({
                    'error': f'Pedido mínimo é R$ {restaurante.pedido_minimo:.2f}'
                }, status=400)
            
            taxa_entrega = restaurante.taxa_entrega if restaurante.taxa_entrega else 0
            total = subtotal + taxa_entrega
            
            # 4. Criar pedido
            numero_pedido = f"PED{uuid.uuid4().hex[:8].upper()}"
            
            pedido = Pedido.objects.create(
                numero=numero_pedido,
                restaurante=restaurante,
                cliente=cliente,
                
                # Dados do cliente
                cliente_nome=cliente.nome,
                cliente_celular=cliente.celular,
                cliente_email=cliente.email,
                
                # Endereço de entrega
                endereco_rua=endereco.endereco,
                endereco_numero=endereco.numero,
                endereco_complemento=endereco.complemento,
                endereco_bairro=endereco.bairro,
                endereco_cidade=endereco.cidade,
                endereco_estado=endereco.estado,
                endereco_cep=endereco.cep,
                endereco_referencia=endereco.referencia,
                
                # Valores
                subtotal=subtotal,
                taxa_entrega=taxa_entrega,
                total=total,
                
                # Configurações
                tipo='delivery',
                forma_pagamento=dados['forma_pagamento'],
                observacoes=dados.get('observacoes', ''),
                status='recebido'
            )
            
            # 5. Criar itens do pedido
            for item in itens_validados:
                ItemPedido.objects.create(
                    pedido=pedido,
                    produto=item['produto'],
                    quantidade=item['quantidade'],
                    preco_unitario=item['preco_unitario'],
                    subtotal=item['subtotal'],
                    observacoes=''
                )
            
            # 6. Atualizar estatísticas do cliente
            cliente.total_pedidos += 1
            cliente.valor_total_gasto += total
            cliente.save()
            
            # 7. Salvar número do pedido na sessão
            request.session['ultimo_pedido_numero'] = numero_pedido
            
            return JsonResponse({
                'success': True,
                'numero_pedido': numero_pedido,
                'total': float(total),
                'message': 'Pedido realizado com sucesso!',
                'redirect_url': f"/{slug}/pedido-recebido/"
            })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Dados JSON inválidos'}, status=400)
    except Exception as e:
        import traceback
        print(f"Erro ao finalizar pedido: {e}")
        print(traceback.format_exc())
        return JsonResponse({'error': 'Erro interno do servidor'}, status=500)
