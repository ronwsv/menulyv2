"""
Modelos para gerenciamento de impressoras dos restaurantes
"""
from django.db import models
from apps.restaurantes.models import Restaurante


class ConfiguracaoImpressora(models.Model):
    """Configurações de impressoras para o restaurante"""
    TIPO_CHOICES = [
        ('termica', 'Térmica'),
        ('laser', 'Laser'),
        ('matricial', 'Matricial'),
        ('usb', 'USB Local'),
        ('rede', 'Rede/IP'),
    ]
    
    restaurante = models.ForeignKey(
        Restaurante, 
        on_delete=models.CASCADE, 
        related_name='impressoras_config'
    )
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='termica')
    ip_address = models.GenericIPAddressField(
        blank=True, 
        null=True, 
        help_text="IP para impressoras de rede"
    )
    porta = models.IntegerField(
        default=9100, 
        help_text="Porta para impressoras de rede"
    )
    caminho_usb = models.CharField(
        max_length=200, 
        blank=True, 
        null=True, 
        help_text="Caminho do dispositivo USB (ex: /dev/usb/lp0, COM1)"
    )
    ativa = models.BooleanField(default=True)
    
    # Configurações de impressão
    auto_imprimir_pedido = models.BooleanField(
        default=False, 
        help_text="Imprimir automaticamente ao receber pedido"
    )
    imprimir_cozinha = models.BooleanField(
        default=False, 
        help_text="Imprimir pedido para a cozinha"
    )
    imprimir_balcao = models.BooleanField(
        default=True, 
        help_text="Imprimir pedido para o balcão"
    )
    
    # Configurações de layout
    largura_papel = models.IntegerField(
        default=58, 
        help_text="Largura do papel em mm"
    )
    cortar_papel = models.BooleanField(default=True)
    imprimir_logo = models.BooleanField(default=True)
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Configuração de Impressora'
        verbose_name_plural = 'Configurações de Impressoras'
        ordering = ['nome']
        app_label = 'lojistas'
    
    def __str__(self):
        return f'{self.nome} - {self.restaurante.nome}'
    
    @property
    def status_display(self):
        return "Ativa" if self.ativa else "Inativa"
    
    @property
    def conexao_display(self):
        if self.tipo == 'rede':
            return f"{self.ip_address}:{self.porta}"
        elif self.tipo == 'usb':
            return self.caminho_usb or "USB"
        return self.get_tipo_display()


class LogImpressao(models.Model):
    """Log de impressões realizadas"""
    STATUS_CHOICES = [
        ('sucesso', 'Sucesso'),
        ('erro', 'Erro'),
        ('pendente', 'Pendente'),
    ]
    
    impressora = models.ForeignKey(
        ConfiguracaoImpressora,
        on_delete=models.CASCADE,
        related_name='logs'
    )
    pedido = models.ForeignKey(
        'pedidos.Pedido',
        on_delete=models.CASCADE,
        related_name='logs_impressao',
        null=True,
        blank=True
    )
    tipo_impressao = models.CharField(
        max_length=50,
        choices=[
            ('pedido', 'Pedido'),
            ('teste', 'Teste'),
            ('relatorio', 'Relatório'),
        ],
        default='pedido'
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    mensagem_erro = models.TextField(blank=True)
    tentativas = models.IntegerField(default=0)
    impresso_em = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Log de Impressão'
        verbose_name_plural = 'Logs de Impressão'
        ordering = ['-impresso_em']
        app_label = 'lojistas'
    
    def __str__(self):
        return f'{self.impressora.nome} - {self.get_tipo_impressao_display()} - {self.status}'
