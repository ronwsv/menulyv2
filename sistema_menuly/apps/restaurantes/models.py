"""
Models do sistema de restaurantes - Sistema White Label completo.

Este arquivo contém todos os models necessários para o funcionamento
dos mini-sites de restaurantes com customização completa.
"""
from django.db import models
from django.conf import settings  # Para AUTH_USER_MODEL
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
import uuid


class PlanoMensal(models.Model):
    """Model para planos de assinatura dos lojistas."""
    
    TIPO_CHOICES = [
        ('basico', 'Básico'),
        ('premium', 'Premium'),
        ('enterprise', 'Enterprise'),
    ]
    
    nome = models.CharField(max_length=100, verbose_name='Nome do Plano')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name='Tipo')
    preco_mensal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço Mensal')
    
    # Limitações
    max_pedidos_mes = models.IntegerField(verbose_name='Máximo de Pedidos/Mês')
    max_produtos = models.IntegerField(verbose_name='Máximo de Produtos')
    max_restaurantes = models.IntegerField(default=1, verbose_name='Máximo de Restaurantes')
    
    # Funcionalidades
    tem_impressoras = models.BooleanField(default=False, verbose_name='Suporte a Impressoras')
    tem_multi_unidades = models.BooleanField(default=False, verbose_name='Múltiplas Unidades')
    tem_relatorios = models.BooleanField(default=False, verbose_name='Relatórios Avançados')
    tem_api = models.BooleanField(default=False, verbose_name='Acesso à API')
    tem_dominio_personalizado = models.BooleanField(default=False, verbose_name='Domínio Personalizado')
    
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    
    class Meta:
        verbose_name = 'Plano Mensal'
        verbose_name_plural = 'Planos Mensais'
        ordering = ['preco_mensal']
    
    def __str__(self):
        return f"{self.nome} - R$ {self.preco_mensal}/mês"


class Lojista(models.Model):
    """Model para lojistas (proprietários dos restaurantes) - MANTIDO POR COMPATIBILIDADE."""
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Usuário')
    plano = models.ForeignKey(PlanoMensal, on_delete=models.PROTECT, verbose_name='Plano Atual')
    
    # Informações pessoais
    nome_completo = models.CharField(max_length=200, verbose_name='Nome Completo')
    cpf = models.CharField(max_length=14, unique=True, verbose_name='CPF')
    telefone = models.CharField(max_length=20, verbose_name='Telefone')
    
    # Assinatura
    data_inicio_plano = models.DateTimeField(auto_now_add=True, verbose_name='Início do Plano')
    data_vencimento = models.DateField(verbose_name='Vencimento')
    trial_ativo = models.BooleanField(default=True, verbose_name='Trial Ativo')
    
    # Status
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    suspenso = models.BooleanField(default=False, verbose_name='Suspenso')
    
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        verbose_name = 'Lojista'
        verbose_name_plural = 'Lojistas'
    
    def __str__(self):
        return self.nome_completo
    
    @property
    def pode_criar_restaurante(self):
        """Verifica se o lojista pode criar mais restaurantes."""
        count_restaurantes = self.restaurantes.count()
        return count_restaurantes < self.plano.max_restaurantes


