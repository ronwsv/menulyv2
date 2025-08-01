"""
Modelos para sistema de Templates White Label - FASE 2
Gerencia temas, cores e personalizações visuais por restaurante
"""
from django.db import models
from django.core.validators import RegexValidator
from apps.restaurantes.models import Restaurante


class TemaRestaurante(models.Model):
    """
    Modelo para gerenciar temas visuais personalizados de cada restaurante
    """
    TIPOS_TEMA = [
        ('moderno', 'Moderno'),
        ('classico', 'Clássico'),
        ('minimalista', 'Minimalista'),
        ('colorido', 'Colorido'),
        ('elegante', 'Elegante'),
        ('casual', 'Casual'),
        ('premium', 'Premium'),
    ]
    
    restaurante = models.OneToOneField(
        Restaurante,
        on_delete=models.CASCADE,
        related_name='tema',
        verbose_name='Restaurante'
    )
    
    # Configurações básicas do tema
    tipo_tema = models.CharField(
        max_length=20,
        choices=TIPOS_TEMA,
        default='moderno',
        verbose_name='Tipo do Tema'
    )
    
    nome_personalizado = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Nome Personalizado do Tema'
    )
    
    # Cores personalizadas
    cor_hex_validator = RegexValidator(
        regex=r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
        message='Formato de cor inválido. Use #RRGGBB ou #RGB'
    )
    
    cor_primaria = models.CharField(
        max_length=7,
        validators=[cor_hex_validator],
        default='#007bff',
        verbose_name='Cor Primária',
        help_text='Cor principal do tema (ex: #007bff)'
    )
    
    cor_secundaria = models.CharField(
        max_length=7,
        validators=[cor_hex_validator],
        default='#6c757d',
        verbose_name='Cor Secundária',
        help_text='Cor secundária do tema (ex: #6c757d)'
    )
    
    cor_fundo = models.CharField(
        max_length=7,
        validators=[cor_hex_validator],
        default='#ffffff',
        verbose_name='Cor de Fundo',
        help_text='Cor de fundo da página (ex: #ffffff)'
    )
    
    cor_texto = models.CharField(
        max_length=7,
        validators=[cor_hex_validator],
        default='#212529',
        verbose_name='Cor do Texto',
        help_text='Cor principal do texto (ex: #212529)'
    )
    
    cor_botao = models.CharField(
        max_length=7,
        validators=[cor_hex_validator],
        default='#28a745',
        verbose_name='Cor dos Botões',
        help_text='Cor dos botões de ação (ex: #28a745)'
    )
    
    # Configurações de tipografia
    fonte_primaria = models.CharField(
        max_length=100,
        default='Roboto, sans-serif',
        verbose_name='Fonte Primária',
        help_text='Fonte principal do site'
    )
    
    fonte_secundaria = models.CharField(
        max_length=100,
        default='Open Sans, sans-serif',
        verbose_name='Fonte Secundária',
        help_text='Fonte para títulos e destaques'
    )
    
    tamanho_fonte_base = models.IntegerField(
        default=16,
        verbose_name='Tamanho Base da Fonte (px)',
        help_text='Tamanho base da fonte em pixels'
    )
    
    # Configurações de layout
    largura_maxima = models.IntegerField(
        default=1200,
        verbose_name='Largura Máxima (px)',
        help_text='Largura máxima do conteúdo em pixels'
    )
    
    espacamento_geral = models.IntegerField(
        default=15,
        verbose_name='Espaçamento Geral (px)',
        help_text='Espaçamento padrão entre elementos'
    )
    
    border_radius = models.IntegerField(
        default=8,
        verbose_name='Raio da Borda (px)',
        help_text='Arredondamento dos cantos em pixels'
    )
    
    # Configurações de imagens
    logo_principal = models.ImageField(
        upload_to='temas/logos/',
        blank=True,
        null=True,
        verbose_name='Logo Principal',
        help_text='Logo principal do restaurante'
    )
    
    logo_pequeno = models.ImageField(
        upload_to='temas/logos/',
        blank=True,
        null=True,
        verbose_name='Logo Pequeno',
        help_text='Logo pequeno para cabeçalho compacto'
    )
    
    favicon = models.ImageField(
        upload_to='temas/favicons/',
        blank=True,
        null=True,
        verbose_name='Favicon',
        help_text='Ícone da aba do navegador (16x16 ou 32x32 px)'
    )
    
    imagem_fundo_hero = models.ImageField(
        upload_to='temas/backgrounds/',
        blank=True,
        null=True,
        verbose_name='Imagem de Fundo Hero',
        help_text='Imagem de fundo da seção principal'
    )
    
    # Configurações avançadas
    css_personalizado = models.TextField(
        blank=True,
        null=True,
        verbose_name='CSS Personalizado',
        help_text='CSS adicional para customizações avançadas'
    )
    
    javascript_personalizado = models.TextField(
        blank=True,
        null=True,
        verbose_name='JavaScript Personalizado',
        help_text='JavaScript adicional para funcionalidades específicas'
    )
    
    # Meta configurações
    ativo = models.BooleanField(
        default=True,
        verbose_name='Tema Ativo'
    )
    
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    
    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )
    
    class Meta:
        verbose_name = 'Tema do Restaurante'
        verbose_name_plural = 'Temas dos Restaurantes'
        db_table = 'temas_restaurantes'
    
    def __str__(self):
        return f"Tema {self.get_tipo_tema_display()} - {self.restaurante.nome}"
    
    def get_css_variables(self):
        """
        Retorna as variáveis CSS para aplicar no template
        """
        return {
            '--cor-primaria': self.cor_primaria,
            '--cor-secundaria': self.cor_secundaria,
            '--cor-fundo': self.cor_fundo,
            '--cor-texto': self.cor_texto,
            '--cor-botao': self.cor_botao,
            '--fonte-primaria': self.fonte_primaria,
            '--fonte-secundaria': self.fonte_secundaria,
            '--tamanho-fonte-base': f'{self.tamanho_fonte_base}px',
            '--largura-maxima': f'{self.largura_maxima}px',
            '--espacamento-geral': f'{self.espacamento_geral}px',
            '--border-radius': f'{self.border_radius}px',
        }
    
    def get_tema_classes(self):
        """
        Retorna classes CSS específicas do tema
        """
        return f'tema-{self.tipo_tema} restaurante-{self.restaurante.slug}'


