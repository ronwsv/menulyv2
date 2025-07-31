"""
Middleware crucial para o sistema White Label - Estrutura Otimizada.

Este middleware detecta automaticamente qual restaurante está sendo acessado
baseado no slug da URL e injeta o restaurante no request para todas as views.
Inclui sistema de cache e permissões granulares.
"""
from django.shortcuts import get_object_or_404
from django.urls import resolve
from django.http import Http404
from django.core.cache import cache
from apps.restaurantes.models import Restaurante


class RestauranteMiddleware:
    """
    Middleware que detecta o restaurante atual baseado no slug da URL.
    
    Funcionalidades OTIMIZADAS:
    - Analisa a URL para extrair o slug do restaurante
    - Sistema de cache para performance
    - URLs reservadas para evitar conflitos
    - Verifica status do lojista e plano
    - Injeta contexto completo do restaurante
    - Permite isolamento completo entre restaurantes
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # URLs que NÃO devem ser processadas como mini-sites
        self.reserved_slugs = [
            'superadmin', 'painel-super', 'painel-lojista', 'painel-restaurante',
            'admin', 'api', 'auth', 'static', 'media', 'favicon.ico', 'robots.txt',
            'sitemap.xml', 'lojista', 'lojistas', 'accounts', 'core'
        ]

    def __call__(self, request):
        # Detecta o restaurante antes de processar a view
        self.detect_restaurante(request)
        
        response = self.get_response(request)
        return response

    def detect_restaurante(self, request):
        """
        Detecta qual restaurante está sendo acessado baseado na URL.
        
        URLs que devem ter restaurante:
        - /{slug}/
        - /{slug}/checkout/
        - /{slug}/sobre/
        - /{slug}/pedido-recebido/
        
        URLs que NÃO devem ter restaurante:
        - /
        - /restaurantes/
        - /lojista/
        - /superadmin/
        - /admin/
        """
        # Inicializa valores padrão
        request.restaurante_atual = None
        request.is_minisite = False
        
        # Pega o path da URL
        path = request.path_info.strip('/')
        
        # Se path está vazio, é a home da plataforma
        if not path:
            return
            
        # Separa o path em segmentos
        segments = path.split('/')
        
        # Se não tem segmentos, não é um mini-site
        if not segments or not segments[0]:
            return
            
        # Primeiro segmento é o possível slug do restaurante
        possible_slug = segments[0]
        
        # Se é uma URL reservada, não busca restaurante
        if possible_slug in self.reserved_slugs:
            return
            
        # Verificar cache primeiro
        cache_key = f'restaurante_slug_{possible_slug}'
        restaurante = cache.get(cache_key)
        
        if restaurante is None:
            # Tenta encontrar o restaurante pelo slug
            try:
                restaurante = Restaurante.objects.select_related(
                    'lojista', 
                    'lojista__plano'
                ).get(
                    slug=possible_slug, 
                    ativo=True,
                    lojista__ativo=True,
                    lojista__suspenso=False
                )
                
                # Cache por 5 minutos
                cache.set(cache_key, restaurante, 300)
                
            except Restaurante.DoesNotExist:
                # Se é apenas o slug sem mais nada, é 404
                if len(segments) == 1:
                    raise Http404("Restaurante não encontrado")
                # Senão, deixa passar para outras URLs
                return
        
        if restaurante:
            # Verificar se o lojista tem plano ativo (se usar o novo sistema)
            try:
                if hasattr(restaurante.lojista, 'perfil_lojista'):
                    perfil = restaurante.lojista.perfil_lojista
                    if not perfil.esta_ativo:
                        raise Http404("Restaurante temporariamente indisponível")
            except:
                # Compatibilidade com sistema antigo
                pass
            
            request.restaurante_atual = restaurante
            request.is_minisite = True
            
            # Adicionar informações úteis ao contexto
            request.restaurante_config = {
                'nome': restaurante.nome,
                'cores': {
                    'primaria': restaurante.cor_primaria,
                    'secundaria': restaurante.cor_secundaria,
                    'fundo': restaurante.cor_fundo,
                    'texto': restaurante.cor_texto,
                    'botoes': restaurante.cor_botoes,
                },
                'contato': {
                    'telefone': restaurante.telefone,
                    'whatsapp': getattr(restaurante, 'whatsapp', ''),
                    'email': restaurante.email,
                },
                'endereco': restaurante.endereco_completo,
                'delivery': {
                    'taxa': restaurante.taxa_entrega,
                    'tempo': restaurante.tempo_estimado,
                    'raio': getattr(restaurante, 'raio_entrega', 5),
                }
            }


def get_user_restaurantes(user):
    """
    Função utilitária para obter restaurantes que um usuário pode acessar.
    
    Retorna diferentes restaurantes baseado no tipo de usuário:
    - Superadmin: Todos os restaurantes
    - Lojista: Apenas seus restaurantes
    - Gerente/Funcionário: Restaurantes onde é administrador
    """
    if not user.is_authenticated:
        return Restaurante.objects.none()
    
    user_tipo = getattr(user, 'tipo', 'cliente')
    
    if user_tipo == 'superadmin':
        return Restaurante.objects.all()
    
    elif user_tipo == 'lojista':
        try:
            return user.lojista.restaurantes.all()
        except:
            return Restaurante.objects.none()
    
    elif user_tipo in ['gerente', 'funcionario']:
        return Restaurante.objects.filter(
            administradores=user,
            restauranteadministrador__ativo=True
        ).distinct()
    
    else:
        return Restaurante.objects.none()


def get_user_permissions_for_restaurante(user, restaurante):
    """
    Função utilitária para obter permissões de um usuário em um restaurante específico.
    
    Retorna um dicionário com as permissões do usuário para o restaurante.
    """
    if not user.is_authenticated:
        return {}
    
    user_tipo = getattr(user, 'tipo', 'cliente')
    
    # Superadmin tem todas as permissões
    if user_tipo == 'superadmin':
        return {
            'pode_editar_produtos': True,
            'pode_editar_configuracoes': True,
            'pode_ver_relatorios': True,
            'pode_gerenciar_usuarios': True,
            'pode_editar_pedidos': True,
            'pode_configurar_impressoras': True,
            'pode_ver_financeiro': True,
        }
    
    # Lojista proprietário tem todas as permissões
    elif user_tipo == 'lojista':
        try:
            if user.lojista.restaurantes.filter(id=restaurante.id).exists():
                return {
                    'pode_editar_produtos': True,
                    'pode_editar_configuracoes': True,
                    'pode_ver_relatorios': True,
                    'pode_gerenciar_usuarios': True,
                    'pode_editar_pedidos': True,
                    'pode_configurar_impressoras': True,
                    'pode_ver_financeiro': True,
                }
        except:
            pass
    
    # Gerente ou funcionário - verificar permissões específicas
    elif user_tipo in ['gerente', 'funcionario']:
        try:
            admin_rel = restaurante.restauranteadministrador_set.filter(
                usuario=user,
                ativo=True
            ).first()
            
            if admin_rel:
                return {
                    'pode_editar_produtos': admin_rel.pode_editar_produtos,
                    'pode_editar_configuracoes': admin_rel.pode_editar_configuracoes,
                    'pode_ver_relatorios': admin_rel.pode_ver_relatorios,
                    'pode_gerenciar_usuarios': admin_rel.pode_gerenciar_usuarios,
                    'pode_editar_pedidos': admin_rel.pode_editar_pedidos,
                    'pode_configurar_impressoras': admin_rel.pode_configurar_impressoras,
                    'pode_ver_financeiro': admin_rel.pode_ver_financeiro,
                    'nivel': admin_rel.nivel,
                }
        except:
            pass
    
    # Sem permissões por padrão
    return {}