class Restaurante(models.Model):
    """
    Model principal para restaurantes - Sistema White Label completo com Administradores.
    
    Cada restaurante é um mini-site independente com:
    - URL personalizada (slug)
    - Design customizável (cores, logo, banner)
    - Sistema de administradores com permissões granulares
    - Configurações próprias
    """
    
    # Relacionamentos principais
    lojista = models.ForeignKey(Lojista, on_delete=models.CASCADE, related_name='restaurantes', verbose_name='Lojista')
    
    # Sistema de administradores (novo)
    administradores = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        through='RestauranteAdministrador',
        through_fields=('restaurante', 'usuario'),  # Especifica quais campos usar
        related_name='restaurantes_gerenciados',
        blank=True,
        verbose_name='Administradores'
    )
    
    # Informações básicas
    nome = models.CharField(max_length=200, verbose_name='Nome do Restaurante')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL Personalizada')
    cnpj = models.CharField(max_length=18, blank=True, verbose_name='CNPJ')
    email = models.EmailField(verbose_name='Email')
    telefone = models.CharField(max_length=20, verbose_name='Telefone')
    whatsapp = models.CharField(max_length=20, blank=True, verbose_name='WhatsApp')
    
    # Endereço completo
    endereco_rua = models.CharField(max_length=200, verbose_name='Rua')
    endereco_numero = models.CharField(max_length=20, verbose_name='Número')
    endereco_complemento = models.CharField(max_length=100, blank=True, verbose_name='Complemento')
    endereco_bairro = models.CharField(max_length=100, verbose_name='Bairro')
    endereco_cidade = models.CharField(max_length=100, verbose_name='Cidade')
    endereco_estado = models.CharField(max_length=2, verbose_name='Estado')
    endereco_cep = models.CharField(max_length=9, verbose_name='CEP')
    
    # Customização visual (White Label)
    cor_primaria = models.CharField(max_length=7, default='#667eea', verbose_name='Cor Primária')
    cor_secundaria = models.CharField(max_length=7, default='#764ba2', verbose_name='Cor Secundária')
    cor_fundo = models.CharField(max_length=7, default='#ffffff', verbose_name='Cor de Fundo')
    cor_texto = models.CharField(max_length=7, default='#333333', verbose_name='Cor do Texto')
    cor_botoes = models.CharField(max_length=7, default='#28a745', verbose_name='Cor dos Botões')
    
    # Imagens
    logo = models.ImageField(upload_to='restaurantes/logos/', blank=True, verbose_name='Logo')
    logo_thumbnail = ImageSpecField(source='logo', processors=[ResizeToFill(200, 200)], format='PNG')
    
    banner = models.ImageField(upload_to='restaurantes/banners/', blank=True, verbose_name='Banner Principal')
    banner_small = ImageSpecField(source='banner', processors=[ResizeToFill(800, 400)], format='JPEG')
    
    favicon = models.ImageField(upload_to='restaurantes/favicons/', blank=True, verbose_name='Favicon')
    
    # Textos personalizados
    slogan = models.CharField(max_length=200, blank=True, verbose_name='Slogan')
    mensagem_boas_vindas = models.TextField(blank=True, verbose_name='Mensagem de Boas-vindas')
    sobre_nos = models.TextField(blank=True, verbose_name='Sobre Nós')
    
    # Configurações de delivery
    taxa_entrega = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name='Taxa de Entrega')
    tempo_estimado_entrega = models.IntegerField(default=30, verbose_name='Tempo Estimado (min)')
    raio_entrega_km = models.DecimalField(max_digits=5, decimal_places=2, default=5, verbose_name='Raio de Entrega (km)')
    
    # Configurações de funcionamento
    aceita_pedidos = models.BooleanField(default=True, verbose_name='Aceita Pedidos')
    pedido_minimo = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name='Pedido Mínimo')
    
    # Horários de funcionamento (JSON ou campos separados)
    # Para simplicidade, vou usar campos booleanos + horários
    funciona_segunda = models.BooleanField(default=True, verbose_name='Funciona Segunda')
    horario_segunda_abertura = models.TimeField(null=True, blank=True, verbose_name='Abertura Segunda')
    horario_segunda_fechamento = models.TimeField(null=True, blank=True, verbose_name='Fechamento Segunda')
    
    funciona_terca = models.BooleanField(default=True, verbose_name='Funciona Terça')
    horario_terca_abertura = models.TimeField(null=True, blank=True, verbose_name='Abertura Terça')
    horario_terca_fechamento = models.TimeField(null=True, blank=True, verbose_name='Fechamento Terça')
    
    funciona_quarta = models.BooleanField(default=True, verbose_name='Funciona Quarta')
    horario_quarta_abertura = models.TimeField(null=True, blank=True, verbose_name='Abertura Quarta')
    horario_quarta_fechamento = models.TimeField(null=True, blank=True, verbose_name='Fechamento Quarta')
    
    funciona_quinta = models.BooleanField(default=True, verbose_name='Funciona Quinta')
    horario_quinta_abertura = models.TimeField(null=True, blank=True, verbose_name='Abertura Quinta')
    horario_quinta_fechamento = models.TimeField(null=True, blank=True, verbose_name='Fechamento Quinta')
    
    funciona_sexta = models.BooleanField(default=True, verbose_name='Funciona Sexta')
    horario_sexta_abertura = models.TimeField(null=True, blank=True, verbose_name='Abertura Sexta')
    horario_sexta_fechamento = models.TimeField(null=True, blank=True, verbose_name='Fechamento Sexta')
    
    funciona_sabado = models.BooleanField(default=True, verbose_name='Funciona Sábado')
    horario_sabado_abertura = models.TimeField(null=True, blank=True, verbose_name='Abertura Sábado')
    horario_sabado_fechamento = models.TimeField(null=True, blank=True, verbose_name='Fechamento Sábado')
    
    funciona_domingo = models.BooleanField(default=False, verbose_name='Funciona Domingo')
    horario_domingo_abertura = models.TimeField(null=True, blank=True, verbose_name='Abertura Domingo')
    horario_domingo_fechamento = models.TimeField(null=True, blank=True, verbose_name='Fechamento Domingo')
    
    # Status e controle
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    aprovado = models.BooleanField(default=False, verbose_name='Aprovado')
    destaque = models.BooleanField(default=False, verbose_name='Em Destaque')
    
    # Meta dados
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        verbose_name = 'Restaurante'
        verbose_name_plural = 'Restaurantes'
        ordering = ['nome']
    
    def __str__(self):
        return self.nome
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """URL do mini-site do restaurante."""
        return f"/{self.slug}/"
    
    @property
    def endereco_completo(self):
        """Retorna o endereço completo formatado."""
        endereco = f"{self.endereco_rua}, {self.endereco_numero}"
        if self.endereco_complemento:
            endereco += f", {self.endereco_complemento}"
        endereco += f" - {self.endereco_bairro}, {self.endereco_cidade}/{self.endereco_estado}"
        return endereco
    
    @property
    def esta_aberto(self):
        """Verifica se o restaurante está aberto no momento."""
        # TODO: Implementar lógica de horário de funcionamento
        return self.aceita_pedidos and self.ativo


