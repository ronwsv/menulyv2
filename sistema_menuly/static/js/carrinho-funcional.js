// 🍕 Sistema de Carrinho Funcional para Pizzaria do José
console.log('🍕 Carregando sistema de carrinho...');

// Estado global do carrinho
let carrinho = [];
let restauranteId = null;

// Inicializar sistema quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    console.log('📄 DOM carregado, inicializando sistema de carrinho...');
    
    // Extrair ID do restaurante
    const metaRestaurante = document.querySelector('meta[name="restaurante-id"]');
    if (metaRestaurante) {
        restauranteId = metaRestaurante.content;
    } else {
        restauranteId = window.restauranteIdGlobal || '1';
    }
    
    console.log('🏪 Restaurante ID:', restauranteId);
    
    // Carregar carrinho existente
    carregarCarrinho();
    
    // Aguardar um pouco para garantir que todos os elementos foram renderizados
    setTimeout(() => {
        configurarEventos();
        atualizarInterface();
        console.log('✅ Sistema de carrinho totalmente configurado!');
    }, 500);
    
    // Adicionar event listener para responsividade
    window.addEventListener('resize', ajustarResponsividade);
});

// Carregar carrinho do localStorage
function carregarCarrinho() {
    try {
        const carrinhoSalvo = localStorage.getItem(`carrinho_${restauranteId}`);
        if (carrinhoSalvo) {
            carrinho = JSON.parse(carrinhoSalvo);
            console.log('📦 Carrinho carregado do localStorage:', carrinho.length, 'itens');
        } else {
            console.log('📦 Carrinho vazio inicializado');
            carrinho = [];
        }
    } catch (error) {
        console.error('❌ Erro ao carregar carrinho:', error);
        carrinho = [];
    }
}

// Salvar carrinho no localStorage
function salvarCarrinho() {
    try {
        localStorage.setItem(`carrinho_${restauranteId}`, JSON.stringify(carrinho));
        console.log('💾 Carrinho salvo no localStorage');
    } catch (error) {
        console.error('❌ Erro ao salvar carrinho:', error);
    }
}

// Configurar eventos da página
function configurarEventos() {
    console.log('⚙️ Configurando eventos dos produtos...');
    
    // Encontrar todos os elementos que podem ser produtos
    const possiveisProdutos = [
        ...document.querySelectorAll('.card'),
        ...document.querySelectorAll('.produto-card'),
        ...document.querySelectorAll('[class*="produto"]'),
        ...document.querySelectorAll('[class*="card"]')
    ];
    
    // Remover duplicatas
    const produtoCards = Array.from(new Set(possiveisProdutos));
    
    console.log(`🍽️ Analisando ${produtoCards.length} elementos como possíveis produtos...`);
    
    let produtosConfigurados = 0;
    
    produtoCards.forEach((card, index) => {
        // Verificar se parece um produto (tem título e preço)
        const titulo = card.querySelector('.card-title, h3, h4, h5, h6, .nome-produto, .produto-nome');
        const preco = card.querySelector('.preco, .price, .text-success, [class*="preco"]');
        
        if (!titulo && !preco) {
            return; // Não é um produto
        }
        
        const nome = titulo ? titulo.textContent.trim() : `Produto ${index + 1}`;
        const precoTexto = preco ? preco.textContent : 'R$ 15,00';
        const precoNumerico = extrairPreco(precoTexto);
        const produtoId = index + 1;
        
        // IMPORTANTE: Não criar novos botões, apenas configurar os existentes
        let botaoAdicionar = card.querySelector('button:not(.btn-close)');
        
        if (botaoAdicionar) {
            // Configurar botão existente
            console.log(`🔘 Configurando botão existente para: ${nome}`);
            
            // Remover eventos anteriores
            botaoAdicionar.onclick = null;
            botaoAdicionar.removeAttribute('onclick');
            
            // Adicionar novo evento
            botaoAdicionar.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                console.log(`�️ Clique detectado em: ${nome}`);
                adicionarProduto(produtoId, nome, precoNumerico);
            });
            
            // Melhorar visual do botão
            if (!botaoAdicionar.innerHTML.includes('Adicionar')) {
                botaoAdicionar.innerHTML = '<i class="fas fa-plus me-1"></i>Adicionar';
            }
            
            produtosConfigurados++;
        } else {
            // Se não há botão, adicionar evento ao card inteiro
            console.log(`🖱️ Configurando card clicável para: ${nome}`);
            
            card.style.cursor = 'pointer';
            card.addEventListener('click', function(e) {
                e.preventDefault();
                console.log(`🖱️ Clique no card: ${nome}`);
                adicionarProduto(produtoId, nome, precoNumerico);
            });
            
            produtosConfigurados++;
        }
        
        console.log(`✅ Produto configurado: "${nome}" - R$ ${precoNumerico.toFixed(2)}`);
    });
    
    console.log(`🎯 Total configurado: ${produtosConfigurados} produtos`);
    
    // Configurar carrinho flutuante
    configurarCarrinhoFlutuante();
    
    // Configurar botão flutuante de checkout
    configurarBotaoCheckout();
}

