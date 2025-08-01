"""
Middleware simplificado para detectar restaurantes por slug.
"""
from django.http import Http404
from apps.restaurantes.models import Restaurante


class RestauranteMiddleware:
    """
    Middleware simplificado que detecta o restaurante atual baseado no slug da URL.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # URLs reservadas básicas
        self.reserved_slugs = [
            'admin', 'api', 'static', 'media', 'superadmin', 'lojista', 
            'restaurantes', 'accounts', 'auth', 'login', 'logout'
        ]

    def __call__(self, request):
        # Detecta o restaurante
        print(f"[MIDDLEWARE] Processando: {request.path_info}")
        self.detect_restaurante(request)
        
        response = self.get_response(request)
        return response

    def detect_restaurante(self, request):
        """Detecta qual restaurante está sendo acessado."""
        print(f"[DEBUG] Middleware executado para: {request.path_info}")
        
        # Inicializa valores padrão
        request.restaurante_atual = None
        request.is_minisite = False
        
        # Pega o path da URL
        path = request.path_info.strip('/')
        print(f"[DEBUG] Path processado: '{path}'")
        
        # Se path está vazio, é a home da plataforma
        if not path:
            print("[DEBUG] Path vazio - home da plataforma")
            return
            
        # Separa o path em segmentos
        segments = path.split('/')
        print(f"[DEBUG] Segmentos: {segments}")
        
        # Se não tem segmentos válidos, não é um mini-site
        if not segments or not segments[0]:
            print("[DEBUG] Sem segmentos válidos")
            return
            
        # Primeiro segmento é o possível slug do restaurante
        possible_slug = segments[0].lower()
        print(f"[DEBUG] Possível slug: '{possible_slug}'")
        
        # Se é uma URL reservada, não busca restaurante
        if possible_slug in self.reserved_slugs:
            print(f"[DEBUG] Slug reservado: {possible_slug}")
            return
            
        # Busca o restaurante
        try:
            restaurante = Restaurante.objects.get(
                slug=possible_slug,
                ativo=True
            )
            
            # Se encontrou, define no request
            request.restaurante_atual = restaurante
            request.is_minisite = True
            
            # Debug para verificar se está funcionando
            print(f"[DEBUG] Restaurante encontrado: {restaurante.nome}")
            
        except Restaurante.DoesNotExist:
            # Debug para verificar o que está acontecendo
            print(f"[DEBUG] Restaurante não encontrado para slug: {possible_slug}")
            
            # Se é apenas o slug (sem sub-páginas), retorna 404
            if len(segments) == 1:
                raise Http404("Restaurante não encontrado")
