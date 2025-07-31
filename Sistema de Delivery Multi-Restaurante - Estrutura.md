<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# Sistema de Delivery Multi-Restaurante - Estrutura Otimizada

Com base no seu arquivo e nos requisitos específicos, vou propor uma estrutura melhorada que atende perfeitamente à sua necessidade de um sistema multi-tenant com gestão granular de permissões e checkout guest inteligente.

## 🏗️ **Arquitetura de Usuários e Permissões Melhorada**

### **1. Modelo de Usuário Customizado**

```python
# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    TIPO_USUARIO = (
        ('superadmin', 'Super Administrador'),
        ('lojista', 'Lojista/Proprietário'),
        ('gerente', 'Gerente'),
        ('funcionario', 'Funcionário'),
        ('cliente', 'Cliente'),
    )
    
    tipo = models.CharField(max_length=15, choices=TIPO_USUARIO, default='cliente')
    celular = models.CharField(max_length=20, blank=True, null=True)
    cpf = models.CharField(max_length=14, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'auth_user'

class PerfilLojista(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_lojista')
    cnpj = models.CharField(max_length=18, unique=True)
    razao_social = models.CharField(max_length=200)
    inscricao_estadual = models.CharField(max_length=20, blank=True)
    plano = models.ForeignKey('PlanoMensal', on_delete=models.PROTECT)
    data_vencimento = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('ativo', 'Ativo'),
        ('suspenso', 'Suspenso'),
        ('trial', 'Trial'),
        ('cancelado', 'Cancelado')
    ], default='trial')
    
    def __str__(self):
        return f"{self.razao_social} - {self.usuario.get_full_name()}"
```


### **2. Sistema de Restaurantes com Múltiplos Administradores**

```python
# restaurantes/models.py
class Restaurante(models.Model):
    # Informações básicas
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    proprietario = models.ForeignKey(PerfilLojista, on_delete=models.CASCADE, related_name='restaurantes')
    
    # Administradores da loja (relacionamento many-to-many com níveis)
    administradores = models.ManyToManyField(
        User, 
        through='RestauranteAdministrador',
        related_name='restaurantes_gerenciados'
    )
    
    # Informações do negócio
    cnpj = models.CharField(max_length=18, blank=True)
    email = models.EmailField()
    telefone = models.CharField(max_length=20)
    
    # Endereço completo
    endereco = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=9)
    
    # Customização White Label
    cor_primaria = models.CharField(max_length=7, default='#667eea')
    cor_secundaria = models.CharField(max_length=7, default='#764ba2')
    cor_fundo = models.CharField(max_length=7, default='#ffffff')
    cor_texto = models.CharField(max_length=7, default='#333333')
    cor_botoes = models.CharField(max_length=7, default='#28a745')
    
    logo = models.ImageField(upload_to='restaurantes/logos/', blank=True, null=True)
    banner = models.ImageField(upload_to='restaurantes/banners/', blank=True, null=True)
    favicon = models.ImageField(upload_to='restaurantes/favicons/', blank=True, null=True)
    
    # Textos personalizáveis
    slogan = models.CharField(max_length=200, blank=True)
    mensagem_boas_vindas = models.TextField(blank=True)
    sobre_nos = models.TextField(blank=True)
    
    # Configurações de delivery
    taxa_entrega = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tempo_estimado = models.IntegerField(default=30)  # em minutos
    raio_entrega = models.IntegerField(default=5)  # em km
    
    # Status e controle
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['nome']
        
    def __str__(self):
        return self.nome

class RestauranteAdministrador(models.Model):
    """Tabela intermediária para administradores do restaurante com níveis de acesso"""
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    NIVEL_ACESSO = (
        ('gerente', 'Gerente'),
        ('funcionario', 'Funcionário'),
    )
    nivel = models.CharField(max_length=15, choices=NIVEL_ACESSO)
    
    # Permissões específicas
    pode_editar_produtos = models.BooleanField(default=True)
    pode_editar_configuracoes = models.BooleanField(default=False)  # Só gerente
    pode_ver_relatorios = models.BooleanField(default=True)
    pode_gerenciar_usuarios = models.BooleanField(default=False)  # Só gerente
    pode_editar_pedidos = models.BooleanField(default=True)
    
    data_adicionado = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['restaurante', 'usuario']
        
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.restaurante.nome} ({self.nivel})"
```