// Extrair preço do texto
function extrairPreco(texto) {
    // Remover símbolos e extrair números
    const numeroTexto = texto.replace(/[^\d,\.]/g, '').replace(',', '.');
    const numero = parseFloat(numeroTexto);
    return isNaN(numero) ? 15.00 : numero; // Preço padrão se não conseguir extrair
}

// Adicionar produto ao carrinho
function adicionarProduto(id, nome, preco) {
    console.log('➕ Adicionando produto ao carrinho:', { id, nome, preco });
    
    // Verificar se já existe no carrinho
    const itemExistente = carrinho.find(item => item.id === id);
    
    if (itemExistente) {
        itemExistente.quantidade += 1;
        itemExistente.subtotal = itemExistente.preco * itemExistente.quantidade;
        console.log('📈 Quantidade aumentada:', itemExistente);
    } else {
        const novoItem = {
            id: id,
            nome: nome,
            preco: preco,
            quantidade: 1,
            subtotal: preco
        };
        carrinho.push(novoItem);
        console.log('🆕 Novo item adicionado:', novoItem);
    }
    
    // Salvar e atualizar
    salvarCarrinho();
    atualizarInterface();
    
    // Feedback visual mais elaborado
    mostrarFeedbackAvancado(nome, preco);
    
    // Animação no botão
    const botoes = document.querySelectorAll('button');
    botoes.forEach(btn => {
        if (btn.textContent.includes('Adicionar')) {
            btn.style.backgroundColor = '#28a745';
            btn.textContent = '✅ Adicionado!';
            setTimeout(() => {
                btn.style.backgroundColor = '';
                btn.innerHTML = '<i class="fas fa-plus me-1"></i>Adicionar';
            }, 1000);
        }
    });
}

// Atualizar interface do carrinho
function atualizarInterface() {
    atualizarCarrinhoFlutuante();
    
    // Atualizar carrinho lateral se a função existir
    if (typeof atualizarCarrinhoLateral === 'function') {
        atualizarCarrinhoLateral();
    }
    
    // Garantir que o botão de checkout existe
    if (!document.getElementById('checkout-flutuante')) {
        configurarBotaoCheckout();
    }
}

// Configurar carrinho flutuante (REMOVIDO - agora usa carrinho lateral)
function configurarCarrinhoFlutuante() {
    // Não criar mais o carrinho flutuante azul
    console.log('🛒 Carrinho flutuante removido - usando carrinho lateral no header');
}

