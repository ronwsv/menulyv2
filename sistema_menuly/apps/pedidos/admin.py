"""
Admin para o sistema de pedidos.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Cliente, Pedido, ItemPedido


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ['subtotal_display']
    
    def subtotal_display(self, obj):
        return f"R$ {obj.subtotal:.2f}"
    subtotal_display.short_description = 'Subtotal'


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'telefone', 'email', 'cidade_estado', 'criado_em']
    list_filter = ['endereco_cidade', 'endereco_estado', 'criado_em']
    search_fields = ['nome', 'telefone', 'email']
    readonly_fields = ['criado_em']
    
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome', 'telefone', 'email')
        }),
        ('Endereço Padrão', {
            'fields': (
                'endereco_rua', 'endereco_numero', 'endereco_complemento',
                'endereco_bairro', 'endereco_cidade', 'endereco_estado',
                'endereco_cep', 'endereco_referencia'
            )
        }),
        ('Meta Dados', {
            'fields': ('criado_em',),
            'classes': ('collapse',)
        }),
    )
    
    def cidade_estado(self, obj):
        if obj.endereco_cidade and obj.endereco_estado:
            return f"{obj.endereco_cidade}/{obj.endereco_estado}"
        return "-"
    cidade_estado.short_description = 'Cidade/Estado'


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = [
        'numero', 'restaurante', 'cliente_nome', 'status_display', 
        'tipo', 'total', 'forma_pagamento', 'criado_em'
    ]
    list_filter = [
        'status', 'tipo', 'forma_pagamento', 'restaurante', 
        'criado_em', 'confirmado_em'
    ]
    search_fields = [
        'numero', 'cliente__nome', 'cliente__telefone', 
        'restaurante__nome'
    ]
    readonly_fields = [
        'numero', 'criado_em', 'confirmado_em', 'pronto_em', 
        'entregue_em', 'valor_troco_display'
    ]
    
    inlines = [ItemPedidoInline]
    
    fieldsets = (
        ('Identificação', {
            'fields': ('numero', 'restaurante', 'cliente')
        }),
        ('Status e Tipo', {
            'fields': ('status', 'tipo')
        }),
        ('Endereço de Entrega', {
            'fields': (
                'endereco_entrega_rua', 'endereco_entrega_numero', 
                'endereco_entrega_complemento', 'endereco_entrega_bairro',
                'endereco_entrega_cidade', 'endereco_entrega_estado',
                'endereco_entrega_cep', 'endereco_entrega_referencia'
            )
        }),
        ('Valores', {
            'fields': ('subtotal', 'taxa_entrega', 'desconto', 'total')
        }),
        ('Pagamento', {
            'fields': ('forma_pagamento', 'troco_para', 'valor_troco_display')
        }),
        ('Observações', {
            'fields': ('observacoes',)
        }),
        ('Timestamps', {
            'fields': (
                'criado_em', 'confirmado_em', 'pronto_em', 'entregue_em'
            ),
            'classes': ('collapse',)
        }),
    )
    
    def cliente_nome(self, obj):
        return obj.cliente.nome
    cliente_nome.short_description = 'Cliente'
    
    def status_display(self, obj):
        colors = {
            'recebido': '#ffc107',
            'confirmado': '#17a2b8',
            'preparando': '#fd7e14',
            'pronto': '#20c997',
            'saiu_entrega': '#6f42c1',
            'entregue': '#28a745',
            'cancelado': '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_display.short_description = 'Status'
    
    def valor_troco_display(self, obj):
        if obj.valor_troco > 0:
            return f"R$ {obj.valor_troco:.2f}"
        return "Não há troco"
    valor_troco_display.short_description = 'Valor do Troco'


@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ['pedido', 'produto', 'quantidade', 'preco_unitario', 'subtotal_display']
    list_filter = ['pedido__restaurante', 'produto__categoria']
    search_fields = ['pedido__numero', 'produto__nome']
    
    def subtotal_display(self, obj):
        return f"R$ {obj.subtotal:.2f}"
    subtotal_display.short_description = 'Subtotal'
