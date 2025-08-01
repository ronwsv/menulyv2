# 🍕 Menuly v2 - Sistema White Label de Delivery

[![Django](https://img.shields.io/badge/Django-5.2.4-green.svg)](https://djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-purple.svg)](https://getbootstrap.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow.svg)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Sistema completo de delivery multi-restaurante com mini-sites personalizados e carrinho funcional avançado.

## 🚀 Características Principais

### 🏪 Sistema Multi-Restaurante
- **Mini-sites independentes** para cada restaurante
- **URLs personalizadas** (`/pizzaria-do-jose/`, `/sushi-zen/`)
- **Customização visual completa** (cores, logos, banners)
- **Sistema de administração** para lojistas

### 🛒 Carrinho Avançado
- **Carrinho lateral responsivo** com animações
- **Persistência no localStorage** por restaurante
- **Interface mobile otimizada** (90vw em dispositivos móveis)
- **Feedback visual elaborado** para ações do usuário
- **Integração completa** com sistema de checkout

### 💳 Checkout Completo
- **4 etapas bem definidas**: Dados → Endereço → Pagamento → Confirmação
- **Integração com ViaCEP** para busca automática de endereços
- **Múltiplas formas de pagamento** (PIX, Cartão, Dinheiro)
- **Interface moderna** com cards e indicadores de progresso

### 🎨 White Label
- **Cores personalizáveis** por restaurante
- **Upload de logos e banners**
- **Templates customizados**
- **Gradientes dinâmicos** baseados nas cores do restaurante

## 📱 Interface Responsiva

### Desktop
- Carrinho lateral elegante
- Layout em grid otimizado
- Animações suaves

### Mobile
- Carrinho lateral em 90% da largura
- Botões otimizados para toque
- Interface adaptativa

## 🛠️ Tecnologias

- **Backend**: Django 5.2.4
- **Frontend**: Bootstrap 5.3.0, JavaScript ES6+
- **Banco**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **Estilos**: CSS3 com variáveis customizadas
- **Icons**: Font Awesome 6.4.0

## 📦 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/ronwsv/menulyv2.git
cd menulyv2
```

### 2. Criar ambiente virtual
```bash
cd sistema_menuly
python -m venv .venv
```

### 3. Ativar ambiente virtual
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 4. Instalar dependências
```bash
pip install -r requirements.txt
```

### 5. Configurar banco de dados
```bash
python manage.py migrate
```

### 6. Criar superusuário
```bash
python manage.py createsuperuser
```

### 7. Executar servidor
```bash
python manage.py runserver
```

Acesse: `http://localhost:8000`

## 🏗️ Estrutura do Projeto

```
sistema_menuly/
├── apps/
│   ├── accounts/          # Sistema de usuários customizado
│   ├── core/              # Funcionalidades centrais
│   ├── lojistas/          # Painel do lojista
│   ├── pedidos/           # Sistema de pedidos
│   ├── restaurantes/      # Gestão de restaurantes
│   └── superadmin/        # Administração geral
├── backend/               # Configurações Django
├── static/
│   └── js/
│       └── carrinho-funcional.js  # Sistema de carrinho
├── templates/
│   ├── base.html          # Template base com carrinho lateral
│   ├── restaurante/       # Templates dos mini-sites
│   └── lojista/           # Templates do painel lojista
└── manage.py
```

## 🎯 Funcionalidades por Módulo

### 🍽️ Restaurantes
- Gestão completa de produtos e categorias
- Sistema de horários de funcionamento
- Configuração de taxa de entrega
- Upload de imagens (logo, banner, favicon)

### 🛒 Sistema de Carrinho
- Detecção automática de produtos na página
- Configuração dinâmica de eventos de clique
- Animações e feedback visual
- Integração com checkout

### 👥 Usuários e Permissões
- Sistema de usuários customizado
- Perfis diferenciados (Lojista, Administrador)
- Permissões granulares por restaurante

### 📊 Dashboard Lojista
- Métricas de vendas em tempo real
- Gestão de pedidos
- Configuração de impressoras
- Relatórios detalhados

## 🔧 Configuração Avançada

### Cores Personalizadas
```css
:root {
    --cor-principal: {{ restaurante.cor_primaria }};
    --cor-secundaria: {{ restaurante.cor_secundaria }};
    --cor-botoes: {{ restaurante.cor_botoes }};
    --gradiente-principal: linear-gradient(135deg, var(--cor-principal), var(--cor-secundaria));
}
```

### JavaScript do Carrinho
```javascript
// Debug do carrinho disponível globalmente
window.carrinhoDebug.status();  // Ver status atual
window.carrinhoDebug.limpar();  // Limpar carrinho
window.carrinhoDebug.adicionar(1, 'Produto', 15.90);  // Adicionar item
```

## 🚀 Deploy

### Variáveis de Ambiente
```env
DEBUG=False
SECRET_KEY=sua_chave_secreta_aqui
DATABASE_URL=postgresql://user:pass@host:port/dbname
ALLOWED_HOSTS=seu-dominio.com
```

### Configuração para Produção
1. Configure `DEBUG = False`
2. Defina `ALLOWED_HOSTS`
3. Configure banco PostgreSQL
4. Execute `python manage.py collectstatic`
5. Configure servidor web (nginx/apache)

## 📝 Uso

### Criar Restaurante
1. Acesse `/admin/`
2. Crie um Lojista
3. Adicione um Restaurante
4. Configure cores e imagens
5. Adicione produtos e categorias

### Testar Carrinho
1. Acesse `/nome-do-restaurante/`
2. Clique em produtos para adicionar
3. Use `Ctrl+Shift+I` → Console
4. Digite `window.carrinhoDebug.status()`

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🎉 Recursos Implementados

- ✅ Sistema multi-restaurante completo
- ✅ Carrinho funcional com localStorage
- ✅ Checkout em 4 etapas
- ✅ Interface responsiva mobile/desktop
- ✅ Customização visual (White Label)
- ✅ Sistema de usuários e permissões
- ✅ Dashboard para lojistas
- ✅ Integração com ViaCEP
- ✅ Sistema de pedidos completo
- ✅ Configuração de impressoras

## 📞 Suporte

Para dúvidas ou suporte, abra uma [issue](https://github.com/ronwsv/menulyv2/issues) no GitHub.

---

**Desenvolvido com ❤️ para revolucionar o delivery brasileiro!**
