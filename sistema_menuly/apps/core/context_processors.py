"""
Context processors globais para o sistema.
"""

def global_context(request):
    """
    Adiciona variáveis globais disponíveis em todos os templates.
    """
    context = {
        'SITE_NAME': 'Menuly',
        'SITE_DESCRIPTION': 'Sistema de Delivery Multi-Restaurante',
    }
    
    # Se há um restaurante atual, adiciona ao contexto
    if hasattr(request, 'restaurante_atual') and request.restaurante_atual:
        context['restaurante'] = request.restaurante_atual
        
    return context
