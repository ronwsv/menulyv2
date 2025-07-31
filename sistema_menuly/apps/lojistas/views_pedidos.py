"""
Views para gerenciamento de pedidos em tempo real
"""
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Count, Sum, Avg
from django.db.models.functions import TruncDate
from apps.restaurantes.models import Restaurante
from apps.pedidos.models import Pedido, Cliente
import json
from datetime import datetime, timedelta


@login_required
def pedidos_tempo_real(request):
    """Dashboard de pedidos em tempo real"""
    try:
        # Obter restaurante do usuário
        if hasattr(request.user, 'restaurante_lojista'):
            restaurante = request.user.restaurante_lojista
        else:
            restaurante = Restaurante.objects.get(proprietario=request.user)
    except Restaurante.DoesNotExist:
        messages.error(request, 'Você não possui acesso a nenhum restaurante.')
        return redirect('lojista:dashboard')
    
    # Data de hoje
    hoje = timezone.now().date()
    
    # Pedidos do dia
    pedidos_hoje = Pedido.objects.filter(
        restaurante=restaurante,
        criado_em__date=hoje
    ).select_related('cliente').prefetch_related('itens__produto').order_by('-criado_em')
    
    # Estatísticas do dia
    stats = {
        'total_pedidos': pedidos_hoje.count(),
        'pedidos_pendentes': pedidos_hoje.filter(
            status__in=['recebido', 'confirmado', 'preparando', 'pronto']
        ).count(),
        'faturamento_hoje': pedidos_hoje.filter(
            status__in=['entregue', 'pronto']
        ).aggregate(total=Sum('total'))['total'] or 0,
        'tempo_medio': calcular_tempo_medio_pedidos(pedidos_hoje.filter(status='entregue'))
    }
    
    context = {
        'restaurante': restaurante,
        'pedidos': pedidos_hoje[:50],  # Limitar para performance
        'total_pedidos': stats['total_pedidos'],
        'pedidos_pendentes': stats['pedidos_pendentes'],
        'faturamento_hoje': stats['faturamento_hoje'],
        'tempo_medio': stats['tempo_medio'],
        'title': 'Pedidos em Tempo Real'
    }
    
    return render(request, 'lojista/pedidos_tempo_real.html', context)


