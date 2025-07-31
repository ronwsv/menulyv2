"""
URL configuration for backend project.

Sistema de Delivery Multi-Restaurante (White Label)
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin principal
    path('admin/', admin.site.urls),
    
    # Páginas principais da plataforma
    path('', include('apps.core.urls')),
    
    # Super Admin
    path('superadmin/', include('apps.superadmin.urls')),
    
    # Painel do Lojista
    path('lojista/', include('apps.lojistas.urls')),
    
    # API endpoints
    path('api/', include('apps.pedidos.api_urls')),
    
    # Mini-sites dos restaurantes (DEVE SER O ÚLTIMO!)
    # Esta linha captura qualquer slug e direciona para o mini-site
    path('<slug:slug>/', include('apps.restaurantes.restaurante_urls')),
]

# Configuração para servir arquivos estáticos e media em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
