"""
Views para sistema de checkout inteligente com busca por celular.

Implementa o sistema guest inteligente que permite aos clientes
reutilizar dados de pedidos anteriores sem necessidade de cadastro.
"""
from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from apps.accounts.models import Cliente, EnderecoCliente
from apps.restaurantes.models import Restaurante
import json
import re


class BuscarClienteAjaxView(View):
    """
    View AJAX para buscar cliente por celular no checkout.
    
    Retorna dados do cliente, endereços salvos e histórico de pedidos
    para preenchimento automático do formulário.
    """
    
    def post(self, request):
        celular = request.POST.get('celular', '').strip()
        
        # Limpar formatação do celular
        celular_limpo = re.sub(r'\D', '', celular)
        
        if len(celular_limpo) < 10:
            return JsonResponse({
                'found': False,
                'error': 'Celular deve ter pelo menos 10 dígitos'
            })
            
        try:
            # Buscar cliente por celular
            cliente = Cliente.objects.prefetch_related(
                'enderecos',
                'pedido_set'
            ).get(celular=celular_limpo)
            
            # Preparar dados dos endereços
            enderecos = []
            for endereco in cliente.get_enderecos()[:5]:  # Máximo 5 endereços
                enderecos.append({
                    'id': endereco.id,
                    'apelido': endereco.apelido,
                    'endereco': endereco.endereco,
                    'numero': endereco.numero,
                    'complemento': endereco.complemento,
                    'bairro': endereco.bairro,
                    'cidade': endereco.cidade,
                    'estado': endereco.estado,
                    'cep': endereco.cep,
                    'referencia': endereco.referencia,
                    'endereco_completo': endereco.endereco_completo,
                    'vezes_utilizado': endereco.vezes_utilizado,
                })
            
            # Preparar histórico de pedidos (últimos 3)
            ultimos_pedidos = []
            for pedido in cliente.pedido_set.order_by('-criado_em')[:3]:
                ultimos_pedidos.append({
                    'numero': pedido.numero,
                    'data': pedido.criado_em.strftime('%d/%m/%Y'),
                    'valor': str(pedido.total),
                    'status': pedido.get_status_display(),
                    'restaurante': pedido.restaurante.nome if hasattr(pedido, 'restaurante') else 'N/A',
                })
            
            return JsonResponse({
                'found': True,
                'cliente': {
                    'id': cliente.id,
                    'nome': cliente.nome,
                    'email': cliente.email or '',
                    'celular': cliente.celular,
                    'total_pedidos': cliente.total_pedidos,
                    'valor_total_gasto': str(cliente.valor_total_gasto),
                    'ultima_compra': cliente.ultima_compra.strftime('%d/%m/%Y') if cliente.ultima_compra else '',
                },
                'enderecos': enderecos,
                'ultimos_pedidos': ultimos_pedidos,
                'endereco_principal_id': cliente.endereco_principal.id if cliente.endereco_principal else None,
            })
            
        except Cliente.DoesNotExist:
            return JsonResponse({
                'found': False,
                'message': 'Cliente não encontrado. Será criado um novo cadastro.'
            })
        except Exception as e:
            return JsonResponse({
                'found': False,
                'error': f'Erro ao buscar cliente: {str(e)}'
            })


class SalvarEnderecoAjaxView(View):
    """
    View AJAX para salvar endereço do cliente durante o checkout.
    
    Permite que o cliente salve o endereço atual para reutilização futura.
    """
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            # Validar dados obrigatórios
            campos_obrigatorios = ['cliente_id', 'apelido', 'endereco', 'numero', 'bairro', 'cidade', 'estado', 'cep']
            for campo in campos_obrigatorios:
                if not data.get(campo):
                    return JsonResponse({
                        'success': False,
                        'error': f'Campo {campo} é obrigatório'
                    })
            
            cliente = get_object_or_404(Cliente, id=data['cliente_id'])
            
            # Verificar se já existe endereço com mesmo apelido
            endereco_existente = cliente.enderecos.filter(
                apelido=data['apelido'],
                ativo=True
            ).first()
            
            if endereco_existente:
                return JsonResponse({
                    'success': False,
                    'error': f'Já existe um endereço salvo com o nome "{data["apelido"]}"'
                })
            
            # Criar novo endereço
            endereco = EnderecoCliente.objects.create(
                cliente=cliente,
                apelido=data['apelido'],
                endereco=data['endereco'],
                numero=data['numero'],
                complemento=data.get('complemento', ''),
                bairro=data['bairro'],
                cidade=data['cidade'],
                estado=data['estado'],
                cep=data['cep'],
                referencia=data.get('referencia', ''),
            )
            
            # Se é o primeiro endereço, definir como principal
            if not cliente.endereco_principal:
                cliente.endereco_principal = endereco
                cliente.save()
            
            return JsonResponse({
                'success': True,
                'endereco': {
                    'id': endereco.id,
                    'apelido': endereco.apelido,
                    'endereco_completo': endereco.endereco_completo,
                },
                'message': 'Endereço salvo com sucesso!'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Dados JSON inválidos'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Erro ao salvar endereço: {str(e)}'
            })


