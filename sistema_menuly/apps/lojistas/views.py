"""
Views do painel do lojista.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from apps.restaurantes.models import Restaurante, Categoria, Produto, Lojista
from apps.pedidos.models import Pedido
import json


@login_required
def dashboard(request):
    """Dashboard principal do lojista."""
    try:
        lojista = request.user.lojista
    except Lojista.DoesNotExist:
        messages.error(request, 'Usuário não é um lojista válido.')
        return redirect('core:home')
    
    # Busca restaurantes do lojista
    restaurantes = lojista.restaurantes.filter(ativo=True)
    
    # Métricas do dia atual
    hoje = timezone.now().date()
    pedidos_hoje = Pedido.objects.filter(
        restaurante__in=restaurantes,
        criado_em__date=hoje
    )
    
    # Estatísticas básicas
    stats = {
        'total_restaurantes': restaurantes.count(),
        'pedidos_hoje': pedidos_hoje.count(),
        'faturamento_hoje': pedidos_hoje.aggregate(
            total=Sum('total')
        )['total'] or 0,
        'pedidos_pendentes': pedidos_hoje.filter(
            status__in=['recebido', 'confirmado', 'preparando']
        ).count(),
    }
    
    # Pedidos recentes (últimos 10)
    pedidos_recentes = Pedido.objects.filter(
        restaurante__in=restaurantes
    ).order_by('-criado_em')[:10]
    
    # Dados para gráfico de vendas da semana
    # (últimos 7 dias)
    vendas_semana = []
    for i in range(7):
        data = hoje - timedelta(days=i)
        vendas_dia = Pedido.objects.filter(
            restaurante__in=restaurantes,
            criado_em__date=data
        ).aggregate(total=Sum('total'))['total'] or 0
        
        vendas_semana.append({
            'data': data.strftime('%d/%m'),
            'vendas': float(vendas_dia)
        })
    
    vendas_semana.reverse()  # Ordem cronológica
    
    context = {
        'lojista': lojista,
        'user_restaurants': restaurantes,
        'data_atual': hoje,
        'pedidos_hoje': stats['pedidos_hoje'],
        'faturamento_hoje': stats['faturamento_hoje'],
        'pedidos_pendentes': stats['pedidos_pendentes'],
        'clientes_mes': 25,  # Exemplo - implementar depois
        'pedidos_recentes': pedidos_recentes,
        'vendas_semana': json.dumps(vendas_semana),
    }
    
    return render(request, 'lojista/dashboard.html', context)


@login_required
def lista_restaurantes(request):
    """Lista todos os restaurantes do lojista."""
    try:
        lojista = request.user.lojista
    except Lojista.DoesNotExist:
        messages.error(request, 'Usuário não é um lojista válido.')
        return redirect('core:home')
    
    restaurantes = lojista.restaurantes.all()
    
    context = {
        'restaurantes': restaurantes,
        'pode_criar': lojista.pode_criar_restaurante,
    }
    
    return render(request, 'lojista/lista_restaurantes.html', context)


@login_required
def detalhes_restaurante(request, restaurante_id):
    """Exibe detalhes de um restaurante específico."""
    try:
        lojista = request.user.lojista
    except Lojista.DoesNotExist:
        messages.error(request, 'Usuário não é um lojista válido.')
        return redirect('core:home')
    
    restaurante = get_object_or_404(
        Restaurante, 
        id=restaurante_id, 
        lojista=lojista
    )
    
    # Estatísticas do restaurante
    hoje = timezone.now().date()
    stats = {
        'total_produtos': restaurante.produtos.count(),
        'produtos_ativos': restaurante.produtos.filter(disponivel=True).count(),
        'pedidos_hoje': restaurante.pedidos.filter(criado_em__date=hoje).count(),
        'faturamento_mes': restaurante.pedidos.filter(
            criado_em__month=hoje.month,
            criado_em__year=hoje.year
        ).aggregate(total=Sum('total'))['total'] or 0,
    }
    
    context = {
        'restaurante': restaurante,
        'stats': stats,
    }
    
    return render(request, 'lojista/detalhes_restaurante.html', context)


@login_required
def editar_restaurante(request, restaurante_id):
    """Editar configurações do restaurante."""
    # TODO: Implementar formulário de edição
    messages.info(request, 'Funcionalidade em desenvolvimento.')
    return redirect('lojista:detalhes_restaurante', restaurante_id=restaurante_id)


@login_required
def novo_restaurante(request):
    """Criar novo restaurante."""
    # TODO: Implementar formulário de criação
    messages.info(request, 'Funcionalidade em desenvolvimento.')
    return redirect('lojista:lista_restaurantes')


@login_required
def lista_produtos(request, restaurante_id):
    """Lista produtos de um restaurante."""
    try:
        lojista = request.user.lojista
    except Lojista.DoesNotExist:
        messages.error(request, 'Usuário não é um lojista válido.')
        return redirect('core:home')
    
    restaurante = get_object_or_404(
        Restaurante, 
        id=restaurante_id, 
        lojista=lojista
    )
    
    produtos = restaurante.produtos.all().select_related('categoria')
    categorias = restaurante.categorias.all()
    
    context = {
        'restaurante': restaurante,
        'produtos': produtos,
        'categorias': categorias,
    }
    
    return render(request, 'lojista/lista_produtos.html', context)


@login_required
def novo_produto(request, restaurante_id):
    """Criar novo produto."""
    # TODO: Implementar formulário de criação de produto
    messages.info(request, 'Funcionalidade em desenvolvimento.')
    return redirect('lojista:lista_produtos', restaurante_id=restaurante_id)


@login_required
def editar_produto(request, produto_id):
    """Editar produto."""
    # TODO: Implementar formulário de edição de produto
    messages.info(request, 'Funcionalidade em desenvolvimento.')
    return redirect('lojista:lista_produtos', restaurante_id=1)  # Temporary


@login_required
def deletar_produto(request, produto_id):
    """Deletar produto."""
    # TODO: Implementar exclusão de produto
    messages.info(request, 'Funcionalidade em desenvolvimento.')
    return redirect('lojista:lista_produtos', restaurante_id=1)  # Temporary


@login_required
def lista_categorias(request, restaurante_id):
    """Lista categorias de um restaurante."""
    # TODO: Implementar lista de categorias
    messages.info(request, 'Funcionalidade em desenvolvimento.')
    return redirect('lojista:detalhes_restaurante', restaurante_id=restaurante_id)


@login_required
def nova_categoria(request, restaurante_id):
    """Criar nova categoria."""
    # TODO: Implementar criação de categoria
    messages.info(request, 'Funcionalidade em desenvolvimento.')
    return redirect('lojista:lista_categorias', restaurante_id=restaurante_id)


@login_required
def editar_categoria(request, categoria_id):
    """Editar categoria."""
    # TODO: Implementar edição de categoria
    messages.info(request, 'Funcionalidade em desenvolvimento.')
    return redirect('lojista:lista_categorias', restaurante_id=1)  # Temporary


@login_required
def lista_pedidos(request):
    """Lista todos os pedidos dos restaurantes do lojista."""
    try:
        lojista = request.user.lojista
    except Lojista.DoesNotExist:
        messages.error(request, 'Usuário não é um lojista válido.')
        return redirect('core:home')
    
    # Filtros
    status_filter = request.GET.get('status', '')
    restaurante_filter = request.GET.get('restaurante', '')
    data_filter = request.GET.get('data', '')
    
    # CONTROLE MULTI-LOJA: Base query filtra APENAS restaurantes do lojista logado
    pedidos = Pedido.objects.filter(
        restaurante__lojista=lojista  # CRUCIAL: Garante que só vê pedidos dos SEUS restaurantes
    ).select_related('restaurante', 'cliente').prefetch_related('itens__produto').order_by('-criado_em')
    
    # Aplica filtros
    if status_filter:
        pedidos = pedidos.filter(status=status_filter)
    
    if restaurante_filter:
        try:
            rest_id = int(restaurante_filter)
            # SEGURANÇA: Verifica se o restaurante pertence ao lojista
            if lojista.restaurantes.filter(id=rest_id).exists():
                pedidos = pedidos.filter(restaurante_id=rest_id)
            else:
                messages.warning(request, 'Restaurante não encontrado ou não autorizado.')
        except ValueError:
            pass
    
    if data_filter:
        try:
            from datetime import datetime
            data = datetime.strptime(data_filter, '%Y-%m-%d').date()
            pedidos = pedidos.filter(criado_em__date=data)
        except ValueError:
            pass
    
    # Paginação simples (últimos 50)
    pedidos = pedidos[:50]
    
    # Estatísticas do lojista
    total_pedidos = pedidos.count()
    pedidos_entregues = pedidos.filter(status='entregue').count()
    pedidos_preparando = pedidos.filter(status='preparando').count()
    
    # Total de restaurantes do lojista
    total_restaurantes = lojista.restaurantes.count()
    
    context = {
        'pedidos': pedidos,
        'restaurantes': lojista.restaurantes.all(),  # APENAS restaurantes do lojista
        'status_choices': Pedido.STATUS_CHOICES,
        'filtros': {
            'status': status_filter,
            'restaurante': restaurante_filter,
            'data': data_filter,
        },
        'estatisticas': {
            'total_pedidos': total_pedidos,
            'pedidos_entregues': pedidos_entregues,
            'pedidos_preparando': pedidos_preparando,
            'total_restaurantes': total_restaurantes,
        },
        'lojista': lojista,
    }
    
    return render(request, 'lojista/lista_pedidos.html', context)


@login_required
def detalhes_pedido(request, numero):
    """Exibe detalhes de um pedido específico."""
    try:
        lojista = request.user.lojista
    except Lojista.DoesNotExist:
        messages.error(request, 'Usuário não é um lojista válido.')
        return redirect('core:home')
    
    pedido = get_object_or_404(
        Pedido, 
        numero=numero, 
        restaurante__lojista=lojista
    )
    
    context = {
        'pedido': pedido,
    }
    
    return render(request, 'lojista/detalhes_pedido.html', context)


@login_required
def atualizar_status_pedido(request, numero):
    """Atualiza o status de um pedido com controle multi-loja."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método não permitido'}, status=405)
    
    try:
        lojista = request.user.lojista
    except Lojista.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Usuário não é um lojista válido'}, status=403)
    
    # CONTROLE MULTI-LOJA: Garante que o pedido pertence a um restaurante do lojista
    pedido = get_object_or_404(
        Pedido, 
        numero=numero, 
        restaurante__lojista=lojista  # CRUCIAL: Só permite acesso aos pedidos dos SEUS restaurantes
    )
    
    novo_status = request.POST.get('novo_status')
    observacoes = request.POST.get('observacoes', '')
    
    # Valida status
    status_validos = [choice[0] for choice in Pedido.STATUS_CHOICES]
    if novo_status not in status_validos:
        return JsonResponse({'success': False, 'error': 'Status inválido'}, status=400)
    
    # Verifica se o status realmente mudou
    if pedido.status == novo_status:
        return JsonResponse({'success': False, 'error': 'Status já é o mesmo'}, status=400)
    
    # Log da mudança de status
    status_anterior = pedido.get_status_display()
    
    # Atualiza o status
    pedido.status = novo_status
    
    # Atualiza timestamps específicos baseado no novo status
    from django.utils import timezone
    now = timezone.now()
    
    if novo_status == 'confirmado' and not hasattr(pedido, 'confirmado_em'):
        pedido.confirmado_em = now
    elif novo_status == 'preparando' and not hasattr(pedido, 'preparando_em'):
        pedido.preparando_em = now
    elif novo_status == 'pronto' and not hasattr(pedido, 'pronto_em'):
        pedido.pronto_em = now
    elif novo_status == 'entregue' and not hasattr(pedido, 'entregue_em'):
        pedido.entregue_em = now
    elif novo_status == 'cancelado' and not hasattr(pedido, 'cancelado_em'):
        pedido.cancelado_em = now
    
    # Adiciona observações se fornecidas
    if observacoes:
        if pedido.observacoes:
            pedido.observacoes += f"\n[{now.strftime('%d/%m/%Y %H:%M')}] Status alterado para {pedido.get_status_display()}: {observacoes}"
        else:
            pedido.observacoes = f"[{now.strftime('%d/%m/%Y %H:%M')}] Status alterado para {pedido.get_status_display()}: {observacoes}"
    
    try:
        pedido.save()
        
        # Log de sucesso
        messages.success(request, f'Status do pedido #{numero} alterado de "{status_anterior}" para "{pedido.get_status_display()}"')
        
        return JsonResponse({
            'success': True,
            'novo_status': pedido.get_status_display(),
            'status_code': pedido.status,
            'message': f'Status atualizado para {pedido.get_status_display()}'
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'Erro ao salvar: {str(e)}'}, status=500)


@login_required
def configuracoes(request):
    """Configurações gerais do lojista."""
    try:
        lojista = request.user.lojista
    except Lojista.DoesNotExist:
        messages.error(request, 'Usuário não é um lojista válido.')
        return redirect('core:home')
    
    context = {
        'lojista': lojista,
    }
    
    return render(request, 'lojista/configuracoes.html', context)


@login_required
def gerenciar_plano(request):
    """Gerenciamento do plano de assinatura."""
    try:
        lojista = request.user.lojista
    except Lojista.DoesNotExist:
        messages.error(request, 'Usuário não é um lojista válido.')
        return redirect('core:home')
    
    context = {
        'lojista': lojista,
    }
    
    return render(request, 'lojista/gerenciar_plano.html', context)
