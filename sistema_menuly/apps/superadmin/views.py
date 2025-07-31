"""
Views do painel do super administrador.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from apps.restaurantes.models import PlanoMensal, Lojista, Restaurante
from apps.pedidos.models import Pedido
import json


@staff_member_required
def dashboard(request):
    """Dashboard principal do super administrador."""
    
    # Estatísticas gerais da plataforma
    hoje = timezone.now().date()
    
    stats = {
        'total_lojistas': Lojista.objects.count(),
        'lojistas_ativos': Lojista.objects.filter(ativo=True).count(),
        'total_restaurantes': Restaurante.objects.count(),
        'restaurantes_ativos': Restaurante.objects.filter(ativo=True).count(),
        'restaurantes_aprovados': Restaurante.objects.filter(aprovado=True).count(),
        'pedidos_hoje': Pedido.objects.filter(criado_em__date=hoje).count(),
        'faturamento_hoje': Pedido.objects.filter(
            criado_em__date=hoje
        ).aggregate(total=Sum('total'))['total'] or 0,
    }
    
    # Lojistas recentes (últimos 10)
    lojistas_recentes = Lojista.objects.order_by('-criado_em')[:10]
    
    # Restaurantes aguardando aprovação
    restaurantes_pendentes = Restaurante.objects.filter(
        aprovado=False, ativo=True
    ).order_by('-criado_em')[:10]
    
    # Dados para gráfico de crescimento (últimos 30 dias)
    crescimento_dados = []
    for i in range(30):
        data = hoje - timedelta(days=i)
        novos_lojistas = Lojista.objects.filter(criado_em__date=data).count()
        novos_restaurantes = Restaurante.objects.filter(criado_em__date=data).count()
        
        crescimento_dados.append({
            'data': data.strftime('%d/%m'),
            'lojistas': novos_lojistas,
            'restaurantes': novos_restaurantes,
        })
    
    crescimento_dados.reverse()  # Ordem cronológica
    
    context = {
        'stats': stats,
        'lojistas_recentes': lojistas_recentes,
        'restaurantes_pendentes': restaurantes_pendentes,
        'crescimento_dados': json.dumps(crescimento_dados),
    }
    
    return render(request, 'superadmin/dashboard.html', context)


@staff_member_required
def lista_lojistas(request):
    """Lista todos os lojistas da plataforma."""
    
    # Filtros
    ativo_filter = request.GET.get('ativo', '')
    plano_filter = request.GET.get('plano', '')
    trial_filter = request.GET.get('trial', '')
    
    # Base query
    lojistas = Lojista.objects.all().select_related('user', 'plano')
    
    # Aplica filtros
    if ativo_filter == 'true':
        lojistas = lojistas.filter(ativo=True)
    elif ativo_filter == 'false':
        lojistas = lojistas.filter(ativo=False)
    
    if plano_filter:
        lojistas = lojistas.filter(plano_id=plano_filter)
    
    if trial_filter == 'true':
        lojistas = lojistas.filter(trial_ativo=True)
    elif trial_filter == 'false':
        lojistas = lojistas.filter(trial_ativo=False)
    
    # Ordena por mais recentes
    lojistas = lojistas.order_by('-criado_em')
    
    context = {
        'lojistas': lojistas,
        'planos': PlanoMensal.objects.filter(ativo=True),
        'filtros': {
            'ativo': ativo_filter,
            'plano': plano_filter,
            'trial': trial_filter,
        }
    }
    
    return render(request, 'superadmin/lista_lojistas.html', context)


@staff_member_required
def detalhes_lojista(request, lojista_id):
    """Exibe detalhes de um lojista específico."""
    lojista = get_object_or_404(Lojista, id=lojista_id)
    
    # Estatísticas do lojista
    restaurantes = lojista.restaurantes.all()
    total_pedidos = Pedido.objects.filter(restaurante__in=restaurantes)
    
    stats = {
        'total_restaurantes': restaurantes.count(),
        'restaurantes_ativos': restaurantes.filter(ativo=True).count(),
        'total_pedidos': total_pedidos.count(),
        'faturamento_total': total_pedidos.aggregate(
            total=Sum('total')
        )['total'] or 0,
    }
    
    # Pedidos recentes
    pedidos_recentes = total_pedidos.order_by('-criado_em')[:10]
    
    context = {
        'lojista': lojista,
        'stats': stats,
        'restaurantes': restaurantes,
        'pedidos_recentes': pedidos_recentes,
    }
    
    return render(request, 'superadmin/detalhes_lojista.html', context)


@staff_member_required
def novo_lojista(request):
    """Criar novo lojista."""
    # TODO: Implementar formulário de criação
    messages.info(request, 'Funcionalidade em desenvolvimento.')
    return redirect('superadmin:lista_lojistas')


@staff_member_required
def editar_lojista(request, lojista_id):
    """Editar lojista."""
    # TODO: Implementar formulário de edição
    messages.info(request, 'Funcionalidade em desenvolvimento.')
    return redirect('superadmin:detalhes_lojista', lojista_id=lojista_id)


@staff_member_required
def suspender_lojista(request, lojista_id):
    """Suspender/reativar lojista."""
    lojista = get_object_or_404(Lojista, id=lojista_id)
    
    if request.method == 'POST':
        lojista.suspenso = not lojista.suspenso
        lojista.save()
        
        action = 'suspenso' if lojista.suspenso else 'reativado'
        messages.success(request, f'Lojista {action} com sucesso.')
    
    return redirect('superadmin:detalhes_lojista', lojista_id=lojista_id)


@staff_member_required
def lista_restaurantes(request):
    """Lista todos os restaurantes da plataforma."""
    
    # Filtros
    ativo_filter = request.GET.get('ativo', '')
    aprovado_filter = request.GET.get('aprovado', '')
    cidade_filter = request.GET.get('cidade', '')
    
    # Base query
    restaurantes = Restaurante.objects.all().select_related('lojista')
    
    # Aplica filtros
    if ativo_filter == 'true':
        restaurantes = restaurantes.filter(ativo=True)
    elif ativo_filter == 'false':
        restaurantes = restaurantes.filter(ativo=False)
    
    if aprovado_filter == 'true':
        restaurantes = restaurantes.filter(aprovado=True)
    elif aprovado_filter == 'false':
        restaurantes = restaurantes.filter(aprovado=False)
    
    if cidade_filter:
        restaurantes = restaurantes.filter(endereco_cidade__icontains=cidade_filter)
    
    # Ordena por mais recentes
    restaurantes = restaurantes.order_by('-criado_em')
    
    context = {
        'restaurantes': restaurantes,
        'filtros': {
            'ativo': ativo_filter,
            'aprovado': aprovado_filter,
            'cidade': cidade_filter,
        }
    }
    
    return render(request, 'superadmin/lista_restaurantes.html', context)


@staff_member_required
def detalhes_restaurante(request, restaurante_id):
    """Exibe detalhes de um restaurante específico."""
    restaurante = get_object_or_404(Restaurante, id=restaurante_id)
    
    # Estatísticas do restaurante
    pedidos = restaurante.pedidos.all()
    
    stats = {
        'total_produtos': restaurante.produtos.count(),
        'produtos_ativos': restaurante.produtos.filter(disponivel=True).count(),
        'total_pedidos': pedidos.count(),
        'faturamento_total': pedidos.aggregate(
            total=Sum('total')
        )['total'] or 0,
    }
    
    context = {
        'restaurante': restaurante,
        'stats': stats,
    }
    
    return render(request, 'superadmin/detalhes_restaurante.html', context)


@staff_member_required
def aprovar_restaurante(request, restaurante_id):
    """Aprovar/reprovar restaurante."""
    restaurante = get_object_or_404(Restaurante, id=restaurante_id)
    
    if request.method == 'POST':
        restaurante.aprovado = not restaurante.aprovado
        restaurante.save()
        
        action = 'aprovado' if restaurante.aprovado else 'reprovado'
        messages.success(request, f'Restaurante {action} com sucesso.')
    
    return redirect('superadmin:detalhes_restaurante', restaurante_id=restaurante_id)


@staff_member_required
def lista_planos(request):
    """Lista todos os planos de assinatura."""
    planos = PlanoMensal.objects.all().order_by('preco_mensal')
    
    context = {
        'planos': planos,
    }
    
    return render(request, 'superadmin/lista_planos.html', context)


@staff_member_required
def novo_plano(request):
    """Criar novo plano."""
    # TODO: Implementar formulário de criação
    messages.info(request, 'Funcionalidade em desenvolvimento.')
    return redirect('superadmin:lista_planos')


@staff_member_required
def editar_plano(request, plano_id):
    """Editar plano."""
    # TODO: Implementar formulário de edição
    messages.info(request, 'Funcionalidade em desenvolvimento.')
    return redirect('superadmin:lista_planos')


@staff_member_required
def relatorios(request):
    """Página principal de relatórios."""
    context = {}
    return render(request, 'superadmin/relatorios.html', context)


@staff_member_required
def relatorio_vendas(request):
    """Relatório de vendas da plataforma."""
    # TODO: Implementar relatório detalhado de vendas
    messages.info(request, 'Funcionalidade em desenvolvimento.')
    return redirect('superadmin:relatorios')


@staff_member_required
def relatorio_lojistas(request):
    """Relatório de performance dos lojistas."""
    # TODO: Implementar relatório de lojistas
    messages.info(request, 'Funcionalidade em desenvolvimento.')
    return redirect('superadmin:relatorios')


@staff_member_required
def configuracoes(request):
    """Configurações globais da plataforma."""
    # TODO: Implementar configurações globais
    messages.info(request, 'Funcionalidade em desenvolvimento.')
    return render(request, 'superadmin/configuracoes.html', {})
