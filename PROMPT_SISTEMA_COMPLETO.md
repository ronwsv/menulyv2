# PROMPT COMPLETO: Sistema de Delivery Multi-Restaurante (White Label)

## 📋 VISÃO GERAL DO SISTEMA

Crie um sistema completo de delivery multi-restaurante com **mini-sites independentes** para cada lojista, onde cada restaurante possui sua própria URL personalizada (ex: `/pizzaria-do-jose/`, `/hamburgueria-do-joao/`) com design totalmente customizável e funcionalidades completas de e-commerce.

## 🏗️ ARQUITETURA DO SISTEMA

### 🔄 Estrutura Multi-Tenant
- **Super Admin**: Gerencia toda a plataforma e todos os restaurantes
- **Lojistas**: Cada proprietário gerencia seus próprios restaurantes
- **Clientes**: Fazem pedidos através dos mini-sites
- **Sistema White Label**: Cada restaurante tem identidade visual própria

### 🌐 Arquitetura de URLs
```
/                           → Página inicial da plataforma
/restaurantes/              → Lista todos os restaurantes
/superadmin/               → Painel do super administrador
/lojista/                  → Painel do lojista

/{restaurante-slug}/       → Home do mini-site do restaurante
/{restaurante-slug}/checkout/ → Checkout do restaurante
/{restaurante-slug}/sobre/    → Sobre o restaurante
/{restaurante-slug}/pedido-recebido/ → Confirmação do pedido
```

## 🎯 FUNCIONALIDADES PRINCIPAIS

### 1. 🏪 MINI-SITES POR RESTAURANTE
Cada restaurante possui um mini-site completo com:

#### Design Totalmente Customizável:
- **Cores personalizadas**: Primária, secundária, fundo, texto, botões
- **Logo personalizada**: Upload de logo própria
- **Banner principal**: Imagem de destaque do restaurante
- **Favicon**: Ícone personalizado para o navegador
- **Gradientes dinâmicos**: Baseados nas cores do restaurante

#### Páginas do Mini-Site:
- **Home/Cardápio**: Layout premium com categorias, produtos e carrinho
- **Checkout**: Processo completo de finalização de pedido
- **Sobre**: Informações detalhadas do restaurante
- **Confirmação**: Página de sucesso após o pedido

#### Funcionalidades Premium:
- **Carrinho flutuante**: Sempre visível durante a navegação
- **Busca em tempo real**: Filtro de produtos instantâneo
- **Categorias dinâmicas**: Navegação por tipos de produto
- **Produtos em destaque**: Seção especial para promoções
- **Responsivo**: Design adaptável para mobile e desktop

### 2. 🛒 SISTEMA DE PEDIDOS COMPLETO

#### Checkout Avançado:
- **Busca automática de CEP**: Integração com API ViaCEP
- **Opções de entrega**: Delivery ou retirada no local
- **Múltiplas formas de pagamento**: Dinheiro, cartão, PIX
- **Cálculo de troco**: Para pagamento em dinheiro
- **Validação em tempo real**: Formulários inteligentes
- **Resumo do pedido**: Com subtotal, taxa de entrega e total

#### Status do Pedido:
- **Tracking visual**: Barra de progresso do pedido
- **Notificações**: Atualizações em tempo real
- **Histórico completo**: Todos os pedidos do cliente
- **Página de confirmação**: Com detalhes e tempo estimado

### 3. 👨‍💼 PAINEL DO LOJISTA

#### Dashboard Principal:
- **Métricas do dia**: Pedidos, faturamento, produtos mais vendidos
- **Gráficos interativos**: Vendas por período
- **Pedidos em tempo real**: Lista atualizada automaticamente
- **Status dos restaurantes**: Para lojistas com múltiplas unidades

#### Gerenciamento de Produtos:
- **CRUD completo**: Criar, editar, visualizar, deletar produtos
- **Múltiplas imagens**: Até 3 fotos por produto
- **Categorias personalizadas**: Organização do cardápio
- **Opções e adicionais**: Sistema flexível de customização
- **Controle de estoque**: Disponibilidade de produtos
- **Produtos em destaque**: Promoções especiais

