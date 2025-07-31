/**
 * Sistema de Checkout Inteligente - Estrutura Otimizada
 * 
 * Implementa busca automática por celular, preenchimento inteligente
 * de endereços e histórico de pedidos para melhorar a experiência do cliente.
 */

class CheckoutInteligente {
    constructor() {
        this.celularInput = document.getElementById('id_celular');
        this.nomeInput = document.getElementById('id_nome');
        this.emailInput = document.getElementById('id_email');
        this.enderecoSection = document.getElementById('endereco-section');
        this.clienteAtual = null;
        this.enderecosSalvos = [];
        
        this.initEventListeners();
        this.initValidadores();
    }
    
    initEventListeners() {
        if (!this.celularInput) return;
        
        // Buscar cliente quando celular for preenchido
        this.celularInput.addEventListener('blur', () => {
            this.buscarCliente();
        });
        
        // Formatar celular automaticamente
        this.celularInput.addEventListener('input', (e) => {
            e.target.value = this.formatarCelular(e.target.value);
        });
        
        // Validar formulário antes do envio
        const form = this.celularInput.closest('form');
        if (form) {
            form.addEventListener('submit', (e) => {
                if (!this.validarFormulario()) {
                    e.preventDefault();
                }
            });
        }
    }
    
    initValidadores() {
        // Validador de CEP
        const cepInput = document.getElementById('id_cep');
        if (cepInput) {
            cepInput.addEventListener('input', (e) => {
                e.target.value = this.formatarCep(e.target.value);
            });
            
            cepInput.addEventListener('blur', () => {
                this.validarCep();
            });
        }
        
        // Validador de email
        const emailInput = document.getElementById('id_email');
        if (emailInput) {
            emailInput.addEventListener('blur', () => {
                this.validarEmail();
            });
        }
    }
    
