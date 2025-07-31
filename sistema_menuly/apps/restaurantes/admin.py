"""
Admin interface para o sistema de restaurantes.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    PlanoMensal, Lojista, Restaurante, Categoria, 
    Produto, OpcoesProduto, ItemOpcao, ConfiguracaoImpressora
)


@admin.register(PlanoMensal)
class PlanoMensalAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'preco_mensal', 'max_pedidos_mes', 'max_produtos', 'ativo']
    list_filter = ['tipo', 'ativo']
    search_fields = ['nome']
    ordering = ['preco_mensal']


@admin.register(Lojista)
class LojistaAdmin(admin.ModelAdmin):
    list_display = ['nome_completo', 'user', 'plano', 'trial_ativo', 'ativo', 'criado_em']
    list_filter = ['plano', 'trial_ativo', 'ativo', 'suspenso']
    search_fields = ['nome_completo', 'cpf', 'user__username']
    readonly_fields = ['criado_em', 'atualizado_em']


class CategoriaInline(admin.TabularInline):
    model = Categoria
    extra = 1
    fields = ['nome', 'ordem', 'ativo']


class ConfiguracaoImpressoraInline(admin.TabularInline):
    model = ConfiguracaoImpressora
    extra = 0


@admin.register(Restaurante)
class RestauranteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'slug', 'lojista', 'cidade_estado', 'ativo', 'aprovado', 'destaque']
    list_filter = ['ativo', 'aprovado', 'destaque', 'endereco_cidade', 'endereco_estado']
    search_fields = ['nome', 'slug', 'endereco_cidade', 'lojista__nome_completo']
    prepopulated_fields = {'slug': ('nome',)}
    readonly_fields = ['criado_em', 'atualizado_em', 'logo_preview', 'banner_preview']
    
    inlines = [CategoriaInline, ConfiguracaoImpressoraInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('lojista', 'nome', 'slug', 'cnpj', 'email', 'telefone', 'whatsapp')
        }),
        ('Endereço', {
            'fields': (
                'endereco_rua', 'endereco_numero', 'endereco_complemento',
                'endereco_bairro', 'endereco_cidade', 'endereco_estado', 'endereco_cep'
            )
        }),
        ('Customização Visual', {
            'fields': ('cor_primaria', 'cor_secundaria', 'cor_fundo', 'cor_texto', 'cor_botoes')
        }),
        ('Imagens', {
            'fields': ('logo', 'logo_preview', 'banner', 'banner_preview', 'favicon')
        }),
        ('Textos Personalizados', {
            'fields': ('slogan', 'mensagem_boas_vindas', 'sobre_nos')
        }),
        ('Configurações de Delivery', {
            'fields': ('taxa_entrega', 'tempo_estimado_entrega', 'raio_entrega_km', 'pedido_minimo')
        }),
        ('Horários de Funcionamento', {
            'fields': (
                ('funciona_segunda', 'horario_segunda_abertura', 'horario_segunda_fechamento'),
                ('funciona_terca', 'horario_terca_abertura', 'horario_terca_fechamento'),
                ('funciona_quarta', 'horario_quarta_abertura', 'horario_quarta_fechamento'),
                ('funciona_quinta', 'horario_quinta_abertura', 'horario_quinta_fechamento'),
                ('funciona_sexta', 'horario_sexta_abertura', 'horario_sexta_fechamento'),
                ('funciona_sabado', 'horario_sabado_abertura', 'horario_sabado_fechamento'),
                ('funciona_domingo', 'horario_domingo_abertura', 'horario_domingo_fechamento'),
            )
        }),
        ('Status', {
            'fields': ('aceita_pedidos', 'ativo', 'aprovado', 'destaque')
        }),
        ('Meta Dados', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    def cidade_estado(self, obj):
        return f"{obj.endereco_cidade}/{obj.endereco_estado}"
    cidade_estado.short_description = 'Cidade/Estado'
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="width: 100px; height: 100px; object-fit: cover;" />', obj.logo.url)
        return "Sem logo"
    logo_preview.short_description = 'Preview Logo'
    
    def banner_preview(self, obj):
        if obj.banner:
            return format_html('<img src="{}" style="width: 200px; height: 100px; object-fit: cover;" />', obj.banner.url)
        return "Sem banner"
    banner_preview.short_description = 'Preview Banner'


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'restaurante', 'ordem', 'ativo', 'criado_em']
    list_filter = ['ativo', 'restaurante']
    search_fields = ['nome', 'restaurante__nome']
    ordering = ['restaurante', 'ordem', 'nome']


class ItemOpcaoInline(admin.TabularInline):
    model = ItemOpcao
    extra = 1


class OpcoesProdutoInline(admin.TabularInline):
    model = OpcoesProduto
    extra = 0


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'restaurante', 'categoria', 'preco', 'disponivel', 'destaque']
    list_filter = ['disponivel', 'destaque', 'categoria', 'restaurante']
    search_fields = ['nome', 'restaurante__nome', 'categoria__nome']
    readonly_fields = ['criado_em', 'atualizado_em', 'imagem_preview']
    
    inlines = [OpcoesProdutoInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('restaurante', 'categoria', 'nome', 'descricao', 'preco')
        }),
        ('Imagens', {
            'fields': ('imagem_principal', 'imagem_preview', 'imagem_extra_1', 'imagem_extra_2')
        }),
        ('Configurações', {
            'fields': ('disponivel', 'destaque', 'ordem')
        }),
        ('Informações Extras', {
            'fields': ('calorias', 'tempo_preparo', 'ingredientes', 'alergenos')
        }),
        ('Meta Dados', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )
    
    def imagem_preview(self, obj):
        if obj.imagem_principal:
            return format_html('<img src="{}" style="width: 150px; height: 150px; object-fit: cover;" />', obj.imagem_principal.url)
        return "Sem imagem"
    imagem_preview.short_description = 'Preview'


@admin.register(OpcoesProduto)
class OpcoesProdutoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'produto', 'tipo', 'obrigatorio', 'ordem']
    list_filter = ['tipo', 'obrigatorio']
    search_fields = ['nome', 'produto__nome']
    
    inlines = [ItemOpcaoInline]


@admin.register(ItemOpcao)
class ItemOpcaoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'opcao', 'preco_adicional', 'disponivel', 'ordem']
    list_filter = ['disponivel', 'opcao__produto__restaurante']
    search_fields = ['nome', 'opcao__nome']


@admin.register(ConfiguracaoImpressora)
class ConfiguracaoImpressoraAdmin(admin.ModelAdmin):
    list_display = ['nome', 'restaurante', 'tipo', 'conexao', 'ativo']
    list_filter = ['tipo', 'conexao', 'ativo']
    search_fields = ['nome', 'restaurante__nome']