class ComponentePersonalizado(models.Model):
    """
    Modelo para componentes personalizados do tema
    """
    TIPOS_COMPONENTE = [
        ('header', 'Cabeçalho'),
        ('footer', 'Rodapé'),
        ('menu', 'Menu de Navegação'),
        ('banner', 'Banner Principal'),
        ('galeria', 'Galeria de Fotos'),
        ('contato', 'Seção de Contato'),
        ('sobre', 'Seção Sobre Nós'),
        ('produtos', 'Lista de Produtos'),
        ('promocoes', 'Seção de Promoções'),
    ]
    
    tema = models.ForeignKey(
        TemaRestaurante,
        on_delete=models.CASCADE,
        related_name='componentes',
        verbose_name='Tema'
    )
    
    tipo_componente = models.CharField(
        max_length=20,
        choices=TIPOS_COMPONENTE,
        verbose_name='Tipo do Componente'
    )
    
    nome = models.CharField(
        max_length=100,
        verbose_name='Nome do Componente'
    )
    
    template_html = models.TextField(
        verbose_name='Template HTML',
        help_text='Código HTML do componente'
    )
    
    css_componente = models.TextField(
        blank=True,
        null=True,
        verbose_name='CSS do Componente',
        help_text='CSS específico do componente'
    )
    
    ordem = models.IntegerField(
        default=0,
        verbose_name='Ordem de Exibição'
    )
    
    ativo = models.BooleanField(
        default=True,
        verbose_name='Componente Ativo'
    )
    
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    
    class Meta:
        verbose_name = 'Componente Personalizado'
        verbose_name_plural = 'Componentes Personalizados'
        db_table = 'componentes_personalizados'
        ordering = ['ordem', 'nome']
    
    def __str__(self):
        return f"{self.get_tipo_componente_display()} - {self.nome}"
