"""
Modelos de usuário customizado - versão simplificada inicial.
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
    
    tipo_usuario = models.CharField(max_length=15, choices=TIPO_USUARIO, default='cliente')
    telefone = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_tipo_usuario_display()})"


class Cliente(models.Model):
    """Cliente que faz pedidos (sistema guest inteligente)."""
    
    nome = models.CharField(max_length=100, verbose_name='Nome')
    celular = models.CharField(max_length=20, unique=True, verbose_name='Celular')
    email = models.EmailField(blank=True, null=True, verbose_name='Email')
    
    # Estatísticas básicas
    data_primeiro_pedido = models.DateTimeField(auto_now_add=True)
    data_ultimo_pedido = models.DateTimeField(auto_now=True)
    total_pedidos = models.IntegerField(default=0)
    valor_total_gasto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-data_ultimo_pedido']
        
    def __str__(self):
        return f"{self.nome} - {self.celular}"


class EnderecoCliente(models.Model):
    """Endereços salvos dos clientes."""
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='enderecos')
    apelido = models.CharField(max_length=50, verbose_name='Nome do Endereço')
    
    # Dados do endereço
    endereco = models.CharField(max_length=200, verbose_name='Rua/Avenida')
    numero = models.CharField(max_length=10, verbose_name='Número')
    complemento = models.CharField(max_length=100, blank=True, verbose_name='Complemento')
    bairro = models.CharField(max_length=100, verbose_name='Bairro')
    cidade = models.CharField(max_length=100, verbose_name='Cidade')
    estado = models.CharField(max_length=2, verbose_name='Estado')
    cep = models.CharField(max_length=10, verbose_name='CEP')
    referencia = models.CharField(max_length=200, blank=True, verbose_name='Ponto de Referência')
    
    # Controles
    eh_principal = models.BooleanField(default=False, verbose_name='Endereço Principal')
    vezes_utilizado = models.IntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Endereço do Cliente'
        verbose_name_plural = 'Endereços dos Clientes'
        
    def __str__(self):
        return f"{self.apelido} - {self.cliente.nome}"
