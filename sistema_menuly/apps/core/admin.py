"""
Admin para gerenciar Templates White Label - FASE 2
Interface administrativa para temas e componentes personalizados
"""
from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import TemaRestaurante, ComponentePersonalizado


@admin.register(TemaRestaurante)
class TemaRestauranteAdmin(admin.ModelAdmin):
    list_display = [
        'restaurante', 
        'tipo_tema', 
        'preview_cores', 
        'ativo', 
        'atualizado_em'
    ]
    list_filter = [
        'tipo_tema', 
        'ativo', 
        'criado_em'
    ]
    search_fields = [
        'restaurante__nome', 
        'restaurante__slug', 
        'nome_personalizado'
    ]
    readonly_fields = [
        'criado_em', 
        'atualizado_em', 
        'preview_tema'
    ]
    
    fieldsets = (
        ('Configurações Básicas', {
            'fields': (
                'restaurante',
                'tipo_tema',
                'nome_personalizado',
                'ativo'
            )
        }),
        ('Cores do Tema', {
            'fields': (
                'cor_primaria',
                'cor_secundaria',
                'cor_fundo',
                'cor_texto',
                'cor_botao'
            ),
            'classes': ('collapse',)
        }),
        ('Tipografia', {
            'fields': (
                'fonte_primaria',
                'fonte_secundaria',
                'tamanho_fonte_base'
            ),
            'classes': ('collapse',)
        }),
        ('Layout', {
            'fields': (
                'largura_maxima',
                'espacamento_geral',
                'border_radius'
            ),
            'classes': ('collapse',)
        }),
        ('Imagens', {
            'fields': (
                'logo_principal',
                'logo_pequeno',
                'favicon',
                'imagem_fundo_hero'
            ),
            'classes': ('collapse',)
        }),
        ('Personalizações Avançadas', {
            'fields': (
                'css_personalizado',
                'javascript_personalizado'
            ),
            'classes': ('collapse',)
        }),
        ('Informações do Sistema', {
            'fields': (
                'criado_em',
                'atualizado_em',
                'preview_tema'
            ),
            'classes': ('collapse',)
        })
    )
    
    def preview_cores(self, obj):
        """Mostra preview das cores principais"""
        html = f'''
        <div style="display: flex; gap: 5px;">
            <div style="width: 20px; height: 20px; background-color: {obj.cor_primaria}; border: 1px solid #ccc; border-radius: 3px;" title="Primária: {obj.cor_primaria}"></div>
            <div style="width: 20px; height: 20px; background-color: {obj.cor_secundaria}; border: 1px solid #ccc; border-radius: 3px;" title="Secundária: {obj.cor_secundaria}"></div>
            <div style="width: 20px; height: 20px; background-color: {obj.cor_botao}; border: 1px solid #ccc; border-radius: 3px;" title="Botão: {obj.cor_botao}"></div>
        </div>
        '''
        return format_html(html)
    preview_cores.short_description = 'Preview Cores'
    
    def preview_tema(self, obj):
        """Mostra preview completo do tema"""
        if not obj.pk:
            return "Salve primeiro para ver o preview"
            
        css_vars = obj.get_css_variables()
        
        html = f'''
        <div style="border: 1px solid #ddd; border-radius: 8px; padding: 20px; background: white;">
            <h3 style="margin: 0 0 15px 0; color: {obj.cor_texto}; font-family: {obj.fonte_secundaria};">
                Preview do Tema: {obj.get_tipo_tema_display()}
            </h3>
            
            <div style="margin-bottom: 15px;">
                <div style="display: inline-block; padding: 8px 16px; background-color: {obj.cor_primaria}; color: white; border-radius: {obj.border_radius}px; font-family: {obj.fonte_primaria}; margin-right: 10px;">
                    Botão Primário
                </div>
                <div style="display: inline-block; padding: 8px 16px; background-color: {obj.cor_botao}; color: white; border-radius: {obj.border_radius}px; font-family: {obj.fonte_primaria};">
                    Botão Ação
                </div>
            </div>
            
            <div style="background-color: {obj.cor_fundo}; padding: 15px; border: 1px solid {obj.cor_secundaria}; border-radius: {obj.border_radius}px; margin-bottom: 15px;">
                <h4 style="color: {obj.cor_texto}; font-family: {obj.fonte_secundaria}; margin: 0 0 10px 0;">
                    Exemplo de Conteúdo
                </h4>
                <p style="color: {obj.cor_texto}; font-family: {obj.fonte_primaria}; font-size: {obj.tamanho_fonte_base}px; margin: 0; line-height: 1.6;">
                    Este é um exemplo de como o texto ficará com as configurações do tema.
                    A fonte primária é {obj.fonte_primaria} e o tamanho base é {obj.tamanho_fonte_base}px.
                </p>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap: 10px; font-size: 12px;">
                <div><strong>Tipo:</strong> {obj.get_tipo_tema_display()}</div>
                <div><strong>Fonte 1:</strong> {obj.fonte_primaria}</div>
                <div><strong>Fonte 2:</strong> {obj.fonte_secundaria}</div>
                <div><strong>Tamanho:</strong> {obj.tamanho_fonte_base}px</div>
                <div><strong>Largura:</strong> {obj.largura_maxima}px</div>
                <div><strong>Espaçamento:</strong> {obj.espacamento_geral}px</div>
            </div>
        </div>
        '''
        return format_html(html)
    preview_tema.short_description = 'Preview Completo'

    class Media:
        css = {
            'all': ('admin/css/tema_admin.css',)
        }
        js = ('admin/js/tema_admin.js',)


class ComponentePersonalizadoInline(admin.TabularInline):
    model = ComponentePersonalizado
    extra = 0
    fields = ['tipo_componente', 'nome', 'ordem', 'ativo']
    readonly_fields = []


@admin.register(ComponentePersonalizado)
class ComponentePersonalizadoAdmin(admin.ModelAdmin):
    list_display = [
        'nome', 
        'tema', 
        'tipo_componente', 
        'ordem', 
        'ativo'
    ]
    list_filter = [
        'tipo_componente', 
        'ativo', 
        'tema__restaurante'
    ]
    search_fields = [
        'nome', 
        'tema__restaurante__nome'
    ]
    
    fieldsets = (
        ('Configurações Básicas', {
            'fields': (
                'tema',
                'tipo_componente',
                'nome',
                'ordem',
                'ativo'
            )
        }),
        ('Conteúdo', {
            'fields': (
                'template_html',
                'css_componente'
            )
        })
    )
    
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name in ['template_html', 'css_componente']:
            kwargs['widget'] = admin.widgets.AdminTextareaWidget(attrs={'rows': 15, 'cols': 80})
        return super().formfield_for_dbfield(db_field, request, **kwargs)


# Adiciona o inline de componentes ao admin do tema
TemaRestauranteAdmin.inlines = [ComponentePersonalizadoInline]
