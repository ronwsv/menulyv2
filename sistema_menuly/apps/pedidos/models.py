"""
Models do sistema de pedidos.
"""
from django.db import models
from django.contrib.auth.models import User
from apps.restaurantes.models import Restaurante, Produto
from apps.accounts.models import Cliente
import uuid


class Pedido(models.Model):
    """Model principal para pedidos."""
    
    STATUS_CHOICES = [
        ('recebido', 'Recebido'),
        ('confirmado', 'Confirmado'),
        ('preparando', 'Preparando'),
        ('pronto', 'Pronto'),
        ('saiu_entrega', 'Saiu para Entrega'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]
    
    TIPO_CHOICES = [
        ('delivery', 'Delivery'),
        ('retirada', 'Retirada no Local'),
    ]
    
    FORMA_PAGAMENTO_CHOICES = [
        ('dinheiro', 'Dinheiro'),
        ('cartao_debito', 'Cartão de Débito'),
        ('cartao_credito', 'Cartão de Crédito'),
        ('pix', 'PIX'),
    ]
    
    # Identificação
    numero = models.CharField(max_length=20, unique=True, verbose_name='Número do Pedido')
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, related_name='pedidos', verbose_name='Restaurante')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pedidos', verbose_name='Cliente')
    
    # Status e tipo
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='recebido', verbose_name='Status')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='delivery', verbose_name='Tipo de Entrega')
    
    # Endereço de entrega (pode ser diferente do endereço padrão do cliente)
    endereco_entrega_rua = models.CharField(max_length=200, verbose_name='Rua')
    endereco_entrega_numero = models.CharField(max_length=20, verbose_name='Número')
    endereco_entrega_complemento = models.CharField(max_length=100, blank=True, verbose_name='Complemento')
    endereco_entrega_bairro = models.CharField(max_length=100, verbose_name='Bairro')
    endereco_entrega_cidade = models.CharField(max_length=100, verbose_name='Cidade')
    endereco_entrega_estado = models.CharField(max_length=2, verbose_name='Estado')
    endereco_entrega_cep = models.CharField(max_length=9, verbose_name='CEP')
    endereco_entrega_referencia = models.CharField(max_length=200, blank=True, verbose_name='Ponto de Referência')
    
    # Valores
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Subtotal')
    taxa_entrega = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name='Taxa de Entrega')
    desconto = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Desconto')
    total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Total')
    
    # Pagamento
    forma_pagamento = models.CharField(max_length=20, choices=FORMA_PAGAMENTO_CHOICES, verbose_name='Forma de Pagamento')
    troco_para = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name='Troco para')
    
    # Observações
    observacoes = models.TextField(blank=True, verbose_name='Observações')
    
    # Timestamps
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    confirmado_em = models.DateTimeField(null=True, blank=True, verbose_name='Confirmado em')
    pronto_em = models.DateTimeField(null=True, blank=True, verbose_name='Pronto em')
    entregue_em = models.DateTimeField(null=True, blank=True, verbose_name='Entregue em')
    
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"Pedido #{self.numero} - {self.restaurante.nome}"
    
    def save(self, *args, **kwargs):
        if not self.numero:
            # Gera número do pedido: RESTAURANTE_ID + TIMESTAMP_SUFFIX
            import time
            timestamp = int(time.time())
            self.numero = f"{self.restaurante.id}{str(timestamp)[-6:]}"
        super().save(*args, **kwargs)
    
    @property
    def endereco_entrega_completo(self):
        """Retorna o endereço de entrega formatado."""
        endereco = f"{self.endereco_entrega_rua}, {self.endereco_entrega_numero}"
        if self.endereco_entrega_complemento:
            endereco += f", {self.endereco_entrega_complemento}"
        endereco += f" - {self.endereco_entrega_bairro}, {self.endereco_entrega_cidade}/{self.endereco_entrega_estado}"
        return endereco
    
    @property
    def valor_troco(self):
        """Calcula o valor do troco."""
        if self.forma_pagamento == 'dinheiro' and self.troco_para:
            return self.troco_para - self.total
        return 0


class ItemPedido(models.Model):
    """Itens individuais de cada pedido."""
    
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='itens', verbose_name='Pedido')
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, verbose_name='Produto')
    
    quantidade = models.PositiveIntegerField(verbose_name='Quantidade')
    preco_unitario = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Preço Unitário')
    
    # Opções selecionadas (JSON ou texto)
    opcoes_selecionadas = models.JSONField(default=dict, blank=True, verbose_name='Opções Selecionadas')
    observacoes = models.TextField(blank=True, verbose_name='Observações do Item')
    
    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'
    
    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome}"
    
    @property
    def subtotal(self):
        """Calcula o subtotal do item."""
        return self.quantidade * self.preco_unitario
