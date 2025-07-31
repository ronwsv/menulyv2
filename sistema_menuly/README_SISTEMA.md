# 🚀 SISTEMA MENULY - DELIVERY MULTI-RESTAURANTE

## 📋 COMO USAR O SISTEMA

### 1. Iniciar o Sistema
Execute o arquivo: `iniciar_sistema.bat`

O servidor será iniciado em: http://localhost:8000/

---

## 🔑 CREDENCIAIS DE ACESSO

### 👑 SUPER USUÁRIO (Django Admin)
- **Usuário:** `admin`
- **Senha:** `admin123`
- **URL:** http://localhost:8000/admin/
- **Função:** Acesso total ao Django Admin (usuários, grupos, dados)

### 🏢 SUPER ADMIN (Painel Administrativo)
- **Usuário:** `admin`
- **Senha:** `admin123`
- **URL:** http://localhost:8000/superadmin/
- **Função:** Dashboard administrativo da plataforma, gestão de lojistas e restaurantes

### 🏪 LOJISTA (Dono dos Restaurantes)
- **Usuário:** `lojista_teste`
- **Senha:** `lojista123`
- **URL:** http://localhost:8000/lojista/
- **Função:** Gerenciar restaurantes, produtos, pedidos e configurações

### 👤 CLIENTE
- **Status:** Cliente de exemplo criado para testes
- **Nome:** Maria Santos
- **Telefone:** (11) 98765-4321
- **Email:** cliente@teste.com
- **Como usar:** 
  - Use os dados acima no checkout
  - Ou registre-se diretamente no site
  - Sistema permite pedidos como convidado
  - **Nota:** Sistema não requer login de cliente para fazer pedidos

---

## 🌐 URLs PRINCIPAIS

### 📱 Mini-Sites dos Restaurantes (White Label)
- **Pizzaria do José:** http://localhost:8000/pizzaria-do-jose/
  - Tema: Vermelho (#e74c3c)
  - 7 produtos em 3 categorias
  - Taxa entrega: R$ 5,00
  - Tempo: 30 min

- **Burger House:** http://localhost:8000/burger-house/
  - Tema: Laranja (#f39c12)
  - 2 produtos em 2 categorias
  - Taxa entrega: R$ 4,00
  - Tempo: 25 min

### 🏠 Páginas da Plataforma
- **Home:** http://localhost:8000/
- **Lista de Restaurantes:** http://localhost:8000/restaurantes/
- **Painel do Lojista:** http://localhost:8000/lojista/
- **Super Admin:** http://localhost:8000/superadmin/
- **Django Admin:** http://localhost:8000/admin/

---

## 🛒 COMO TESTAR O SISTEMA

### 1. Como Cliente (Fazer Pedidos)
1. Acesse um restaurante: http://localhost:8000/pizzaria-do-jose/
2. Navegue pelas categorias no menu
3. Adicione produtos ao carrinho
4. Clique no ícone do carrinho (canto superior direito)
5. Finalize o pedido no checkout

### 2. Como Lojista (Gerenciar Restaurante)
1. Faça login: http://localhost:8000/lojista/
2. Use: `lojista_teste` / `lojista123`
3. Acesse o dashboard para ver pedidos
4. Gerencie produtos e categorias
5. Configure o restaurante

### 3. Como Administrador (Gerenciar Plataforma)
1. Django Admin: http://localhost:8000/admin/
2. Super Admin: http://localhost:8000/superadmin/
3. Use: `admin` / `admin123`
4. Visualize estatísticas e gerencie usuários

---

## 📊 DADOS PRÉ-POPULADOS

### 🍕 Pizzaria do José
**Categorias:**
- Pizzas Tradicionais (3 produtos)
- Pizzas Especiais (2 produtos)
- Bebidas (2 produtos)

**Produtos em destaque:**
- Pizza Margherita - R$ 32,90
- Pizza do Chef - R$ 45,90

### 🍔 Burger House
**Categorias:**
- Hambúrgueres (1 produto)
- Acompanhamentos (1 produto)

**Produtos:**
- X-Bacon Artesanal - R$ 24,90
- Batata Frita Grande - R$ 12,90

---

## ⚙️ RECURSOS IMPLEMENTADOS

### ✅ Sistema White Label
- URL única por restaurante
- Cores e temas personalizados
- Middleware de detecção automática
- Isolamento completo entre restaurantes

### ✅ Carrinho de Compras
- Persistência via LocalStorage
- Interface lateral deslizante
- Cálculo automático de totais
- Contadores dinâmicos

### ✅ Painel Administrativo
- Dashboard com estatísticas
- Gestão de produtos e categorias
- Controle de pedidos
- Configurações do restaurante

### ✅ Sistema de Pedidos
- API para finalização
- Estados de pedido
- Integração com ViaCEP
- Checkout simplificado

---

## 🔧 TECNOLOGIAS UTILIZADAS

- **Backend:** Django 5.2+
- **Frontend:** Bootstrap 5, JavaScript ES6
- **Banco:** SQLite (desenvolvimento)
- **Python:** 3.13.3
- **Dependências:** django-crispy-forms, crispy-bootstrap5, Pillow, requests

---

## 📞 SUPORTE

Se encontrar algum problema:
1. Verifique se o servidor está rodando
2. Confirme que está usando as credenciais corretas
3. Teste primeiro com as URLs dos mini-sites
4. Use o Django Admin para verificar dados

---

## 🎯 PRÓXIMAS IMPLEMENTAÇÕES (Fase 2)

- [ ] Sistema de notificações em tempo real
- [ ] Relatórios avançados para lojistas
- [ ] Sistema de avaliações
- [ ] Integração com pagamentos
- [ ] App mobile
- [ ] Sistema de cupons e promoções

---

**Sistema desenvolvido com ❤️ usando Django + Bootstrap**