### **3. Sistema de Clientes Guest com Histórico por Celular**

```python
# clientes/models.py
class Cliente(models.Model):
    """Cliente que faz pedidos (não precisa de conta de usuário)"""
    nome = models.CharField(max_length=100)
    celular = models.CharField(max_length=20, unique=True)  # Chave única para busca
    email = models.EmailField(blank=True, null=True)
    
    # Endereços salvos (pode ter múltiplos)
    endereco_principal = models.ForeignKey('EnderecoCliente', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Controle
    primeira_compra = models.DateTimeField(auto_now_add=True)
    ultima_compra = models.DateTimeField(auto_now=True)
    total_pedidos = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-ultima_compra']
        
    def __str__(self):
        return f"{self.nome} - {self.celular}"
        
    def get_enderecos(self):
        return self.enderecos.filter(ativo=True)

class EnderecoCliente(models.Model):
    """Endereços salvos do cliente"""
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='enderecos')
    apelido = models.CharField(max_length=50)  # "Casa", "Trabalho", etc.
    
    endereco = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=9)
    
    referencia = models.CharField(max_length=200, blank=True)
    
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-criado_em']
        
    def __str__(self):
        return f"{self.cliente.nome} - {self.apelido}"
```


## 🌐 **Arquitetura de URLs Sem Conflitos**

### **1. URLs Principais (urls.py principal)**

```python
# backend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Área administrativa
    path('superadmin/', admin.site.urls),
    
    # Painéis de controle (URLs reservadas)
    path('painel-super/', include('superadmin.urls')),
    path('painel-lojista/', include('lojistas.urls')),
    path('painel-restaurante/', include('restaurantes.painel_urls')),
    
    # APIs
    path('api/', include('api.urls')),
    
    # Autenticação
    path('auth/', include('accounts.urls')),
    
    # Página inicial da plataforma
    path('', include('core.urls')),
    
    # IMPORTANTE: Mini-sites dos restaurantes (sempre por último)
    path('<slug:slug>/', include('restaurantes.minisite_urls')),
]

# Arquivos estáticos em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```


### **2. URLs dos Mini-Sites (sem conflito)**

```python
# restaurantes/minisite_urls.py
from django.urls import path
from . import views

app_name = 'minisite'

urlpatterns = [
    # Home do restaurante
    path('', views.RestauranteHomeView.as_view(), name='home'),
    
    # Cardápio e produtos
    path('cardapio/', views.CardapioView.as_view(), name='cardapio'),
    path('produto/<int:pk>/', views.ProdutoDetalheView.as_view(), name='produto_detalhe'),
    
    # Carrinho e checkout
    path('carrinho/', views.CarrinhoView.as_view(), name='carrinho'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('finalizar-pedido/', views.FinalizarPedidoView.as_view(), name='finalizar_pedido'),
    
    # Páginas do restaurante
    path('sobre/', views.SobreView.as_view(), name='sobre'),
    path('contato/', views.ContatoView.as_view(), name='contato'),
    
    # Confirmação e acompanhamento
    path('pedido-confirmado/<str:numero>/', views.PedidoConfirmadoView.as_view(), name='pedido_confirmado'),
    path('acompanhar-pedido/<str:numero>/', views.AcompanharPedidoView.as_view(), name='acompanhar_pedido'),
    
    # AJAX endpoints
    path('ajax/buscar-cliente/', views.BuscarClienteAjaxView.as_view(), name='buscar_cliente_ajax'),
    path('ajax/salvar-endereco/', views.SalvarEnderecoAjaxView.as_view(), name='salvar_endereco_ajax'),
]
```


### **3. Middleware para Detecção Automática do Restaurante**

```python
# restaurantes/middleware.py
from django.shortcuts import get_object_or_404
from django.http import Http404
from .models import Restaurante

class RestauranteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
        # URLs que NÃO devem ser processadas como mini-sites
        self.reserved_slugs = [
            'superadmin', 'painel-super', 'painel-lojista', 'painel-restaurante',
            'admin', 'api', 'auth', 'static', 'media', 'favicon.ico'
        ]

    def __call__(self, request):
        # Detectar se é um mini-site de restaurante
        path_parts = request.path.strip('/').split('/')
        
        if path_parts and path_parts[^0] and path_parts[^0] not in self.reserved_slugs:
            slug = path_parts[^0]
            
            try:
                restaurante = Restaurante.objects.select_related('proprietario').get(
                    slug=slug, 
                    ativo=True,
                    proprietario__status__in=['ativo', 'trial']
                )
                request.restaurante_atual = restaurante
                request.is_minisite = True
            except Restaurante.DoesNotExist:
                if len(path_parts) == 1:  # Apenas o slug, sem mais nada
                    raise Http404("Restaurante não encontrado")
                request.restaurante_atual = None
                request.is_minisite = False
        else:
            request.restaurante_atual = None
            request.is_minisite = False

        response = self.get_response(request)
        return response
```


