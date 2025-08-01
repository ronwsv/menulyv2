"""
Context processors globais para o sistema White Label - FASE 2.
"""

def global_context(request):
    """
    Adiciona variáveis globais disponíveis em todos os templates.
    Inclui dados do restaurante, tema e permissões.
    """
    context = {
        'SITE_NAME': 'Menuly',
        'SITE_DESCRIPTION': 'Sistema de Delivery Multi-Restaurante',
    }
    
    # Se há um restaurante atual, adiciona ao contexto
    if hasattr(request, 'restaurante_atual') and request.restaurante_atual:
        restaurante = request.restaurante_atual
        context.update({
            'restaurante': restaurante,
            'is_minisite': getattr(request, 'is_minisite', False),
        })
        
        # Dados do tema (se existir)
        if hasattr(restaurante, 'tema'):
            tema = restaurante.tema
            context.update({
                'tema': tema,
                'tema_css_vars': tema.get_css_variables(),
                'tema_classes': tema.get_tema_classes(),
                'componentes_personalizados': tema.componentes.filter(ativo=True).order_by('ordem'),
            })
        else:
            # Tema padrão se não houver personalização
            context.update({
                'tema': None,
                'tema_css_vars': get_default_theme_vars(),
                'tema_classes': 'tema-moderno',
                'componentes_personalizados': [],
            })
    
    # Utilitários sempre disponíveis
    context.update({
        'can_manage_current_restaurant': (
            request.can_manage_restaurant(request.user) 
            if hasattr(request, 'can_manage_restaurant') and hasattr(request, 'user') 
            else False
        ),
        'user_permissions': getattr(request, 'restaurante_permissions', {}),
    })
        
    return context


def get_default_theme_vars():
    """
    Retorna variáveis CSS padrão quando não há tema personalizado
    """
    return {
        '--cor-primaria': '#007bff',
        '--cor-secundaria': '#6c757d',
        '--cor-fundo': '#ffffff',
        '--cor-texto': '#212529',
        '--cor-botao': '#28a745',
        '--fonte-primaria': 'Roboto, sans-serif',
        '--fonte-secundaria': 'Open Sans, sans-serif',
        '--tamanho-fonte-base': '16px',
        '--largura-maxima': '1200px',
        '--espacamento-geral': '15px',
        '--border-radius': '8px',
    }