    async buscarCliente() {
        const celular = this.celularInput.value.replace(/\D/g, '');
        
        if (celular.length < 10) {
            this.limparFormulario();
            return;
        }
        
        this.mostrarCarregando(true);
        
        try {
            const response = await fetch('/ajax/buscar-cliente/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: `celular=${celular}`
            });
            
            const data = await response.json();
            
            if (data.found) {
                this.clienteAtual = data.cliente;
                this.enderecosSalvos = data.enderecos;
                this.preencherDadosCliente(data);
                this.mostrarHistorico(data.ultimos_pedidos);
                this.criarSeletorEnderecos(data.enderecos, data.endereco_principal_id);
            } else {
                this.limparFormulario();
                if (data.message) {
                    this.mostrarMensagem(data.message, 'info');
                }
            }
            
        } catch (error) {
            console.error('Erro ao buscar cliente:', error);
            this.mostrarMensagem('Erro ao buscar dados do cliente', 'error');
        } finally {
            this.mostrarCarregando(false);
        }
    }
    
    preencherDadosCliente(data) {
        // Preencher dados básicos
        if (this.nomeInput && !this.nomeInput.value) {
            this.nomeInput.value = data.cliente.nome;
        }
        
        if (this.emailInput && !this.emailInput.value) {
            this.emailInput.value = data.cliente.email;
        }
        
        // Mostrar mensagem de cliente encontrado
        this.mostrarMensagemClienteEncontrado(data.cliente);
    }
    
    mostrarMensagemClienteEncontrado(cliente) {
        this.removerMensagensAnteriores();
        
        const mensagem = document.createElement('div');
        mensagem.className = 'alert alert-success mt-2 cliente-encontrado';
        mensagem.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="fas fa-user-check me-3"></i>
                <div class="flex-grow-1">
                    <strong>Cliente encontrado!</strong><br>
                    <small class="text-muted">
                        ${cliente.nome} • ${cliente.total_pedidos} pedidos • 
                        Total gasto: R$ ${cliente.valor_total_gasto}
                    </small>
                </div>
                <button type="button" class="btn btn-sm btn-outline-primary" onclick="checkout.mostrarHistoricoCompleto()">
                    <i class="fas fa-history"></i> Ver histórico
                </button>
            </div>
        `;
        
        this.celularInput.parentNode.appendChild(mensagem);
    }
    
    criarSeletorEnderecos(enderecos, enderecoPrincipalId) {
        if (enderecos.length === 0) return;
        
        this.removerSeletorEnderecos();
        
        const selectorHTML = `
            <div class="card mt-3" id="enderecos-salvos">
                <div class="card-header">
                    <h6 class="mb-0">
                        <i class="fas fa-map-marked-alt me-2"></i>
                        Endereços Salvos
                    </h6>
                </div>
                <div class="card-body">
                    <select class="form-select mb-3" id="endereco-salvo-select">
                        <option value="">Selecione um endereço salvo ou cadastre um novo</option>
                        ${enderecos.map(endereco => 
                            `<option value="${endereco.id}" 
                                     data-endereco='${JSON.stringify(endereco)}'
                                     ${endereco.id == enderecoPrincipalId ? 'selected' : ''}>
                                ${endereco.apelido} - ${endereco.endereco}, ${endereco.numero}, ${endereco.bairro}
                                ${endereco.vezes_utilizado > 0 ? ` (usado ${endereco.vezes_utilizado}x)` : ''}
                            </option>`
                        ).join('')}
                    </select>
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted">
                            <i class="fas fa-info-circle me-1"></i>
                            Seus endereços ficam salvos para facilitar próximos pedidos
                        </small>
                        <button type="button" class="btn btn-sm btn-outline-success" onclick="checkout.mostrarFormularioSalvarEndereco()">
                            <i class="fas fa-plus"></i> Salvar endereço atual
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        this.enderecoSection.insertAdjacentHTML('afterbegin', selectorHTML);
        
        // Event listener para seleção de endereço
        document.getElementById('endereco-salvo-select').addEventListener('change', (e) => {
            if (e.target.value) {
                const enderecoData = JSON.parse(e.target.selectedOptions[0].dataset.endereco);
                this.preencherCamposEndereco(enderecoData);
                this.marcarEnderecoUtilizado(e.target.value);
            }
        });
        
        // Se tem endereço principal, preencher automaticamente
        if (enderecoPrincipalId) {
            const enderecoPrincipal = enderecos.find(e => e.id == enderecoPrincipalId);
            if (enderecoPrincipal) {
                this.preencherCamposEndereco(enderecoPrincipal);
            }
        }
    }
    
    preencherCamposEndereco(endereco) {
        const campos = {
            'id_endereco': endereco.endereco,
            'id_numero': endereco.numero,
            'id_complemento': endereco.complemento,
            'id_bairro': endereco.bairro,
            'id_cidade': endereco.cidade,
            'id_estado': endereco.estado,
            'id_cep': endereco.cep,
            'id_referencia': endereco.referencia
        };
        
        Object.entries(campos).forEach(([id, valor]) => {
            const campo = document.getElementById(id);
            if (campo) {
                campo.value = valor || '';
                
                // Trigger evento change para validações
                campo.dispatchEvent(new Event('change', { bubbles: true }));
            }
        });
    }
    
    async marcarEnderecoUtilizado(enderecoId) {
        // Marca que o endereço foi utilizado (para estatísticas)
        try {
            await fetch('/ajax/marcar-endereco-utilizado/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify({ endereco_id: enderecoId })
            });
        } catch (error) {
            console.error('Erro ao marcar endereço como utilizado:', error);
        }
    }
    
    mostrarHistorico(pedidos) {
        if (pedidos.length === 0) return;
        
        const historicoHTML = `
            <div class="card mt-3" id="historico-pedidos">
                <div class="card-header">
                    <h6 class="mb-0">
                        <i class="fas fa-history me-2"></i>
                        Pedidos Recentes
                    </h6>
                </div>
                <div class="card-body">
                    ${pedidos.map(pedido => `
                        <div class="d-flex justify-content-between align-items-center mb-2 p-2 rounded bg-light">
                            <div>
                                <strong>#${pedido.numero}</strong><br>
                                <small class="text-muted">
                                    ${pedido.data} • ${pedido.restaurante}
                                </small>
                            </div>
                            <div class="text-end">
                                <strong class="text-success">R$ ${pedido.valor}</strong><br>
                                <span class="badge bg-secondary">${pedido.status}</span>
                            </div>
                        </div>
                    `).join('')}
                    ${pedidos.length >= 3 ? `
                        <button type="button" class="btn btn-sm btn-outline-primary w-100 mt-2" 
                                onclick="checkout.mostrarHistoricoCompleto()">
                            <i class="fas fa-list me-2"></i>Ver histórico completo
                        </button>
                    ` : ''}
                </div>
            </div>
        `;
        
        this.enderecoSection.insertAdjacentHTML('beforeend', historicoHTML);
    }
    
    async mostrarHistoricoCompleto() {
        if (!this.clienteAtual) return;
        
        try {
            const response = await fetch(`/ajax/historico-completo/?cliente_id=${this.clienteAtual.id}`);
            const data = await response.json();
            
            if (data.success) {
                this.abrirModalHistorico(data);
            }
        } catch (error) {
            console.error('Erro ao buscar histórico completo:', error);
        }
    }
    
    abrirModalHistorico(data) {
        // Criar modal dinamicamente
        const modalHTML = `
            <div class="modal fade" id="historicoModal" tabindex="-1">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">
                                <i class="fas fa-history me-2"></i>
                                Histórico de Pedidos - ${data.cliente.nome}
                            </h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="row mb-3">
                                <div class="col-md-4 text-center">
                                    <div class="card bg-primary text-white">
                                        <div class="card-body">
                                            <h3>${data.cliente.total_pedidos}</h3>
                                            <small>Total de Pedidos</small>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4 text-center">
                                    <div class="card bg-success text-white">
                                        <div class="card-body">
                                            <h3>R$ ${data.cliente.valor_total_gasto}</h3>
                                            <small>Total Gasto</small>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-4 text-center">
                                    <div class="card bg-info text-white">
                                        <div class="card-body">
                                            <h3>${data.pedidos.length}</h3>
                                            <small>Últimos Pedidos</small>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="table-responsive">
                                <table class="table table-striped">
                                    <thead>
                                        <tr>
                                            <th>Pedido</th>
                                            <th>Data</th>
                                            <th>Restaurante</th>
                                            <th>Itens</th>
                                            <th>Valor</th>
                                            <th>Status</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        ${data.pedidos.map(pedido => `
                                            <tr>
                                                <td><strong>#${pedido.numero}</strong></td>
                                                <td>${pedido.data}</td>
                                                <td>${pedido.restaurante}</td>
                                                <td>${pedido.itens_count} itens</td>
                                                <td><strong>R$ ${pedido.valor}</strong></td>
                                                <td><span class="badge bg-secondary">${pedido.status}</span></td>
                                            </tr>
                                        `).join('')}
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Adicionar modal ao DOM
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        
        // Mostrar modal
        const modal = new bootstrap.Modal(document.getElementById('historicoModal'));
        modal.show();
        
        // Remover modal após fechar
        document.getElementById('historicoModal').addEventListener('hidden.bs.modal', function() {
            this.remove();
        });
    }
    
    mostrarFormularioSalvarEndereco() {
        // Implementar formulário para salvar endereço atual
        const endereco = this.coletarDadosEndereco();
        
        if (!endereco.endereco || !endereco.numero || !endereco.bairro) {
            this.mostrarMensagem('Preencha os dados do endereço antes de salvar', 'warning');
            return;
        }
        
        const modalHTML = `
            <div class="modal fade" id="salvarEnderecoModal" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">
                                <i class="fas fa-save me-2"></i>
                                Salvar Endereço
                            </h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="mb-3">
                                <label class="form-label">Nome do endereço:</label>
                                <input type="text" class="form-control" id="apelido-endereco" 
                                       placeholder="Ex: Casa, Trabalho, Casa da Mãe">
                                <small class="text-muted">Escolha um nome para identificar este endereço</small>
                            </div>
                            <div class="card bg-light">
                                <div class="card-body">
                                    <strong>Endereço a ser salvo:</strong><br>
                                    ${endereco.endereco}, ${endereco.numero}<br>
                                    ${endereco.bairro}, ${endereco.cidade}/${endereco.estado}<br>
                                    CEP: ${endereco.cep}
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                            <button type="button" class="btn btn-success" onclick="checkout.salvarEndereco()">
                                <i class="fas fa-save me-2"></i>Salvar
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        const modal = new bootstrap.Modal(document.getElementById('salvarEnderecoModal'));
        modal.show();
        
        document.getElementById('salvarEnderecoModal').addEventListener('hidden.bs.modal', function() {
            this.remove();
        });
    }
    
    async salvarEndereco() {
        const apelido = document.getElementById('apelido-endereco').value.trim();
        
        if (!apelido) {
            this.mostrarMensagem('Digite um nome para o endereço', 'warning');
            return;
        }
        
        if (!this.clienteAtual) {
            this.mostrarMensagem('Cliente não identificado', 'error');
            return;
        }
        
        const endereco = this.coletarDadosEndereco();
        endereco.cliente_id = this.clienteAtual.id;
        endereco.apelido = apelido;
        
        try {
            const response = await fetch('/ajax/salvar-endereco/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify(endereco)
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.mostrarMensagem(data.message, 'success');
                bootstrap.Modal.getInstance(document.getElementById('salvarEnderecoModal')).hide();
                
                // Atualizar lista de endereços
                this.enderecosSalvos.push(data.endereco);
                this.atualizarSeletorEnderecos();
            } else {
                this.mostrarMensagem(data.error, 'error');
            }
            
        } catch (error) {
            console.error('Erro ao salvar endereço:', error);
            this.mostrarMensagem('Erro ao salvar endereço', 'error');
        }
    }
    
    coletarDadosEndereco() {
        return {
            endereco: document.getElementById('id_endereco')?.value || '',
            numero: document.getElementById('id_numero')?.value || '',
            complemento: document.getElementById('id_complemento')?.value || '',
            bairro: document.getElementById('id_bairro')?.value || '',
            cidade: document.getElementById('id_cidade')?.value || '',
            estado: document.getElementById('id_estado')?.value || '',
            cep: document.getElementById('id_cep')?.value || '',
            referencia: document.getElementById('id_referencia')?.value || ''
        };
    }
    
    // Formatadores e validadores
    formatarCelular(valor) {
        const numero = valor.replace(/\D/g, '');
        
        if (numero.length <= 10) {
            return numero.replace(/(\d{2})(\d{4})(\d{4})/, '($1) $2-$3');
        } else {
            return numero.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
        }
    }
    
    formatarCep(valor) {
        const numero = valor.replace(/\D/g, '');
        return numero.replace(/(\d{5})(\d{3})/, '$1-$2');
    }
    
    async validarCep() {
        const cepInput = document.getElementById('id_cep');
        if (!cepInput) return;
        
        const cep = cepInput.value.replace(/\D/g, '');
        
        if (cep.length === 8) {
            try {
                const response = await fetch('/ajax/validar-cep/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': this.getCsrfToken()
                    },
                    body: `cep=${cep}`
                });
                
                const data = await response.json();
                
                if (data.valido) {
                    cepInput.classList.remove('is-invalid');
                    cepInput.classList.add('is-valid');
                    
                    // Se a API retornar dados do endereço, preencher automaticamente
                    if (data.endereco) {
                        document.getElementById('id_endereco').value = data.endereco;
                        document.getElementById('id_bairro').value = data.bairro;
                        document.getElementById('id_cidade').value = data.cidade;
                        document.getElementById('id_estado').value = data.estado;
                    }
                } else {
                    cepInput.classList.remove('is-valid');
                    cepInput.classList.add('is-invalid');
                }
            } catch (error) {
                console.error('Erro ao validar CEP:', error);
            }
        }
    }
    
    validarEmail() {
        const emailInput = document.getElementById('id_email');
        if (!emailInput || !emailInput.value) return;
        
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        
        if (emailRegex.test(emailInput.value)) {
            emailInput.classList.remove('is-invalid');
            emailInput.classList.add('is-valid');
        } else {
            emailInput.classList.remove('is-valid');
            emailInput.classList.add('is-invalid');
        }
    }
    
    validarFormulario() {
        let valido = true;
        
        // Validar campos obrigatórios
        const camposObrigatorios = ['id_nome', 'id_celular', 'id_endereco', 'id_numero', 'id_bairro', 'id_cidade'];
        
        camposObrigatorios.forEach(id => {
            const campo = document.getElementById(id);
            if (campo && !campo.value.trim()) {
                campo.classList.add('is-invalid');
                valido = false;
            } else if (campo) {
                campo.classList.remove('is-invalid');
            }
        });
        
        if (!valido) {
            this.mostrarMensagem('Preencha todos os campos obrigatórios', 'error');
        }
        
        return valido;
    }
    
    // Utilitários
    mostrarCarregando(mostrar) {
        const indicator = document.getElementById('loading-indicator') || this.criarIndicadorCarregamento();
        indicator.style.display = mostrar ? 'block' : 'none';
    }
    
    criarIndicadorCarregamento() {
        const indicator = document.createElement('div');
        indicator.id = 'loading-indicator';
        indicator.innerHTML = `
            <div class="d-flex align-items-center">
                <div class="spinner-border spinner-border-sm me-2" role="status"></div>
                <span>Buscando dados...</span>
            </div>
        `;
        indicator.className = 'text-primary mt-2';
        indicator.style.display = 'none';
        
        this.celularInput.parentNode.appendChild(indicator);
        return indicator;
    }
    
    mostrarMensagem(texto, tipo = 'info') {
        const alertClass = {
            'success': 'alert-success',
            'error': 'alert-danger',
            'warning': 'alert-warning',
            'info': 'alert-info'
        }[tipo] || 'alert-info';
        
        const mensagem = document.createElement('div');
        mensagem.className = `alert ${alertClass} alert-dismissible fade show mt-2`;
        mensagem.innerHTML = `
            ${texto}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // Adicionar no topo do formulário
        const form = this.celularInput.closest('form');
        if (form) {
            form.insertBefore(mensagem, form.firstChild);
        }
        
        // Auto-remover após 5 segundos
        setTimeout(() => {
            if (mensagem.parentNode) {
                mensagem.remove();
            }
        }, 5000);
    }
    
    limparFormulario() {
        this.clienteAtual = null;
        this.enderecosSalvos = [];
        
        this.removerMensagensAnteriores();
        this.removerSeletorEnderecos();
        this.removerHistorico();
    }
    
    removerMensagensAnteriores() {
        document.querySelectorAll('.cliente-encontrado, .alert').forEach(el => {
            if (el.parentNode) el.remove();
        });
    }
    
    removerSeletorEnderecos() {
        const selector = document.getElementById('enderecos-salvos');
        if (selector) selector.remove();
    }
    
    removerHistorico() {
        const historico = document.getElementById('historico-pedidos');
        if (historico) historico.remove();
    }
    
    getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }
}

// Inicializar quando a página carregar
let checkout;
document.addEventListener('DOMContentLoaded', () => {
    checkout = new CheckoutInteligente();
});

// Exportar para uso global
window.CheckoutInteligente = CheckoutInteligente;