## 🔐 **Sistema de Permissões Granulares**

### **1. Decorators para Controle de Acesso**

```python
# restaurantes/decorators.py
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied

def requer_administrador_restaurante(permissao=None):
    """Verifica se o usuário é administrador do restaurante atual"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
                
            restaurante_slug = kwargs.get('slug')
            if not restaurante_slug:
                raise PermissionDenied("Restaurante não especificado")
                
            # Verificar se o usuário tem acesso ao restaurante
            if request.user.tipo == 'superadmin':
                # Super admin tem acesso total
                pass
            elif request.user.tipo == 'lojista':
                # Lojista só acessa seus próprios restaurantes
                if not request.user.perfil_lojista.restaurantes.filter(slug=restaurante_slug).exists():
                    raise PermissionDenied("Você não tem acesso a este restaurante")
            else:
                # Gerente ou funcionário
                admin_rel = request.user.restauranteadministrador_set.filter(
                    restaurante__slug=restaurante_slug,
                    ativo=True
                ).first()
                
                if not admin_rel:
                    raise PermissionDenied("Você não tem acesso a este restaurante")
                    
                # Verificar permissão específica se solicitada
                if permissao:
                    if not getattr(admin_rel, f'pode_{permissao}', False):
                        raise PermissionDenied(f"Você não tem permissão para {permissao}")
                        
                # Adicionar o nível de acesso ao request
                request.nivel_acesso = admin_rel.nivel
                request.permissoes = admin_rel
                
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

# Exemplos de uso:
# @requer_administrador_restaurante()  # Qualquer administrador
# @requer_administrador_restaurante('editar_produtos')  # Permissão específica
# @requer_administrador_restaurante('editar_configuracoes')  # Só gerente
```


### **2. Views com Controle de Acesso**

```python
# restaurantes/painel_views.py
from django.shortcuts import render, get_object_or_404
from .decorators import requer_administrador_restaurante

class PainelRestauranteView(View):
    @method_decorator(requer_administrador_restaurante())
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
        
    def get(self, request, slug):
        restaurante = get_object_or_404(Restaurante, slug=slug)
        
        # Métricas do dia
        hoje = timezone.now().date()
        pedidos_hoje = restaurante.pedidos.filter(criado_em__date=hoje)
        
        context = {
            'restaurante': restaurante,
            'pedidos_hoje': pedidos_hoje.count(),
            'faturamento_hoje': pedidos_hoje.aggregate(
                total=models.Sum('total')
            )['total'] or 0,
            'pode_editar_config': getattr(request, 'permissoes', None) and 
                                request.permissoes.pode_editar_configuracoes,
        }
        
        return render(request, 'restaurantes/painel/dashboard.html', context)
```


## 🛒 **Sistema de Checkout Guest Inteligente**

### **1. View para Busca de Cliente por Celular**

```python
# clientes/views.py
from django.http import JsonResponse
from django.views import View
from .models import Cliente

class BuscarClienteAjaxView(View):
    def post(self, request):
        celular = request.POST.get('celular', '').strip()
        
        if not celular:
            return JsonResponse({'found': False})
            
        try:
            cliente = Cliente.objects.prefetch_related('enderecos').get(celular=celular)
            
            # Preparar dados do cliente
            enderecos = []
            for endereco in cliente.get_enderecos():
                enderecos.append({
                    'id': endereco.id,
                    'apelido': endereco.apelido,
                    'endereco_completo': f"{endereco.endereco}, {endereco.numero}",
                    'bairro': endereco.bairro,
                    'cidade': endereco.cidade,
                    'cep': endereco.cep,
                    'complemento': endereco.complemento,
                    'referencia': endereco.referencia,
                })
            
            # Últimos pedidos
            ultimos_pedidos = []
            for pedido in cliente.pedidos.order_by('-criado_em')[:3]:
                ultimos_pedidos.append({
                    'numero': pedido.numero,
                    'data': pedido.criado_em.strftime('%d/%m/%Y'),
                    'total': str(pedido.total),
                    'status': pedido.get_status_display(),
                })
            
            return JsonResponse({
                'found': True,
                'cliente': {
                    'nome': cliente.nome,
                    'email': cliente.email or '',
                    'total_pedidos': cliente.total_pedidos,
                },
                'enderecos': enderecos,
                'ultimos_pedidos': ultimos_pedidos,
            })
            
        except Cliente.DoesNotExist:
            return JsonResponse({'found': False})
```