class Categoria(models.Model):
    """Categorias de produtos para organizar o cardápio."""
    
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, related_name='categorias', verbose_name='Restaurante')
    nome = models.CharField(max_length=100, verbose_name='Nome da Categoria')
    descricao = models.TextField(blank=True, verbose_name='Descrição')
    imagem = models.ImageField(upload_to='categorias/', blank=True, verbose_name='Imagem')
    ordem = models.IntegerField(default=0, verbose_name='Ordem de Exibição')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    
    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['ordem', 'nome']
        unique_together = ['restaurante', 'nome']
    
    def __str__(self):
        return f"{self.restaurante.nome} - {self.nome}"


class Produto(models.Model):
    """Produtos do cardápio de cada restaurante."""
    
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, related_name='produtos', verbose_name='Restaurante')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='produtos', verbose_name='Categoria')
    
    # Informações básicas
    nome = models.CharField(max_length=200, verbose_name='Nome do Produto')
    descricao = models.TextField(verbose_name='Descrição')
    preco = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Preço')
    
    # Imagens (principal + 2 extras)
    imagem_principal = models.ImageField(upload_to='produtos/', verbose_name='Imagem Principal')
    imagem_principal_thumb = ImageSpecField(source='imagem_principal', processors=[ResizeToFill(300, 300)], format='JPEG')
    
    imagem_extra_1 = models.ImageField(upload_to='produtos/', blank=True, verbose_name='Imagem Extra 1')
    imagem_extra_2 = models.ImageField(upload_to='produtos/', blank=True, verbose_name='Imagem Extra 2')
    
    # Configurações
    disponivel = models.BooleanField(default=True, verbose_name='Disponível')
    destaque = models.BooleanField(default=False, verbose_name='Em Destaque')
    ordem = models.IntegerField(default=0, verbose_name='Ordem de Exibição')
    
    # Informações extras
    calorias = models.IntegerField(null=True, blank=True, verbose_name='Calorias')
    tempo_preparo = models.IntegerField(default=15, verbose_name='Tempo de Preparo (min)')
    ingredientes = models.TextField(blank=True, verbose_name='Ingredientes')
    alergenos = models.TextField(blank=True, verbose_name='Alergênicos')
    
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['categoria', 'ordem', 'nome']
    
    def __str__(self):
        return f"{self.restaurante.nome} - {self.nome}"


class OpcoesProduto(models.Model):
    """Grupos de opções para produtos (ex: Tamanho, Adicionais)."""
    
    TIPO_CHOICES = [
        ('radio', 'Seleção Única (Radio)'),
        ('checkbox', 'Múltipla Seleção (Checkbox)'),
    ]
    
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='opcoes', verbose_name='Produto')
    nome = models.CharField(max_length=100, verbose_name='Nome do Grupo')  # Ex: "Tamanho", "Adicionais"
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='radio', verbose_name='Tipo de Seleção')
    obrigatorio = models.BooleanField(default=False, verbose_name='Obrigatório')
    ordem = models.IntegerField(default=0, verbose_name='Ordem')
    
    class Meta:
        verbose_name = 'Opções do Produto'
        verbose_name_plural = 'Opções dos Produtos'
        ordering = ['ordem', 'nome']
    
    def __str__(self):
        return f"{self.produto.nome} - {self.nome}"