#### Gerenciamento de Pedidos:
- **Lista em tempo real**: Todos os pedidos recebidos
- **Atualização de status**: Confirmado → Preparando → Pronto → Entregue
- **Detalhes completos**: Cliente, endereço, itens, pagamento
- **Impressão**: Integração com impressoras térmicas
- **Filtros avançados**: Por data, status, forma de pagamento

#### Configurações do Restaurante:
- **Informações básicas**: Nome, descrição, contato, endereço
- **Horário de funcionamento**: Por dia da semana
- **Delivery**: Taxa, tempo estimado, raio de entrega
- **Visual**: Cores, logo, banner, textos personalizados
- **Impressoras**: Configuração de impressoras térmicas

### 4. 🔧 PAINEL DO SUPER ADMIN

#### Gerenciamento de Lojistas:
- **CRUD de lojistas**: Criar, editar, suspender contas
- **Múltiplos restaurantes**: Um lojista pode ter várias unidades
- **Controle de acesso**: Permissões e limitações por plano
- **Auditoria**: Log de todas as ações dos lojistas

#### Planos e Assinaturas:
- **Planos flexíveis**: Básico, Premium, Enterprise
- **Limitações por plano**: Número de pedidos, produtos, funcionalidades
- **Cobrança**: Controle de vencimentos e pagamentos
- **Trial**: Período experimental para novos lojistas

#### Configurações Globais:
- **Taxa da plataforma**: Porcentagem sobre vendas
- **Configurações de email**: SMTP, templates
- **Integrações**: APIs externas, gateways de pagamento
- **Backup**: Rotinas automáticas de backup

### 5. 🎨 SISTEMA WHITE LABEL

#### Customização Visual:
- **Paleta de cores**: 5 cores principais personalizáveis
- **Tipografia**: Fontes e tamanhos customizáveis
- **Layout**: Templates flexíveis e responsivos
- **Componentes**: Botões, cards, formulários personalizados

#### Branding:
- **Logo**: Upload e posicionamento automático
- **Favicon**: Geração automática em múltiplos tamanhos
- **Meta tags**: SEO otimizado por restaurante
- **Domínio personalizado**: Opcional para planos premium

## 🗄️ MODELO DE DADOS COMPLETO

### Entidades Principais:

#### PlanoMensal
```python
- nome, tipo (básico/premium/enterprise)
- preco_mensal, max_pedidos_mes, max_produtos
- funcionalidades (impressoras, multi_unidades, relatórios, API)
```

#### Restaurante (White Label)
```python
- Informações básicas: nome, slug, cnpj, email, telefone
- Endereço completo: rua, número, bairro, cidade, estado, cep
- Customização visual: cores (primária, secundária, fundo, texto, botões)
- Imagens: logo, banner, favicon
- Textos: slogan, mensagem_boas_vindas, sobre_nos
- Delivery: taxa_entrega, tempo_estimado, raio_entrega
- Horários: funcionamento por dia da semana
- Status: ativo, suspenso, cancelado, trial
- Plano: referência ao plano atual
- Proprietário: lojista responsável
```

#### Produto
```python
- Informações: nome, descrição, preço, categoria
- Imagens: principal + 2 extras
- Configurações: disponível, destaque, ordem
- Extras: calorias, ingredientes, alergênicos, tempo_preparo
```

#### OpcoesProduto + ItemOpcao
```python
- Grupos de opções: Tamanho, Adicionais, Bebidas
- Tipos: seleção única (radio) ou múltipla (checkbox)
- Itens: nome, preço_adicional, disponível
```

#### Pedido + ItemPedido
```python
- Relacionamentos: restaurante, cliente
- Informações: número, status, tipo (delivery/retirada)
- Endereço: completo para entrega
- Valores: subtotal, taxa_entrega, desconto, total
- Pagamento: forma, troco_para
- Tempos: criado_em, confirmado_em, pronto_em, entregue_em
```

#### ConfiguracaoImpressora
```python
- Tipos: térmica, laser, USB, rede
- Conexão: IP, porta, caminho_usb
- Configurações: auto_imprimir, layout, cortar_papel
```

## 🔐 SISTEMA DE AUTENTICAÇÃO

### Middleware de Restaurante:
```python
class RestauranteMiddleware:
    # Detecta automaticamente o restaurante pela URL
    # Injeta request.restaurante_atual em todas as views
    # Permite acesso transparente ao contexto do restaurante
```