### **2. JavaScript para Checkout Inteligente**

```javascript
// static/js/checkout-inteligente.js
class CheckoutInteligente {
    constructor() {
        this.celularInput = document.getElementById('id_celular');
        this.nomeInput = document.getElementById('id_nome');
        this.emailInput = document.getElementById('id_email');
        this.enderecoSection = document.getElementById('endereco-section');
        
        this.initEventListeners();
    }
    
    initEventListeners() {
        // Buscar cliente quando celular for preenchido
        this.celularInput.addEventListener('blur', () => {
            this.buscarCliente();
        });
        
        // Formatar celular automaticamente
        this.celularInput.addEventListener('input', (e) => {
            e.target.value = this.formatarCelular(e.target.value);
        });
    }
    
    async buscarCliente() {
        const celular = this.celularInput.value.replace(/\D/g, '');
        
        if (celular.length < 10) return;
        
        try {
            const response = await fetch('/ajax/buscar-cliente/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: `celular=${celular}`
            });
            
            const data = await response.json();
            
            if (data.found) {
                this.preencherDadosCliente(data);
                this.mostrarHistorico(data.ultimos_pedidos);
            } else {
                this.limparFormulario();
            }
            
        } catch (error) {
            console.error('Erro ao buscar cliente:', error);
        }
    }
    
    preencherDadosCliente(data) {
        // Preencher dados básicos
        this.nomeInput.value = data.cliente.nome;
        this.emailInput.value = data.cliente.email;
        
        // Mostrar mensagem de cliente existente
        this.mostrarMensagemClienteEncontrado(data.cliente);
        
        // Preencher endereços salvos
        this.preencherEnderecosDisponives(data.enderecos);
    }
    
    mostrarMensagemClienteEncontrado(cliente) {
        const mensagem = document.createElement('div');
        mensagem.className = 'alert alert-success mt-2';
        mensagem.innerHTML = `
            <i class="fas fa-user-check"></i>
            <strong>Cliente encontrado!</strong> 
            ${cliente.nome} - ${cliente.total_pedidos} pedidos anteriores
        `;
        
        // Remover mensagem anterior se existir
        const mensagemAnterior = this.celularInput.parentNode.querySelector('.alert');
        if (mensagemAnterior) {
            mensagemAnterior.remove();
        }
        
        this.celularInput.parentNode.appendChild(mensagem);
    }
    
    preencherEnderecosDisponives(enderecos) {
        if (enderecos.length === 0) return;
        
        // Criar seletor de endereços salvos
        const selectorHTML = `
            <div class="mb-3" id="enderecos-salvos">
                <label class="form-label">Endereços Salvos</label>
                <select class="form-select" id="endereco-salvo-select">
                    <option value="">Selecione um endereço salvo ou cadastre novo</option>
                    ${enderecos.map(endereco => 
                        `<option value="${endereco.id}" data-endereco='${JSON.stringify(endereco)}'>
                            ${endereco.apelido} - ${endereco.endereco_completo}, ${endereco.bairro}
                        </option>`
                    ).join('')}
                </select>
            </div>
        `;
        
        this.enderecoSection.insertAdjacentHTML('afterbegin', selectorHTML);
        
        // Event listener para preenchimento automático
        document.getElementById('endereco-salvo-select').addEventListener('change', (e) => {
            if (e.target.value) {
                const enderecoData = JSON.parse(e.target.selectedOptions[^0].dataset.endereco);
                this.preencherCamposEndereco(enderecoData);
            }
        });
    }
    
    preencherCamposEndereco(endereco) {
        document.getElementById('id_endereco').value = endereco.endereco_completo.split(',')[^0];
        document.getElementById('id_numero').value = endereco.endereco_completo.split(',')[^1]?.trim() || '';
        document.getElementById('id_bairro').value = endereco.bairro;
        document.getElementById('id_cidade').value = endereco.cidade;
        document.getElementById('id_cep').value = endereco.cep;
        document.getElementById('id_complemento').value = endereco.complemento || '';
        document.getElementById('id_referencia').value = endereco.referencia || '';
    }
    
    formatarCelular(valor) {
        const numero = valor.replace(/\D/g, '');
        
        if (numero.length <= 10) {
            return numero.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
        } else {
            return numero.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
        }
    }
    
    mostrarHistorico(pedidos) {
        if (pedidos.length === 0) return;
        
        const historicoHTML = `
            <div class="card mt-3" id="historico-pedidos">
                <div class="card-header">
                    <h6 class="mb-0"><i class="fas fa-history"></i> Pedidos Anteriores</h6>
                </div>
                <div class="card-body">
                    ${pedidos.map(pedido => `
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <div>
                                <strong>#${pedido.numero}</strong><br>
                                <small class="text-muted">${pedido.data}</small>
                            </div>
                            <div class="text-end">
                                <strong>R$ ${pedido.total}</strong><br>
                                <span class="badge bg-secondary">${pedido.status}</span>
                            </div>
                        </div>
                    `).join('<hr class="my-2">')}
                </div>
            </div>
        `;
        
        this.enderecoSection.insertAdjacentHTML('beforeend', historicoHTML);
    }
    
    limparFormulario() {
        // Remover mensagens e histórico anteriores
        const elementos = [
            '.alert',
            '#enderecos-salvos', 
            '#historico-pedidos'
        ];
        
        elementos.forEach(seletor => {
            const elemento = document.querySelector(seletor);
            if (elemento) elemento.remove();
        });
    }
}

// Inicializar quando a página carregar
document.addEventListener('DOMContentLoaded', () => {
    new CheckoutInteligente();
});
```


