"""
Modelos de usuário customizado baseado na estrutura otimizada.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """Modelo de usuário customizado com tipos específicos."""
    
    TIPO_USUARIO = (
        ('superadmin', 'Super Administrador'),
        ('lojista', 'Lojista/Proprietário'),
        ('gerente', 'Gerente'),
        ('funcionario', 'Funcionário'),
        ('cliente', 'Cliente'),
    )
    
    tipo = models.CharField(max_length=15, choices=TIPO_USUARIO, default='cliente')
    celular = models.CharField(max_length=20, blank=True, null=True)
    cpf = models.CharField(max_length=14, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'auth_user'
        
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_tipo_display()})"


class PlanoMensal(models.Model):
    """Planos de assinatura para lojistas."""
    
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    limite_restaurantes = models.IntegerField()
    limite_produtos = models.IntegerField()
    suporte_whitelabel = models.BooleanField(default=False)
    suporte_api = models.BooleanField(default=False)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['preco']
        
    def __str__(self):
        return f"{self.nome} - R$ {self.preco}"


class PerfilLojista(models.Model):
    """Perfil específico para lojistas/proprietários."""
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_lojista')
    cnpj = models.CharField(max_length=18, unique=True)
    razao_social = models.CharField(max_length=200)
    inscricao_estadual = models.CharField(max_length=20, blank=True)
    plano = models.ForeignKey(PlanoMensal, on_delete=models.PROTECT)
    data_vencimento = models.DateField()
    
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('suspenso', 'Suspenso'),
        ('trial', 'Trial'),
        ('cancelado', 'Cancelado')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='trial')
    
    # Configurações do lojista
    pode_criar_restaurante = models.BooleanField(default=True)
    notificacoes_email = models.BooleanField(default=True)
    notificacoes_whatsapp = models.BooleanField(default=False)
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Perfil Lojista'
        verbose_name_plural = 'Perfis Lojistas'
        
    def __str__(self):
        return f"{self.razao_social} - {self.usuario.get_full_name()}"
        
    @property
    def esta_ativo(self):
        """Verifica se o lojista está com o plano ativo."""
        return (
            self.status in ['ativo', 'trial'] and 
            self.data_vencimento >= timezone.now().date()
        )
        
    def pode_criar_mais_restaurantes(self):
        """Verifica se pode criar mais restaurantes baseado no plano."""
        total_restaurantes = self.restaurantes.count()
        return total_restaurantes < self.plano.limite_restaurantes


class Cliente(models.Model):
    """Cliente que faz pedidos (sistema guest inteligente)."""
    
    nome = models.CharField(max_length=100)
    celular = models.CharField(max_length=20, unique=True, help_text="Chave única para busca automática")
    email = models.EmailField(blank=True, null=True)
    
    # Endereço principal (referência rápida)
    endereco_principal = models.ForeignKey(
        'EnderecoCliente', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='clientes_principais'
    )
    
    # Estatísticas e controle
    primeira_compra = models.DateTimeField(auto_now_add=True)
    ultima_compra = models.DateTimeField(auto_now=True)
    total_pedidos = models.IntegerField(default=0)
    valor_total_gasto = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Preferências
    aceita_marketing = models.BooleanField(default=False)
    observacoes = models.TextField(blank=True, help_text="Observações internas sobre o cliente")
    
    class Meta:
        ordering = ['-ultima_compra']
        indexes = [
            models.Index(fields=['celular']),
            models.Index(fields=['ultima_compra']),
        ]
        
    def __str__(self):
        return f"{self.nome} - {self.celular}"
        
    def get_enderecos(self):
        """Retorna endereços ativos do cliente."""
        return self.enderecos.filter(ativo=True).order_by('-criado_em')
        
    def incrementar_pedido(self, valor):
        """Incrementa contadores após novo pedido."""
        self.total_pedidos += 1
        self.valor_total_gasto += valor
        self.ultima_compra = timezone.now()
        self.save(update_fields=['total_pedidos', 'valor_total_gasto', 'ultima_compra'])


class EnderecoCliente(models.Model):
    """Endereços salvos do cliente para reutilização."""
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='enderecos')
    apelido = models.CharField(max_length=50, help_text="Ex: Casa, Trabalho, Casa da Mãe")
    
    # Endereço completo
    endereco = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    cep = models.CharField(max_length=9)
    
    # Informações adicionais
    referencia = models.CharField(max_length=200, blank=True, help_text="Ponto de referência")
    
    # Controle
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    ultima_utilizacao = models.DateTimeField(null=True, blank=True)
    vezes_utilizado = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-ultima_utilizacao', '-criado_em']
        indexes = [
            models.Index(fields=['cliente', 'ativo']),
        ]
        
    def __str__(self):
        return f"{self.cliente.nome} - {self.apelido}"
        
    @property
    def endereco_completo(self):
        """Retorna o endereço formatado."""
        endereco = f"{self.endereco}, {self.numero}"
        if self.complemento:
            endereco += f", {self.complemento}"
        endereco += f" - {self.bairro}, {self.cidade}/{self.estado}"
        return endereco
        
    def marcar_utilizacao(self):
        """Marca que o endereço foi utilizado."""
        self.ultima_utilizacao = timezone.now()
        self.vezes_utilizado += 1
        self.save(update_fields=['ultima_utilizacao', 'vezes_utilizado'])
