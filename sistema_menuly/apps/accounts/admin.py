from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Cliente, EnderecoCliente


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin personalizado para o modelo User"""
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Informações Pessoais'), {'fields': ('first_name', 'last_name', 'telefone')}),
        (_('Permissões'), {'fields': ('is_active', 'is_staff', 'is_superuser', 
                                     'groups', 'user_permissions')}),
        (_('Datas Importantes'), {'fields': ('last_login', 'date_joined')}),
        (_('Tipo de Usuário'), {'fields': ('tipo_usuario',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'tipo_usuario'),
        }),
    )
    
    list_display = ('email', 'first_name', 'last_name', 'tipo_usuario', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'tipo_usuario', 'date_joined')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    """Admin para clientes guests"""
    
    list_display = ('nome', 'celular', 'email', 'total_pedidos', 'valor_total_gasto', 'data_primeiro_pedido')
    list_filter = ('data_primeiro_pedido', 'data_ultimo_pedido')
    search_fields = ('nome', 'celular', 'email')
    ordering = ('-data_ultimo_pedido',)
    
    readonly_fields = ('total_pedidos', 'valor_total_gasto', 'data_primeiro_pedido', 'data_ultimo_pedido')


@admin.register(EnderecoCliente)
class EnderecoClienteAdmin(admin.ModelAdmin):
    """Admin para endereços de clientes"""
    
    list_display = ('cliente', 'apelido', 'endereco', 'bairro', 'cidade', 'eh_principal', 'vezes_utilizado')
    list_filter = ('eh_principal', 'cidade', 'estado')
    search_fields = ('cliente__nome', 'cliente__celular', 'endereco', 'bairro')