### Tipos de Usuário:
- **Super Admin**: Acesso total ao sistema
- **Lojista**: Acesso aos próprios restaurantes
- **Cliente**: Acesso para fazer pedidos

### Controle de Acesso:
- **Por plano**: Limitações baseadas na assinatura
- **Por funcionalidade**: Recursos específicos por nível
- **Por restaurante**: Isolamento total entre lojistas

## 🎨 FRONTEND MODERNO

### Tecnologias:
- **HTML5 + CSS3**: Semântico e acessível
- **Bootstrap 5**: Framework responsivo
- **JavaScript ES6+**: Interatividade moderna
- **Font Awesome**: Ícones profissionais

### Recursos Visuais:
- **Gradientes dinâmicos**: Baseados nas cores do restaurante
- **Animações CSS**: Transições suaves
- **Cards elegantes**: Design material
- **Loading states**: Feedback visual
- **Toast notifications**: Mensagens não intrusivas

### Funcionalidades JavaScript:
- **LocalStorage**: Persistência do carrinho
- **API Integration**: Busca de CEP, envio de pedidos
- **Real-time updates**: Atualizações sem recarregar
- **Form validation**: Validação em tempo real
- **Responsive design**: Adaptação automática

## 📱 INTEGRAÇÃO E APIS

### APIs Externas:
- **ViaCEP**: Busca automática de endereços
- **Firebase**: Notificações push (opcional)
- **WhatsApp**: Links diretos para contato

### APIs Internas:
```
GET /api/restaurantes/          → Lista restaurantes
GET /api/restaurante/{id}/      → Detalhes do restaurante
GET /api/restaurante/{id}/cardapio/ → Produtos e categorias
POST /api/finalizar-pedido/     → Criar novo pedido
PUT /api/pedidos/{id}/status/   → Atualizar status
```

## 🖨️ SISTEMA DE IMPRESSÃO

### Suporte a Impressoras:
- **Térmicas**: 58mm, 80mm
- **USB**: Conexão local
- **Rede**: IP e porta
- **Automática**: Impressão ao receber pedido

### Layouts de Impressão:
- **Pedido completo**: Para balcão
- **Resumo cozinha**: Apenas itens
- **Customizável**: Logo, corte, largura

## 🚀 DEPLOY E INFRAESTRUTURA

### Stack Recomendada:
- **Backend**: Django 5.2+ com Python 3.11+
- **Banco**: PostgreSQL (produção) / SQLite (desenvolvimento)
- **Cache**: Redis para sessões e cache
- **Static**: Nginx para arquivos estáticos
- **Media**: CDN para imagens (AWS S3, Cloudinary)

### Configurações Essenciais:
```python
# settings.py
MIDDLEWARE = [
    'restaurantes.middleware.RestauranteMiddleware',  # CRUCIAL!
    # outros middlewares...
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # configurações...
    }
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

## 📋 REGRAS DE NEGÓCIO

### Lógica de Mini-Sites:
1. **URL Detection**: Middleware detecta restaurante pelo primeiro segmento da URL
2. **Context Injection**: Restaurante disponível em `request.restaurante_atual`
3. **Template Inheritance**: Templates base com customização por restaurante
4. **Isolamento**: Cada restaurante vê apenas seus próprios dados

### Controle de Planos:
1. **Trial**: 30 dias gratuitos para novos lojistas
2. **Limitações**: Baseadas no plano atual
3. **Upgrade/Downgrade**: Mudança de plano a qualquer momento
4. **Suspensão**: Por falta de pagamento

### Fluxo de Pedidos:
1. **Recebido**: Cliente finaliza pedido
2. **Confirmado**: Lojista aceita
3. **Preparando**: Em produção
4. **Pronto**: Aguardando entrega/retirada
5. **Saiu para Entrega**: A caminho
6. **Entregue**: Concluído

## 🎯 FUNCIONALIDADES ESPECÍFICAS

### Carrinho Inteligente:
- **Persistência**: LocalStorage mantém itens
- **Sincronização**: Entre abas do navegador
- **Validação**: Verificação de disponibilidade
- **Cálculos**: Automáticos com taxa de entrega

### Checkout Premium:
- **Multi-step**: Processo dividido em etapas
- **Validação progressiva**: Por seção
- **Auto-complete**: CEP preenche endereço
- **Formatação**: Telefone e outros campos
- **Preview**: Resumo sempre visível

### Dashboard Analytics:
- **Métricas em tempo real**: Vendas do dia
- **Gráficos**: Chart.js para visualizações
- **Comparativos**: Períodos anteriores
- **Exportação**: Relatórios em PDF/Excel

## 🔨 COMANDOS PARA IMPLEMENTAÇÃO

### 1. Estrutura Inicial:
```bash
django-admin startproject backend
cd backend
python manage.py startapp restaurantes
```

### 2. Models Principais:
```python
# restaurantes/models.py
# Implementar todos os models listados acima
```

### 3. Middleware Obrigatório:
```python
# restaurantes/middleware.py
# RestauranteMiddleware para detecção automática
```

### 4. URLs com Slug:
```python
# backend/urls.py
path('<slug:slug>/', include('restaurantes.restaurante_urls')),
```

### 5. Views por Contexto:
```python
# restaurantes/views.py
def menu_view(request, slug=None):
    restaurante = request.restaurante_atual
    # lógica da view...
