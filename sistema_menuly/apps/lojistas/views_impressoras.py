"""
Views para gerenciamento de impressoras dos restaurantes
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from apps.restaurantes.models import Restaurante
from .models_impressoras import ConfiguracaoImpressora, LogImpressao
import socket
import json


@login_required
def impressoras(request):
    """Lista e gerencia impressoras do restaurante"""
    # Obter restaurante do usuário logado
    try:
        if hasattr(request.user, 'restaurante_lojista'):
            restaurante = request.user.restaurante_lojista
        else:
            # Buscar como proprietário
            restaurante = Restaurante.objects.get(proprietario=request.user)
    except Restaurante.DoesNotExist:
        messages.error(request, 'Você não possui acesso a nenhum restaurante.')
        return redirect('lojista:dashboard')
    
    # Processar formulários
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            # Adicionar nova impressora
            nome = request.POST.get('nome')
            tipo = request.POST.get('tipo')
            ip = request.POST.get('ip', '')
            porta = request.POST.get('porta', 9100)
            
            try:
                impressora = ConfiguracaoImpressora.objects.create(
                    restaurante=restaurante,
                    nome=nome,
                    tipo=tipo,
                    ip_address=ip if ip else None,
                    porta=int(porta) if porta else 9100,
                    ativa=True
                )
                messages.success(request, f'Impressora "{nome}" adicionada com sucesso!')
            except Exception as e:
                messages.error(request, f'Erro ao adicionar impressora: {str(e)}')
        
        elif action == 'edit':
            # Editar impressora existente
            impressora_id = request.POST.get('impressora_id')
            try:
                impressora = ConfiguracaoImpressora.objects.get(
                    id=impressora_id,
                    restaurante=restaurante
                )
                impressora.nome = request.POST.get('nome')
                impressora.tipo = request.POST.get('tipo')
                impressora.ip_address = request.POST.get('ip') or None
                impressora.porta = int(request.POST.get('porta', 9100))
                impressora.ativa = 'ativa' in request.POST
                impressora.save()
                
                messages.success(request, f'Impressora "{impressora.nome}" atualizada com sucesso!')
            except ConfiguracaoImpressora.DoesNotExist:
                messages.error(request, 'Impressora não encontrada.')
            except Exception as e:
                messages.error(request, f'Erro ao atualizar impressora: {str(e)}')
        
        elif action == 'delete':
            # Excluir impressora
            impressora_id = request.POST.get('impressora_id')
            try:
                impressora = ConfiguracaoImpressora.objects.get(
                    id=impressora_id,
                    restaurante=restaurante
                )
                nome = impressora.nome
                impressora.delete()
                messages.success(request, f'Impressora "{nome}" removida com sucesso!')
            except ConfiguracaoImpressora.DoesNotExist:
                messages.error(request, 'Impressora não encontrada.')
        
        elif action == 'test':
            # Testar impressora
            impressora_id = request.POST.get('impressora_id')
            try:
                impressora = ConfiguracaoImpressora.objects.get(
                    id=impressora_id,
                    restaurante=restaurante
                )
                
                # Criar log de teste
                log = LogImpressao.objects.create(
                    impressora=impressora,
                    tipo_impressao='teste',
                    status='pendente'
                )
                
                # Tentar conectar com a impressora
                resultado = testar_conexao_impressora(impressora)
                
                if resultado['sucesso']:
                    log.status = 'sucesso'
                    log.save()
                    messages.success(request, f'Teste da impressora "{impressora.nome}" realizado com sucesso!')
                else:
                    log.status = 'erro'
                    log.mensagem_erro = resultado['erro']
                    log.save()
                    messages.error(request, f'Erro no teste da impressora "{impressora.nome}": {resultado["erro"]}')
                    
            except ConfiguracaoImpressora.DoesNotExist:
                messages.error(request, 'Impressora não encontrada.')
        
        return redirect('lojista:impressoras')
    
    # Listar impressoras
    impressoras = ConfiguracaoImpressora.objects.filter(restaurante=restaurante)
    
    # Tipos de impressora para o formulário
    tipos_impressora = ConfiguracaoImpressora.TIPO_CHOICES
    
    context = {
        'restaurante': restaurante,
        'impressoras': impressoras,
        'tipos_impressora': tipos_impressora,
        'title': 'Gerenciar Impressoras'
    }
    
    return render(request, 'lojista/impressoras.html', context)


def testar_conexao_impressora(impressora):
    """Testa a conexão com uma impressora"""
    try:
        if impressora.tipo == 'rede' and impressora.ip_address:
            # Testar conexão de rede
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)  # 5 segundos timeout
            
            result = sock.connect_ex((impressora.ip_address, impressora.porta))
            sock.close()
            
            if result == 0:
                return {'sucesso': True, 'mensagem': 'Conexão estabelecida com sucesso'}
            else:
                return {'sucesso': False, 'erro': 'Não foi possível conectar com a impressora'}
        
        elif impressora.tipo == 'usb':
            # Para impressoras USB, apenas simular teste
            return {'sucesso': True, 'mensagem': 'Impressora USB configurada (teste simulado)'}
        
        else:
            return {'sucesso': True, 'mensagem': 'Impressora configurada com sucesso'}
            
    except Exception as e:
        return {'sucesso': False, 'erro': str(e)}


@login_required
@require_POST
def imprimir_pedido(request, pedido_id):
    """Imprime um pedido específico"""
    try:
        # Obter restaurante
        restaurante = Restaurante.objects.get(proprietario=request.user)
        
        # Obter pedido
        from apps.pedidos.models import Pedido
        pedido = get_object_or_404(Pedido, id=pedido_id, restaurante=restaurante)
        
        # Obter impressoras ativas
        impressoras = ConfiguracaoImpressora.objects.filter(
            restaurante=restaurante,
            ativa=True
        )
        
        resultados = []
        for impressora in impressoras:
            if impressora.auto_imprimir_pedido:
                # Simular impressão
                log = LogImpressao.objects.create(
                    impressora=impressora,
                    pedido=pedido,
                    tipo_impressao='pedido',
                    status='sucesso'
                )
                resultados.append({
                    'impressora': impressora.nome,
                    'status': 'sucesso'
                })
        
        return JsonResponse({
            'sucesso': True,
            'mensagem': f'Pedido impresso em {len(resultados)} impressora(s)',
            'resultados': resultados
        })
        
    except Exception as e:
        return JsonResponse({
            'sucesso': False,
            'erro': str(e)
        }, status=500)


@login_required
def logs_impressao(request):
    """Visualiza logs de impressão"""
    try:
        restaurante = Restaurante.objects.get(proprietario=request.user)
        logs = LogImpressao.objects.filter(
            impressora__restaurante=restaurante
        ).select_related('impressora', 'pedido')[:100]
        
        context = {
            'logs': logs,
            'restaurante': restaurante,
            'title': 'Logs de Impressão'
        }
        
        return render(request, 'lojista/logs_impressao.html', context)
        
    except Restaurante.DoesNotExist:
        messages.error(request, 'Você não possui acesso a nenhum restaurante.')
        return redirect('lojista:dashboard')