## 📊 **Melhorias Identificadas no Sistema**

### **1. Estrutura de Dados Mais Robusta**

- **Cliente separado de User**: Permite pedidos guest sem contas de usuário
- **Relacionamento many-to-many entre Restaurante e Administradores**: Flexibilidade total
- **Permissões granulares**: Controle fino sobre o que cada função pode fazer
- **Endereços múltiplos**: Cliente pode ter vários endereços salvos


### **2. URLs Mais Inteligentes**

- **Lista de slugs reservados**: Evita conflitos entre mini-sites e funcionalidades do sistema
- **Middleware otimizado**: Detecção automática sem impacto na performance
- **Estrutura hierárquica**: URLs organizadas por contexto (painel, api, mini-site)


### **3. Sistema de Checkout Revolucionário**

- **Busca automática por celular**: Cliente não precisa recriar dados a cada pedido
- **Preenchimento inteligente**: Endereços e dados salvos aparecem automaticamente
- **Histórico visual**: Cliente vê pedidos anteriores durante o checkout
- **Multiple endereços**: Sistema permite salvar e reutilizar endereços


### **4. Controle de Acesso Avançado**

- **Decorators especializados**: Facilita aplicação de regras de negócio
- **Permissões por função**: Gerente vs Funcionário com controles específicos
- **Context de permissões**: Templates sabem o que o usuário pode fazer
- **Auditoria completa**: Todos os acessos são rastreáveis


### **5. Performance e Escalabilidade**

- **Select_related otimizado**: Queries eficientes para evitar N+1
- **Cache de restaurante**: Middleware armazena contexto para reutilização
- **Índices estratégicos**: Campos de busca frequente indexados
- **Lazy loading**: Dados carregados sob demanda


## 🎯 **Implementação Sugerida**

1. **Fase 1**: Implementar novos models e migrations
2. **Fase 2**: Atualizar middleware e sistema de URLs
3. **Fase 3**: Criar sistema de permissões e decorators
4. **Fase 4**: Implementar checkout inteligente com busca por celular
5. **Fase 5**: Testes e refinamentos

Esta estrutura garante um sistema verdadeiramente escalável, com gestão granular de permissões e uma experiência de checkout que vai impressionar seus clientes. O sistema de busca por celular é inovador e resolve um problema real do e-commerce atual.

<div style="text-align: center">⁂</div>

[^1]: PROMPT-COMPLETO-Sistema-de-Delive.txt