class FormatarCelularAjaxView(View):
    """
    View AJAX para formatar celular em tempo real.
    """
    
    def post(self, request):
        celular = request.POST.get('celular', '').strip()
        
        # Remover tudo que não é número
        numeros = re.sub(r'\D', '', celular)
        
        # Formatar baseado na quantidade de dígitos
        if len(numeros) <= 10:
            # Formato: (XX) XXXX-XXXX
            formatado = re.sub(r'(\d{2})(\d{4})(\d{4})', r'(\1) \2-\3', numeros)
        else:
            # Formato: (XX) XXXXX-XXXX
            formatado = re.sub(r'(\d{2})(\d{5})(\d{4})', r'(\1) \2-\3', numeros)
        
        return JsonResponse({
            'formatado': formatado,
            'limpo': numeros,
            'valido': len(numeros) >= 10
        })


class ValidarCepAjaxView(View):
    """
    View AJAX para validar e buscar informações do CEP.
    
    Pode ser integrada com APIs de CEP como ViaCEP.
    """
    
    def post(self, request):
        cep = request.POST.get('cep', '').strip()
        
        # Limpar formatação do CEP
        cep_limpo = re.sub(r'\D', '', cep)
        
        if len(cep_limpo) != 8:
            return JsonResponse({
                'valido': False,
                'error': 'CEP deve ter 8 dígitos'
            })
        
        # Formatar CEP
        cep_formatado = f'{cep_limpo[:5]}-{cep_limpo[5:]}'
        
        # Aqui você pode integrar com APIs de CEP
        # Por enquanto, retorna apenas a validação
        return JsonResponse({
            'valido': True,
            'cep_formatado': cep_formatado,
            'cep_limpo': cep_limpo,
            # 'endereco': endereco_da_api,
            # 'bairro': bairro_da_api,
            # 'cidade': cidade_da_api,
            # 'estado': estado_da_api,
        })


@method_decorator(csrf_exempt, name='dispatch')
class CriarClienteGuestView(View):
    """
    View para criar cliente guest durante o checkout.
    
    Cria automaticamente um registro de cliente quando não existe.
    """
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            # Validar dados obrigatórios
            nome = data.get('nome', '').strip()
            celular = data.get('celular', '').strip()
            
            if not nome or not celular:
                return JsonResponse({
                    'success': False,
                    'error': 'Nome e celular são obrigatórios'
                })
            
            # Limpar celular
            celular_limpo = re.sub(r'\D', '', celular)
            
            if len(celular_limpo) < 10:
                return JsonResponse({
                    'success': False,
                    'error': 'Celular inválido'
                })
            
            with transaction.atomic():
                # Verificar se cliente já existe
                cliente, criado = Cliente.objects.get_or_create(
                    celular=celular_limpo,
                    defaults={
                        'nome': nome,
                        'email': data.get('email', '').strip() or None,
                    }
                )
                
                if not criado:
                    # Cliente existe, atualizar dados se necessário
                    if cliente.nome != nome:
                        cliente.nome = nome
                    if data.get('email') and cliente.email != data.get('email'):
                        cliente.email = data.get('email').strip()
                    cliente.save()
                
                return JsonResponse({
                    'success': True,
                    'cliente': {
                        'id': cliente.id,
                        'nome': cliente.nome,
                        'celular': cliente.celular,
                        'email': cliente.email or '',
                        'criado': criado,
                    },
                    'message': 'Cliente criado com sucesso!' if criado else 'Cliente atualizado!'
                })
                
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Dados JSON inválidos'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Erro ao criar cliente: {str(e)}'
            })


class HistoricoPedidosClienteView(View):
    """
    View para buscar histórico completo de pedidos de um cliente.
    """
    
    def get(self, request):
        cliente_id = request.GET.get('cliente_id')
        
        if not cliente_id:
            return JsonResponse({
                'success': False,
                'error': 'ID do cliente é obrigatório'
            })
        
        try:
            cliente = get_object_or_404(Cliente, id=cliente_id)
            
            # Buscar pedidos do cliente (últimos 10)
            pedidos = []
            for pedido in cliente.pedido_set.order_by('-criado_em')[:10]:
                pedidos.append({
                    'numero': pedido.numero,
                    'data': pedido.criado_em.strftime('%d/%m/%Y %H:%M'),
                    'valor': str(pedido.total),
                    'status': pedido.get_status_display(),
                    'restaurante': pedido.restaurante.nome if hasattr(pedido, 'restaurante') else 'N/A',
                    'itens_count': pedido.itens.count() if hasattr(pedido, 'itens') else 0,
                })
            
            return JsonResponse({
                'success': True,
                'cliente': {
                    'nome': cliente.nome,
                    'total_pedidos': cliente.total_pedidos,
                    'valor_total_gasto': str(cliente.valor_total_gasto),
                },
                'pedidos': pedidos
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Erro ao buscar histórico: {str(e)}'
            })