// Configurar botão flutuante de checkout
function configurarBotaoCheckout() {
    let botaoCheckout = document.getElementById('checkout-flutuante');
    
    if (!botaoCheckout) {
        console.log('💳 Criando botão de checkout flutuante...');
        
        botaoCheckout = document.createElement('div');
        botaoCheckout.id = 'checkout-flutuante';
        botaoCheckout.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: linear-gradient(135deg, #28a745, #20c997);
            color: white;
            padding: 15px 25px;
            border-radius: 50px;
            box-shadow: 0 4px 20px rgba(40,167,69,0.3);
            cursor: pointer;
            z-index: 1040;
            display: none;
            font-weight: 600;
            transition: all 0.3s ease;
            font-size: 16px;
            min-width: 250px;
            text-align: center;
        `;
        
        // Responsividade mobile
        if (window.innerWidth <= 768) {
            botaoCheckout.style.cssText += `
                font-size: 14px;
                padding: 12px 20px;
                min-width: 200px;
                bottom: 10px;
                right: 10px;
            `;
        }
        
        botaoCheckout.innerHTML = `
            <i class="fas fa-credit-card me-2"></i>
            Finalizar Pedido
            <small class="d-block" style="font-size: 12px; opacity: 0.9;">
                R$ <span id="checkout-total">0,00</span> • <span id="checkout-itens">0</span> itens
            </small>
        `;
        
        // Efeitos de hover
        botaoCheckout.onmouseenter = function() {
            this.style.transform = 'scale(1.05)';
            this.style.boxShadow = '0 6px 25px rgba(40,167,69,0.5)';
        };
        
        botaoCheckout.onmouseleave = function() {
            this.style.transform = 'scale(1)';
            this.style.boxShadow = '0 4px 20px rgba(40,167,69,0.3)';
        };
        
        // Evento para ir ao checkout
        botaoCheckout.onclick = finalizarPedidoCarrinho;
        
        document.body.appendChild(botaoCheckout);
        console.log('✅ Botão de checkout flutuante criado');
    }
    
    // Ajustar responsividade
    ajustarResponsividade();
}

// Ajustar responsividade do botão
function ajustarResponsividade() {
    const botaoCheckout = document.getElementById('checkout-flutuante');
    if (!botaoCheckout) return;
    
    if (window.innerWidth <= 768) {
        botaoCheckout.style.fontSize = '14px';
        botaoCheckout.style.padding = '12px 20px';
        botaoCheckout.style.minWidth = '200px';
        botaoCheckout.style.bottom = '10px';
        botaoCheckout.style.right = '10px';
    } else {
        botaoCheckout.style.fontSize = '16px';
        botaoCheckout.style.padding = '15px 25px';
        botaoCheckout.style.minWidth = '250px';
        botaoCheckout.style.bottom = '20px';
        botaoCheckout.style.right = '20px';
    }
}

// Atualizar carrinho flutuante (REMOVIDO - agora usa carrinho lateral)
function atualizarCarrinhoFlutuante() {
    // Atualizar apenas o botão de checkout
    const checkoutEl = document.getElementById('checkout-flutuante');
    const checkoutTotalEl = document.getElementById('checkout-total');
    const checkoutItensEl = document.getElementById('checkout-itens');
    
    if (carrinho.length === 0) {
        if (checkoutEl) checkoutEl.style.display = 'none';
        return;
    }
    
    const totalItens = carrinho.reduce((sum, item) => sum + item.quantidade, 0);
    const totalPreco = carrinho.reduce((sum, item) => sum + item.subtotal, 0);
    
    // Atualizar botão de checkout
    if (checkoutEl && checkoutTotalEl && checkoutItensEl) {
        checkoutTotalEl.textContent = totalPreco.toFixed(2).replace('.', ',');
        checkoutItensEl.textContent = totalItens;
        checkoutEl.style.display = 'block';
    }
    
    console.log('🛒 Interface atualizada:', { itens: totalItens, total: totalPreco });
}

// Atualizar carrinho no header
function atualizarCarrinhoHeader(totalItens, totalPreco) {
    // Procurar por elemento de carrinho no header
    const headerCarrinho = document.querySelector('#header-carrinho, .header-carrinho, [data-carrinho="header"]');
    
    if (headerCarrinho) {
        // Se existe elemento específico, atualizar
        const quantidadeHeader = headerCarrinho.querySelector('.quantidade, .badge');
        if (quantidadeHeader) {
            quantidadeHeader.textContent = totalItens;
            quantidadeHeader.style.display = totalItens > 0 ? 'inline' : 'none';
        }
    } else {
        // Criar ou atualizar badge no navbar
        criarCarrinhoHeader(totalItens, totalPreco);
    }
}

// Criar carrinho no header
function criarCarrinhoHeader(totalItens, totalPreco) {
    const navbar = document.querySelector('.navbar-nav');
    if (!navbar) return;
    
    // Verificar se já existe
    let carrinhoHeaderItem = document.getElementById('header-carrinho-item');
    
    if (!carrinhoHeaderItem) {
        // Criar item do menu
        carrinhoHeaderItem = document.createElement('li');
        carrinhoHeaderItem.className = 'nav-item';
        carrinhoHeaderItem.id = 'header-carrinho-item';
        
        const carrinhoLink = document.createElement('a');
        carrinhoLink.className = 'nav-link position-relative';
        carrinhoLink.href = '#';
        carrinhoLink.style.cursor = 'pointer';
        carrinhoLink.onclick = function(e) {
            e.preventDefault();
            if (carrinho.length > 0) {
                abrirCarrinho();
            } else {
                mostrarFeedbackAvancado('Carrinho vazio', 0);
            }
        };
        
        carrinhoLink.innerHTML = `
            <i class="fas fa-shopping-cart me-1"></i>Carrinho
            <span id="header-carrinho-badge" class="badge bg-danger ms-1" style="display: none;">0</span>
        `;
        
        carrinhoHeaderItem.appendChild(carrinhoLink);
        navbar.appendChild(carrinhoHeaderItem);
        
        console.log('🛒 Carrinho adicionado ao header');
    }
    
    // Atualizar badge
    const badge = document.getElementById('header-carrinho-badge');
    if (badge) {
        badge.textContent = totalItens;
        badge.style.display = totalItens > 0 ? 'inline' : 'none';
    }
}

// Mostrar feedback avançado
function mostrarFeedbackAvancado(nome, preco) {
    console.log('💬 Mostrando feedback para:', nome);
    
    // Criar elemento de feedback
    const feedback = document.createElement('div');
    feedback.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(40,167,69,0.3);
        z-index: 9999;
        font-weight: 600;
        animation: slideIn 0.3s ease;
        max-width: 300px;
    `;
    
    feedback.innerHTML = `
        <div style="display: flex; align-items: center;">
            <i class="fas fa-check-circle me-2" style="font-size: 1.2em;"></i>
            <div>
                <div style="font-size: 0.9em;">${nome}</div>
                <div style="font-size: 0.8em; opacity: 0.9;">R$ ${preco.toFixed(2)} adicionado ao carrinho</div>
            </div>
        </div>
    `;
    
    // Adicionar animação CSS
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from { transform: translateX(100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
    `;
    document.head.appendChild(style);
    
    document.body.appendChild(feedback);
    
    // Remover após 3 segundos
    setTimeout(() => {
        feedback.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => feedback.remove(), 300);
    }, 3000);
}

// Abrir carrinho
function abrirCarrinho() {
    console.log('🛒 Abrindo carrinho...', carrinho.length, 'itens');
    
    if (carrinho.length === 0) {
        mostrarFeedbackAvancado('Carrinho vazio', 0);
        return;
    }
    
    // Criar modal do carrinho
    const modal = document.createElement('div');
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0,0,0,0.7);
        z-index: 10000;
        display: flex;
        align-items: center;
        justify-content: center;
    `;
    
    const totalItens = carrinho.reduce((sum, item) => sum + item.quantidade, 0);
    const totalPreco = carrinho.reduce((sum, item) => sum + item.subtotal, 0);
    
    const conteudo = `
        <div style="
            background: white;
            border-radius: 15px;
            padding: 30px;
            max-width: 500px;
            width: 90%;
            max-height: 80vh;
            overflow-y: auto;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <h3 style="margin: 0; color: #333;">🛒 Seu Carrinho</h3>
                <button onclick="this.closest('.modal-carrinho').remove()" style="
                    border: none;
                    background: none;
                    font-size: 1.5em;
                    cursor: pointer;
                    color: #999;
                ">×</button>
            </div>
            
            <div style="margin-bottom: 20px;">
                ${carrinho.map((item, index) => `
                    <div style="
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        padding: 15px;
                        border: 1px solid #eee;
                        border-radius: 10px;
                        margin-bottom: 10px;
                        background: #f8f9fa;
                    ">
                        <div>
                            <div style="font-weight: 600; color: #333;">${item.nome}</div>
                            <div style="color: #666; font-size: 0.9em;">${item.quantidade}x R$ ${item.preco.toFixed(2)}</div>
                        </div>
                        <div style="text-align: right;">
                            <div style="font-weight: 600; color: #007bff;">R$ ${item.subtotal.toFixed(2)}</div>
                            <button onclick="window.removerItemCarrinho(${index})" style="
                                border: none;
                                background: #dc3545;
                                color: white;
                                padding: 5px 10px;
                                border-radius: 5px;
                                font-size: 0.8em;
                                cursor: pointer;
                                margin-top: 5px;
                            ">
                                <i class="fas fa-trash"></i> Remover
                            </button>
                        </div>
                    </div>
                `).join('')}
            </div>
            
            <div style="
                border-top: 2px solid #007bff;
                padding-top: 15px;
                margin-top: 20px;
            ">
                <div style="display: flex; justify-content: space-between; font-size: 1.1em; font-weight: 600; margin-bottom: 15px;">
                    <span>Total: ${totalItens} itens</span>
                    <span style="color: #007bff;">R$ ${totalPreco.toFixed(2)}</span>
                </div>
                
                <button onclick="window.finalizarPedidoCarrinho()" style="
                    width: 100%;
                    background: linear-gradient(135deg, #28a745, #20c997);
                    color: white;
                    border: none;
                    padding: 15px;
                    border-radius: 10px;
                    font-size: 1.1em;
                    font-weight: 600;
                    cursor: pointer;
                    transition: all 0.3s ease;
                ">
                    <i class="fas fa-credit-card me-2"></i>Finalizar Pedido
                </button>
            </div>
        </div>
    `;
    
    modal.className = 'modal-carrinho';
    modal.innerHTML = conteudo;
    
    // Fechar ao clicar fora
    modal.onclick = function(e) {
        if (e.target === modal) {
            modal.remove();
        }
    };
    
    document.body.appendChild(modal);
}

// Remover item do carrinho
function removerItemCarrinho(index) {
    console.log('�️ Removendo item do carrinho:', index);
    carrinho.splice(index, 1);
    salvarCarrinho();
    atualizarInterface();
    
    // Fechar modal atual e reabrir se ainda houver itens
    document.querySelector('.modal-carrinho')?.remove();
    if (carrinho.length > 0) {
        setTimeout(abrirCarrinho, 100);
    }
}

// Finalizar pedido
function finalizarPedidoCarrinho() {
    console.log('✅ Finalizando pedido...', carrinho.length, 'itens');
    
    // Fechar modal
    document.querySelector('.modal-carrinho')?.remove();
    
    // Redirecionar para checkout
    try {
        const slug = window.location.pathname.split('/')[1] || 'pizzaria-do-jose';
        const checkoutUrl = `/${slug}/checkout/`;
        
        console.log('🔄 Redirecionando para:', checkoutUrl);
        window.location.href = checkoutUrl;
    } catch (error) {
        console.error('❌ Erro ao redirecionar:', error);
        mostrarFeedbackAvancado('Erro ao abrir checkout', 0);
    }
}

// Expor funções globalmente para compatibilidade
window.abrirModalProduto = function(id) {
    console.log('🔄 Chamada legacy abrirModalProduto:', id);
    const botoes = Array.from(document.querySelectorAll('button'));
    const botao = botoes[id - 1] || botoes[0];
    if (botao) botao.click();
};

window.removerItemCarrinho = removerItemCarrinho;
window.finalizarPedidoCarrinho = finalizarPedidoCarrinho;

// Debug interface
window.carrinhoDebug = {
    carrinho: () => carrinho,
    adicionar: adicionarProduto,
    limpar: () => {
        carrinho = [];
        salvarCarrinho();
        atualizarInterface();
        console.log('🗑️ Carrinho limpo');
    },
    status: () => {
        console.log('📊 Status do carrinho:', {
            itens: carrinho.length,
            total: carrinho.reduce((sum, item) => sum + item.subtotal, 0),
            produtos: carrinho
        });
        return carrinho;
    },
    abrir: abrirCarrinho
};

// Funções para controlar o carrinho lateral
function abrirCarrinhoLateral() {
    console.log('🛒 Abrindo carrinho lateral...');
    const overlay = document.getElementById('carrinho-overlay');
    const lateral = document.getElementById('carrinho-lateral');
    
    if (overlay && lateral) {
        overlay.style.display = 'block';
        lateral.classList.add('active');
        document.body.style.overflow = 'hidden'; // Prevenir scroll
        atualizarCarrinhoLateral();
    } else {
        console.error('❌ Elementos do carrinho lateral não encontrados');
    }
}

function fecharCarrinhoLateral() {
    console.log('🛒 Fechando carrinho lateral...');
    const overlay = document.getElementById('carrinho-overlay');
    const lateral = document.getElementById('carrinho-lateral');
    
    if (overlay && lateral) {
        overlay.style.display = 'none';
        lateral.classList.remove('active');
        document.body.style.overflow = 'auto'; // Restaurar scroll
    }
}

function atualizarCarrinhoLateral() {
    const itensEl = document.getElementById('carrinho-lateral-itens');
    const footerEl = document.getElementById('carrinho-lateral-footer');
    const subtotalEl = document.getElementById('carrinho-lateral-subtotal');
    const totalEl = document.getElementById('carrinho-lateral-total');
    
    if (!itensEl) return;
    
    if (carrinho.length === 0) {
        itensEl.innerHTML = `
            <div class="text-center text-muted py-5">
                <i class="fas fa-shopping-cart fa-3x mb-3"></i>
                <p>Seu carrinho está vazio</p>
            </div>
        `;
        if (footerEl) footerEl.style.display = 'none';
        return;
    }
    
    let html = '';
    let subtotal = 0;
    
    carrinho.forEach(item => {
        subtotal += item.subtotal;
        html += `
            <div class="item-carrinho">
                <div class="item-quantity me-3">${item.quantidade}</div>
                <div class="flex-grow-1">
                    <h6 class="mb-1">${item.nome}</h6>
                    <small class="text-muted">R$ ${item.preco.toFixed(2)} cada</small>
                </div>
                <div class="text-end">
                    <strong>R$ ${item.subtotal.toFixed(2)}</strong>
                </div>
            </div>
        `;
    });
    
    itensEl.innerHTML = html;
    
    if (subtotalEl) subtotalEl.textContent = subtotal.toFixed(2);
    
    // Calcular total com taxa de entrega
    const taxaEntrega = window.MENULY?.taxaEntrega || 0;
    const total = subtotal + taxaEntrega;
    if (totalEl) totalEl.textContent = total.toFixed(2);
    
    if (footerEl) footerEl.style.display = 'block';
}

// Disponibilizar as funções globalmente
window.abrirCarrinhoLateral = abrirCarrinhoLateral;
window.fecharCarrinhoLateral = fecharCarrinhoLateral;

console.log('🎉 Sistema de carrinho carregado com sucesso!');
console.log('🔧 Debug disponível em: window.carrinhoDebug');