```

### 6. Templates White Label:
```html
<!-- templates/restaurante/base.html -->
<style>
:root {
    --cor-principal: {{ restaurante.cor_primaria }};
    --cor-secundaria: {{ restaurante.cor_secundaria }};
}
</style>
```

## ✅ CHECKLIST DE IMPLEMENTAÇÃO

### Fase 1 - Core System:
- [ ] Models completos (Restaurante, Produto, Pedido, etc.)
- [ ] RestauranteMiddleware funcionando
- [ ] Sistema de URLs com slug
- [ ] Templates base white label
- [ ] Autenticação multi-nível

### Fase 2 - Mini-Sites:
- [ ] Layout responsivo premium
- [ ] Carrinho com LocalStorage
- [ ] Checkout completo com CEP
- [ ] Página de confirmação
- [ ] Sistema de cores dinâmicas

### Fase 3 - Painel Lojista:
- [ ] Dashboard com métricas
- [ ] CRUD de produtos
- [ ] Gerenciamento de pedidos
- [ ] Configurações do restaurante
- [ ] Upload de imagens

### Fase 4 - Super Admin:
- [ ] Gerenciamento de lojistas
- [ ] Sistema de planos
- [ ] Relatórios globais
- [ ] Configurações do sistema

### Fase 5 - Funcionalidades Avançadas:
- [ ] Impressoras térmicas
- [ ] Notificações push
- [ ] APIs externas
- [ ] Relatórios avançados

## 🎨 EXEMPLO DE IMPLEMENTAÇÃO

### View com Context de Restaurante:
```python
def menu_view(request, slug=None):
    if not request.restaurante_atual:
        return redirect('restaurantes')
    
    restaurante = request.restaurante_atual
    categorias = restaurante.categorias.filter(ativo=True)
    produtos = restaurante.produtos.filter(disponivel=True)
    
    context = {
        'restaurante': restaurante,
        'categorias': categorias,
        'produtos': produtos
    }
    return render(request, 'restaurante/menu-final.html', context)
```

### Template com Cores Dinâmicas:
```html
<style>
:root {
    --cor-principal: {{ restaurante.cor_primaria|default:"#667eea" }};
    --cor-secundaria: {{ restaurante.cor_secundaria|default:"#764ba2" }};
    --cor-botoes: {{ restaurante.cor_botoes|default:"#28a745" }};
}

.hero-section {
    background: linear-gradient(135deg, var(--cor-principal), var(--cor-secundaria));
}
</style>
```

## 🚀 RESULTADO ESPERADO

Um sistema completo onde:
- **Cada restaurante** tem sua própria URL e identidade visual
- **Lojistas** gerenciam independentemente seus negócios
- **Clientes** têm experiência premium de compra
- **Super Admin** controla toda a plataforma
- **Sistema escalável** para centenas de restaurantes
- **Design responsivo** e moderno
- **Performance otimizada** para alta concorrência

Este é um sistema **White Label** completo, onde cada restaurante funciona como um e-commerce independente dentro da mesma plataforma, com toda a infraestrutura compartilhada mas experiência única para cada negócio.