@login_required
@require_POST
def atualizar_status_pedido(request, numero):
    """Atualiza o status de um pedido"""
    try:
        restaurante = Restaurante.objects.get(proprietario=request.user)
        pedido = get_object_or_404(Pedido, numero=numero, restaurante=restaurante)
        
        data = json.loads(request.body)
        novo_status = data.get('status')
        
        if novo_status not in dict(Pedido.STATUS_CHOICES):
            return JsonResponse({'success': False, 'error': 'Status inválido'})
        
        # Atualizar timestamps baseado no status
        agora = timezone.now()
        status_anterior = pedido.status
        pedido.status = novo_status
        
        if novo_status == 'confirmado' and not pedido.confirmado_em:
            pedido.confirmado_em = agora
        elif novo_status == 'pronto' and not pedido.pronto_em:
            pedido.pronto_em = agora
        elif novo_status == 'entregue' and not pedido.entregue_em:
            pedido.entregue_em = agora
        
        pedido.save()
        
        # Aqui seria enviado via WebSocket para outros clientes
        # broadcast_order_update(pedido)
        
        # Se tem impressoras configuradas para auto-imprimir
        if novo_status == 'confirmado':
            from .views_impressoras import auto_imprimir_pedido
            auto_imprimir_pedido(pedido)
        
        return JsonResponse({
            'success': True,
            'order_id': pedido.id,
            'old_status': status_anterior,
            'new_status': novo_status,
            'updated_at': agora.isoformat()
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def api_pedidos_estatisticas(request):
    """API para estatísticas dos pedidos em tempo real"""
    try:
        restaurante = Restaurante.objects.get(proprietario=request.user)
        hoje = timezone.now().date()
        
        pedidos_hoje = Pedido.objects.filter(
            restaurante=restaurante,
            criado_em__date=hoje
        )
        
        # Contar por status
        status_counts = pedidos_hoje.values('status').annotate(
            count=Count('id')
        ).order_by('status')
        
        # Faturamento por hora
        faturamento_hora = pedidos_hoje.filter(
            status__in=['entregue', 'pronto']
        ).extra(
            select={'hora': 'EXTRACT(hour FROM criado_em)'}
        ).values('hora').annotate(
            total=Sum('total')
        ).order_by('hora')
        
        # Pedidos por hora
        pedidos_hora = pedidos_hoje.extra(
            select={'hora': 'EXTRACT(hour FROM criado_em)'}
        ).values('hora').annotate(
            count=Count('id')
        ).order_by('hora')
        
        return JsonResponse({
            'status_counts': list(status_counts),
            'faturamento_hora': list(faturamento_hora),
            'pedidos_hora': list(pedidos_hora),
            'total_pedidos': pedidos_hoje.count(),
            'faturamento_total': pedidos_hoje.filter(
                status__in=['entregue', 'pronto']
            ).aggregate(total=Sum('total'))['total'] or 0
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def dashboard_metricas(request):
    """Dashboard com métricas avançadas"""
    try:
        restaurante = Restaurante.objects.get(proprietario=request.user)
        
        # Últimos 7 dias
        fim = timezone.now().date()
        inicio = fim - timedelta(days=7)
        
        # Pedidos por dia dos últimos 7 dias
        pedidos_por_dia = Pedido.objects.filter(
            restaurante=restaurante,
            criado_em__date__range=[inicio, fim]
        ).extra(
            select={'dia': 'DATE(criado_em)'}
        ).values('dia').annotate(
            pedidos=Count('id'),
            faturamento=Sum('total')
        ).order_by('dia')
        
        # Produtos mais vendidos
        produtos_populares = Pedido.objects.filter(
            restaurante=restaurante,
            criado_em__date__range=[inicio, fim],
            status__in=['entregue', 'pronto']
        ).values(
            'itens__produto__nome'
        ).annotate(
            quantidade=Sum('itens__quantidade')
        ).order_by('-quantidade')[:10]
        
        # Horários de pico
        horarios_pico = Pedido.objects.filter(
            restaurante=restaurante,
            criado_em__date__range=[inicio, fim]
        ).extra(
            select={'hora': 'EXTRACT(hour FROM criado_em)'}
        ).values('hora').annotate(
            pedidos=Count('id')
        ).order_by('-pedidos')[:5]
        
        context = {
            'restaurante': restaurante,
            'pedidos_por_dia': list(pedidos_por_dia),
            'produtos_populares': list(produtos_populares),
            'horarios_pico': list(horarios_pico),
            'title': 'Métricas e Analytics'
        }
        
        return render(request, 'lojista/dashboard_metricas.html', context)
        
    except Restaurante.DoesNotExist:
        messages.error(request, 'Você não possui acesso a nenhum restaurante.')
        return redirect('lojista:dashboard')


def calcular_tempo_medio_pedidos(pedidos_entregues):
    """Calcula tempo médio de entrega dos pedidos"""
    if not pedidos_entregues.exists():
        return 0
    
    tempos = []
    for pedido in pedidos_entregues:
        if pedido.entregue_em and pedido.criado_em:
            tempo_minutos = (pedido.entregue_em - pedido.criado_em).total_seconds() / 60
            tempos.append(tempo_minutos)
    
    if tempos:
        return round(sum(tempos) / len(tempos))
    return 0


@login_required
def criar_pedido_teste(request):
    """Cria um pedido de teste para demonstração"""
    try:
        restaurante = Restaurante.objects.get(proprietario=request.user)
        
        # Criar cliente de teste se não existir
        cliente, created = Cliente.objects.get_or_create(
            telefone='(11) 99999-9999',
            defaults={
                'nome': 'Cliente Teste',
                'email': 'teste@email.com',
                'endereco_rua': 'Rua de Teste',
                'endereco_numero': '123',
                'endereco_bairro': 'Centro',
                'endereco_cidade': 'São Paulo',
                'endereco_estado': 'SP',
                'endereco_cep': '01000-000'
            }
        )
        
        # Criar pedido de teste
        from apps.pedidos.models import Pedido, ItemPedido
        
        pedido = Pedido.objects.create(
            restaurante=restaurante,
            cliente=cliente,
            status='recebido',
            tipo='delivery',
            endereco_entrega_rua=cliente.endereco_rua,
            endereco_entrega_numero=cliente.endereco_numero,
            endereco_entrega_bairro=cliente.endereco_bairro,
            endereco_entrega_cidade=cliente.endereco_cidade,
            endereco_entrega_estado=cliente.endereco_estado,
            endereco_entrega_cep=cliente.endereco_cep,
            subtotal=35.90,
            taxa_entrega=5.00,
            total=40.90,
            forma_pagamento='pix',
            observacoes='Pedido de teste criado automaticamente'
        )
        
        # Adicionar itens de teste se existirem produtos
        produtos = restaurante.produtos.filter(disponivel=True)[:2]
        for i, produto in enumerate(produtos):
            ItemPedido.objects.create(
                pedido=pedido,
                produto=produto,
                quantidade=1 + i,
                preco_unitario=produto.preco
            )
        
        return JsonResponse({
            'success': True,
            'message': f'Pedido de teste #{pedido.numero} criado com sucesso!',
            'order_id': pedido.id
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# Função auxiliar para auto-impressão
def auto_imprimir_pedido(pedido):
    """Auto-imprime pedido se configurado"""
    from .models_impressoras import ConfiguracaoImpressora, LogImpressao
    
    impressoras_auto = ConfiguracaoImpressora.objects.filter(
        restaurante=pedido.restaurante,
        ativa=True,
        auto_imprimir_pedido=True
    )
    
    for impressora in impressoras_auto:
        try:
            # Simular impressão
            log = LogImpressao.objects.create(
                impressora=impressora,
                pedido=pedido,
                tipo_impressao='pedido',
                status='sucesso'
            )
        except Exception as e:
            LogImpressao.objects.create(
                impressora=impressora,
                pedido=pedido,
                tipo_impressao='pedido',
                status='erro',
                mensagem_erro=str(e)
            )
