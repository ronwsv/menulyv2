"""
Views da API de pedidos.
"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from apps.restaurantes.models import Restaurante, Categoria, Produto
from .models import Pedido, Cliente, ItemPedido
import json


def lista_restaurantes(request):
    """API para listar todos os restaurantes ativos."""
    restaurantes = Restaurante.objects.filter(ativo=True, aprovado=True)
    
    data = []
    for restaurante in restaurantes:
        data.append({
            'id': restaurante.id,
            'nome': restaurante.nome,
            'slug': restaurante.slug,
            'endereco': restaurante.endereco_completo,
            'telefone': restaurante.telefone,
            'taxa_entrega': float(restaurante.taxa_entrega),
            'tempo_estimado': restaurante.tempo_estimado_entrega,
            'esta_aberto': restaurante.esta_aberto,
            'logo': restaurante.logo.url if restaurante.logo else None,
        })
    
    return JsonResponse({'restaurantes': data})


def detalhes_restaurante(request, restaurante_id):
    """API para detalhes de um restaurante específico."""
    try:
        restaurante = Restaurante.objects.get(id=restaurante_id, ativo=True, aprovado=True)
    except Restaurante.DoesNotExist:
        return JsonResponse({'erro': 'Restaurante não encontrado'}, status=404)
    
    data = {
        'id': restaurante.id,
        'nome': restaurante.nome,
        'slug': restaurante.slug,
        'endereco_completo': restaurante.endereco_completo,
        'telefone': restaurante.telefone,
        'whatsapp': restaurante.whatsapp,
        'email': restaurante.email,
        'slogan': restaurante.slogan,
        'sobre_nos': restaurante.sobre_nos,
        'taxa_entrega': float(restaurante.taxa_entrega),
        'tempo_estimado_entrega': restaurante.tempo_estimado_entrega,
        'pedido_minimo': float(restaurante.pedido_minimo),
        'esta_aberto': restaurante.esta_aberto,
        'cores': {
            'primaria': restaurante.cor_primaria,
            'secundaria': restaurante.cor_secundaria,
            'fundo': restaurante.cor_fundo,
            'texto': restaurante.cor_texto,
            'botoes': restaurante.cor_botoes,
        },
        'imagens': {
            'logo': restaurante.logo.url if restaurante.logo else None,
            'banner': restaurante.banner.url if restaurante.banner else None,
            'favicon': restaurante.favicon.url if restaurante.favicon else None,
        }
    }
    
    return JsonResponse(data)


def cardapio_restaurante(request, restaurante_id):
    """API para o cardápio completo de um restaurante."""
    try:
        restaurante = Restaurante.objects.get(id=restaurante_id, ativo=True, aprovado=True)
    except Restaurante.DoesNotExist:
        return JsonResponse({'erro': 'Restaurante não encontrado'}, status=404)
    
    categorias = restaurante.categorias.filter(ativo=True).prefetch_related('produtos')
    
    data = {
        'restaurante': {
            'id': restaurante.id,
            'nome': restaurante.nome,
        },
        'categorias': []
    }
    
    for categoria in categorias:
        produtos = categoria.produtos.filter(disponivel=True)
        
        produtos_data = []
        for produto in produtos:
            produtos_data.append({
                'id': produto.id,
                'nome': produto.nome,
                'descricao': produto.descricao,
                'preco': float(produto.preco),
                'imagem': produto.imagem_principal.url if produto.imagem_principal else None,
                'destaque': produto.destaque,
                'tempo_preparo': produto.tempo_preparo,
                'calorias': produto.calorias,
            })
        
        if produtos_data:  # Só inclui categoria se tiver produtos disponíveis
            data['categorias'].append({
                'id': categoria.id,
                'nome': categoria.nome,
                'descricao': categoria.descricao,
                'produtos': produtos_data
            })
    
    return JsonResponse(data)


@csrf_exempt
@require_http_methods(["POST"])
def finalizar_pedido_api(request):
    """API para finalizar um pedido."""
    try:
        dados = json.loads(request.body)
        
        # Valida dados obrigatórios
        campos_obrigatorios = [
            'restaurante_id', 'cliente', 'itens', 'endereco_entrega',
            'forma_pagamento', 'tipo'
        ]
        
        for campo in campos_obrigatorios:
            if campo not in dados:
                return JsonResponse({'erro': f'Campo obrigatório: {campo}'}, status=400)
        
        # Valida restaurante
        try:
            restaurante = Restaurante.objects.get(
                id=dados['restaurante_id'], 
                ativo=True, 
                aceita_pedidos=True
            )
        except Restaurante.DoesNotExist:
            return JsonResponse({'erro': 'Restaurante não disponível'}, status=400)
        
        # Cria ou busca cliente
        cliente_data = dados['cliente']
        cliente, created = Cliente.objects.get_or_create(
            telefone=cliente_data['telefone'],
            defaults={
                'nome': cliente_data['nome'],
                'email': cliente_data.get('email', ''),
            }
        )
        
        # Calcula valores do pedido
        subtotal = 0
        itens_validos = []
        
        for item_data in dados['itens']:
            try:
                produto = Produto.objects.get(
                    id=item_data['produto_id'], 
                    disponivel=True,
                    restaurante=restaurante
                )
                
                quantidade = int(item_data['quantidade'])
                preco_unitario = float(produto.preco)
                
                # TODO: Calcular preço com opções adicionais
                
                subtotal += quantidade * preco_unitario
                
                itens_validos.append({
                    'produto': produto,
                    'quantidade': quantidade,
                    'preco_unitario': preco_unitario,
                    'opcoes': item_data.get('opcoes', {}),
                    'observacoes': item_data.get('observacoes', ''),
                })
                
            except (Produto.DoesNotExist, ValueError, KeyError):
                return JsonResponse({'erro': 'Item inválido no pedido'}, status=400)
        
        if not itens_validos:
            return JsonResponse({'erro': 'Pedido sem itens válidos'}, status=400)
        
        # Calcula taxa de entrega
        taxa_entrega = 0
        if dados['tipo'] == 'delivery':
            taxa_entrega = float(restaurante.taxa_entrega)
        
        total = subtotal + taxa_entrega
        
        # Valida pedido mínimo
        if total < restaurante.pedido_minimo:
            return JsonResponse({
                'erro': f'Pedido mínimo: R$ {restaurante.pedido_minimo:.2f}'
            }, status=400)
        
        # Cria o pedido
        endereco = dados['endereco_entrega']
        pedido = Pedido.objects.create(
            restaurante=restaurante,
            cliente=cliente,
            tipo=dados['tipo'],
            endereco_entrega_rua=endereco['rua'],
            endereco_entrega_numero=endereco['numero'],
            endereco_entrega_complemento=endereco.get('complemento', ''),
            endereco_entrega_bairro=endereco['bairro'],
            endereco_entrega_cidade=endereco['cidade'],
            endereco_entrega_estado=endereco['estado'],
            endereco_entrega_cep=endereco['cep'],
            endereco_entrega_referencia=endereco.get('referencia', ''),
            subtotal=subtotal,
            taxa_entrega=taxa_entrega,
            total=total,
            forma_pagamento=dados['forma_pagamento'],
            troco_para=dados.get('troco_para'),
            observacoes=dados.get('observacoes', ''),
        )
        
        # Cria os itens do pedido
        for item_data in itens_validos:
            ItemPedido.objects.create(
                pedido=pedido,
                produto=item_data['produto'],
                quantidade=item_data['quantidade'],
                preco_unitario=item_data['preco_unitario'],
                opcoes_selecionadas=item_data['opcoes'],
                observacoes=item_data['observacoes'],
            )
        
        return JsonResponse({
            'sucesso': True,
            'pedido': {
                'numero': pedido.numero,
                'total': float(pedido.total),
                'tempo_estimado': restaurante.tempo_estimado_entrega,
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'erro': 'Dados inválidos'}, status=400)
    except Exception as e:
        return JsonResponse({'erro': 'Erro interno do servidor'}, status=500)


@csrf_exempt
@require_http_methods(["PUT"])
def atualizar_status_pedido(request, numero):
    """API para atualizar o status de um pedido."""
    try:
        dados = json.loads(request.body)
        novo_status = dados.get('status')
        
        if not novo_status:
            return JsonResponse({'erro': 'Status não informado'}, status=400)
        
        # Valida status
        status_validos = [choice[0] for choice in Pedido.STATUS_CHOICES]
        if novo_status not in status_validos:
            return JsonResponse({'erro': 'Status inválido'}, status=400)
        
        # Busca o pedido
        try:
            pedido = Pedido.objects.get(numero=numero)
        except Pedido.DoesNotExist:
            return JsonResponse({'erro': 'Pedido não encontrado'}, status=404)
        
        # Atualiza o status
        pedido.status = novo_status
        
        # Atualiza timestamps específicos
        from django.utils import timezone
        if novo_status == 'confirmado' and not pedido.confirmado_em:
            pedido.confirmado_em = timezone.now()
        elif novo_status == 'pronto' and not pedido.pronto_em:
            pedido.pronto_em = timezone.now()
        elif novo_status == 'entregue' and not pedido.entregue_em:
            pedido.entregue_em = timezone.now()
        
        pedido.save()
        
        return JsonResponse({
            'sucesso': True,
            'pedido': {
                'numero': pedido.numero,
                'status': pedido.status,
                'status_display': pedido.get_status_display(),
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'erro': 'Dados inválidos'}, status=400)
    except Exception as e:
        return JsonResponse({'erro': 'Erro interno do servidor'}, status=500)
