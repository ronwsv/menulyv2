"""
Decorators para controle de acesso granular baseado na estrutura otimizada.

Estes decorators implementam um sistema de permissões flexível que permite
controle fino sobre quem pode fazer o que em cada restaurante.
"""
from functools import wraps
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from apps.restaurantes.models import Restaurante
from apps.core.middleware import get_user_permissions_for_restaurante


def requer_administrador_restaurante(permissao=None, redirect_url=None):
    """
    Verifica se o usuário é administrador do restaurante atual.
    
    Args:
        permissao (str): Permissão específica requerida (ex: 'editar_produtos')
        redirect_url (str): URL para redirecionamento em caso de erro
    
    Uso:
        @requer_administrador_restaurante()  # Qualquer administrador
        @requer_administrador_restaurante('editar_produtos')  # Permissão específica
        @requer_administrador_restaurante('editar_configuracoes')  # Só gerente/lojista
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            # Obter slug do restaurante
            restaurante_slug = kwargs.get('slug')
            if not restaurante_slug:
                # Tentar obter do request se disponível
                if hasattr(request, 'restaurante_atual') and request.restaurante_atual:
                    restaurante = request.restaurante_atual
                else:
                    raise PermissionDenied("Restaurante não especificado")
            else:
                restaurante = get_object_or_404(Restaurante, slug=restaurante_slug, ativo=True)
            
            user = request.user
            user_tipo = getattr(user, 'tipo', 'cliente')
            
            # Verificar se o usuário tem acesso ao restaurante
            if user_tipo == 'superadmin':
                # Super admin tem acesso total
                request.user_permissions = {
                    'pode_editar_produtos': True,
                    'pode_editar_configuracoes': True,
                    'pode_ver_relatorios': True,
                    'pode_gerenciar_usuarios': True,
                    'pode_editar_pedidos': True,
                    'pode_configurar_impressoras': True,
                    'pode_ver_financeiro': True,
                }
                
            elif user_tipo == 'lojista':
                # Lojista só acessa seus próprios restaurantes
                try:
                    if not user.lojista.restaurantes.filter(slug=restaurante_slug).exists():
                        if redirect_url:
                            messages.error(request, 'Você não tem acesso a este restaurante.')
                            return redirect(redirect_url)
                        raise PermissionDenied("Você não tem acesso a este restaurante")
                    
                    # Lojista tem todas as permissões
                    request.user_permissions = {
                        'pode_editar_produtos': True,
                        'pode_editar_configuracoes': True,
                        'pode_ver_relatorios': True,
                        'pode_gerenciar_usuarios': True,
                        'pode_editar_pedidos': True,
                        'pode_configurar_impressoras': True,
                        'pode_ver_financeiro': True,
                    }
                except AttributeError:
                    if redirect_url:
                        messages.error(request, 'Perfil de lojista não encontrado.')
                        return redirect(redirect_url)
                    raise PermissionDenied("Perfil de lojista não encontrado")
                    
            else:
                # Gerente ou funcionário
                try:
                    admin_rel = restaurante.restauranteadministrador_set.filter(
                        usuario=user,
                        ativo=True
                    ).first()
                    
                    if not admin_rel:
                        if redirect_url:
                            messages.error(request, 'Você não tem acesso a este restaurante.')
                            return redirect(redirect_url)
                        raise PermissionDenied("Você não tem acesso a este restaurante")
                        
                    # Armazenar permissões no request
                    request.user_permissions = {
                        'pode_editar_produtos': admin_rel.pode_editar_produtos,
                        'pode_editar_configuracoes': admin_rel.pode_editar_configuracoes,
                        'pode_ver_relatorios': admin_rel.pode_ver_relatorios,
                        'pode_gerenciar_usuarios': admin_rel.pode_gerenciar_usuarios,
                        'pode_editar_pedidos': admin_rel.pode_editar_pedidos,
                        'pode_configurar_impressoras': admin_rel.pode_configurar_impressoras,
                        'pode_ver_financeiro': admin_rel.pode_ver_financeiro,
                    }
                    
                    # Adicionar informações do nível de acesso
                    request.nivel_acesso = admin_rel.nivel
                    request.admin_rel = admin_rel
                    
                except Exception as e:
                    if redirect_url:
                        messages.error(request, 'Erro ao verificar permissões.')
                        return redirect(redirect_url)
                    raise PermissionDenied("Erro ao verificar permissões")
            
            # Verificar permissão específica se solicitada
            if permissao:
                permissao_key = f'pode_{permissao}'
                if not request.user_permissions.get(permissao_key, False):
                    if redirect_url:
                        messages.error(request, f'Você não tem permissão para {permissao.replace("_", " ")}.')
                        return redirect(redirect_url)
                    raise PermissionDenied(f"Você não tem permissão para {permissao}")
            
            # Adicionar restaurante ao request se ainda não tiver
            if not hasattr(request, 'restaurante_atual'):
                request.restaurante_atual = restaurante
                
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def requer_permissao(permissao, redirect_url=None):
    """
    Decorator mais simples que apenas verifica uma permissão específica.
    
    Args:
        permissao (str): Nome da permissão (ex: 'editar_produtos')
        redirect_url (str): URL para redirecionamento em caso de erro
    """
    return requer_administrador_restaurante(permissao=permissao, redirect_url=redirect_url)


def requer_lojista_ou_gerente(redirect_url=None):
    """
    Decorator que permite acesso apenas para lojistas ou gerentes.
    
    Args:
        redirect_url (str): URL para redirecionamento em caso de erro
    """
    def decorator(view_func):
        @wraps(view_func)
        @requer_administrador_restaurante(redirect_url=redirect_url)
        def wrapper(request, *args, **kwargs):
            user_tipo = getattr(request.user, 'tipo', 'cliente')
            
            # Superadmin sempre pode
            if user_tipo == 'superadmin':
                return view_func(request, *args, **kwargs)
            
            # Lojista sempre pode
            elif user_tipo == 'lojista':
                return view_func(request, *args, **kwargs)
            
            # Funcionários com nível gerente podem
            elif user_tipo in ['gerente', 'funcionario']:
                if hasattr(request, 'nivel_acesso') and request.nivel_acesso == 'gerente':
                    return view_func(request, *args, **kwargs)
                else:
                    if redirect_url:
                        messages.error(request, 'Acesso restrito a gerentes.')
                        return redirect(redirect_url)
                    raise PermissionDenied("Acesso restrito a gerentes")
            
            else:
                if redirect_url:
                    messages.error(request, 'Acesso não autorizado.')
                    return redirect(redirect_url)
                raise PermissionDenied("Acesso não autorizado")
                
        return wrapper
    return decorator


def requer_lojista_apenas(redirect_url=None):
    """
    Decorator que permite acesso apenas para lojistas proprietários.
    
    Args:
        redirect_url (str): URL para redirecionamento em caso de erro
    """
    def decorator(view_func):
        @wraps(view_func)
        @requer_administrador_restaurante(redirect_url=redirect_url)
        def wrapper(request, *args, **kwargs):
            user_tipo = getattr(request.user, 'tipo', 'cliente')
            
            # Superadmin sempre pode
            if user_tipo == 'superadmin':
                return view_func(request, *args, **kwargs)
            
            # Apenas lojista proprietário pode
            elif user_tipo == 'lojista':
                return view_func(request, *args, **kwargs)
            
            else:
                if redirect_url:
                    messages.error(request, 'Acesso restrito ao proprietário.')
                    return redirect(redirect_url)
                raise PermissionDenied("Acesso restrito ao proprietário")
                
        return wrapper
    return decorator


class PermissionRequiredMixin:
    """
    Mixin para views baseadas em classe com controle de permissões.
    
    Uso:
        class MinhaView(PermissionRequiredMixin, View):
            permission_required = 'editar_produtos'
            redirect_url = 'lojista:dashboard'
    """
    permission_required = None
    redirect_url = None
    
    def dispatch(self, request, *args, **kwargs):
        # Aplicar decorator
        if self.permission_required:
            decorator = requer_permissao(self.permission_required, self.redirect_url)
        else:
            decorator = requer_administrador_restaurante(redirect_url=self.redirect_url)
            
        decorated_dispatch = decorator(super().dispatch)
        return decorated_dispatch(request, *args, **kwargs)


# Decorators de conveniência para uso comum
editar_produtos = requer_permissao('editar_produtos')
editar_configuracoes = requer_permissao('editar_configuracoes')
ver_relatorios = requer_permissao('ver_relatorios')
gerenciar_usuarios = requer_permissao('gerenciar_usuarios')
editar_pedidos = requer_permissao('editar_pedidos')
configurar_impressoras = requer_permissao('configurar_impressoras')
ver_financeiro = requer_permissao('ver_financeiro')


def usuario_pode_acessar_restaurante(user, restaurante):
    """
    Função utilitária para verificar se um usuário pode acessar um restaurante.
    
    Args:
        user: Usuário a ser verificado
        restaurante: Restaurante a ser verificado
        
    Returns:
        bool: True se pode acessar, False caso contrário
    """
    if not user.is_authenticated:
        return False
    
    user_tipo = getattr(user, 'tipo', 'cliente')
    
    if user_tipo == 'superadmin':
        return True
    
    elif user_tipo == 'lojista':
        try:
            return user.lojista.restaurantes.filter(id=restaurante.id).exists()
        except:
            return False
    
    elif user_tipo in ['gerente', 'funcionario']:
        try:
            return restaurante.restauranteadministrador_set.filter(
                usuario=user,
                ativo=True
            ).exists()
        except:
            return False
    
    return False