class ItemOpcao(models.Model):
    """Itens de cada grupo de opções."""
    
    opcao = models.ForeignKey(OpcoesProduto, on_delete=models.CASCADE, related_name='itens', verbose_name='Opção')
    nome = models.CharField(max_length=100, verbose_name='Nome do Item')  # Ex: "Grande", "Queijo Extra"
    preco_adicional = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name='Preço Adicional')
    disponivel = models.BooleanField(default=True, verbose_name='Disponível')
    ordem = models.IntegerField(default=0, verbose_name='Ordem')
    
    class Meta:
        verbose_name = 'Item da Opção'
        verbose_name_plural = 'Itens das Opções'
        ordering = ['ordem', 'nome']
    
    def __str__(self):
        return f"{self.opcao.nome} - {self.nome}"


class ConfiguracaoImpressora(models.Model):
    """Configurações de impressoras térmicas para cada restaurante."""
    
    TIPO_CHOICES = [
        ('termica', 'Térmica'),
        ('laser', 'Laser'),
    ]
    
    CONEXAO_CHOICES = [
        ('usb', 'USB'),
        ('rede', 'Rede'),
    ]
    
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, related_name='impressoras', verbose_name='Restaurante')
    nome = models.CharField(max_length=100, verbose_name='Nome da Impressora')
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='termica', verbose_name='Tipo')
    conexao = models.CharField(max_length=10, choices=CONEXAO_CHOICES, default='usb', verbose_name='Tipo de Conexão')
    
    # Configurações de conexão
    ip_rede = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP da Rede')
    porta_rede = models.IntegerField(null=True, blank=True, verbose_name='Porta')
    caminho_usb = models.CharField(max_length=200, blank=True, verbose_name='Caminho USB')
    
    # Configurações de impressão
    auto_imprimir = models.BooleanField(default=True, verbose_name='Impressão Automática')
    cortar_papel = models.BooleanField(default=True, verbose_name='Cortar Papel')
    largura_papel = models.IntegerField(default=80, verbose_name='Largura do Papel (mm)')
    
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    
    class Meta:
        verbose_name = 'Configuração de Impressora'
        verbose_name_plural = 'Configurações de Impressoras'
    
    def __str__(self):
        return f"{self.restaurante.nome} - {self.nome}"


class RestauranteAdministrador(models.Model):
    """
    Tabela intermediária para administradores do restaurante com níveis de acesso.
    
    Permite que lojistas adicionem gerentes e funcionários aos seus restaurantes
    com permissões específicas para cada função.
    """
    
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, verbose_name='Restaurante')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Usuário')
    
    NIVEL_ACESSO = (
        ('gerente', 'Gerente'),
        ('funcionario', 'Funcionário'),
    )
    nivel = models.CharField(max_length=15, choices=NIVEL_ACESSO, verbose_name='Nível de Acesso')
    
    # Permissões específicas
    pode_editar_produtos = models.BooleanField(default=True, verbose_name='Pode Editar Produtos')
    pode_editar_configuracoes = models.BooleanField(default=False, verbose_name='Pode Editar Configurações')  # Só gerente
    pode_ver_relatorios = models.BooleanField(default=True, verbose_name='Pode Ver Relatórios')
    pode_gerenciar_usuarios = models.BooleanField(default=False, verbose_name='Pode Gerenciar Usuários')  # Só gerente
    pode_editar_pedidos = models.BooleanField(default=True, verbose_name='Pode Editar Pedidos')
    pode_configurar_impressoras = models.BooleanField(default=False, verbose_name='Pode Configurar Impressoras')
    pode_ver_financeiro = models.BooleanField(default=False, verbose_name='Pode Ver Financeiro')
    
    # Controle
    data_adicionado = models.DateTimeField(auto_now_add=True, verbose_name='Data de Adição')
    adicionado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='administradores_adicionados',
        verbose_name='Adicionado por'
    )
    ativo = models.BooleanField(default=True, verbose_name='Ativo')
    
    class Meta:
        unique_together = ['restaurante', 'usuario']
        verbose_name = 'Administrador do Restaurante'
        verbose_name_plural = 'Administradores dos Restaurantes'
        
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.restaurante.nome} ({self.get_nivel_display()})"
        
    def save(self, *args, **kwargs):
        """Auto-define permissões baseado no nível."""
        if self.nivel == 'gerente':
            self.pode_editar_configuracoes = True
            self.pode_gerenciar_usuarios = True
            self.pode_configurar_impressoras = True
            self.pode_ver_financeiro = True
        elif self.nivel == 'funcionario':
            self.pode_editar_configuracoes = False
            self.pode_gerenciar_usuarios = False
            self.pode_configurar_impressoras = False
            self.pode_ver_financeiro = False
            
        super().save(*args, **kwargs)
